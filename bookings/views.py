# -- coding: utf-8 --

TEST = False # If True, run in test mode. If False, run in live mode

import os
from os.path import basename

from bookings import app
import settings
from google.appengine.ext import db
from models import Booking
from booking_ref_functions import derive
from email_templates import get_booking_confirmation_email_body
from email_templates import get_booking_confirmation_email_no_payment_body
from email_templates import get_pseudo_pdf_attachment_body
from calculations import calculate

from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect
from flask import request
from flask import session
from forms import BookingForm

import datetime
from decimal import Decimal

import apiclient
from oauth2client.contrib.flask_util import UserOAuth2

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import base64

from google.appengine.api import urlfetch


OAUTH2 = UserOAuth2(app)
CALENDAR = apiclient.discovery.build('calendar', 'v3')
SCOPES = ["https://www.googleapis.com/auth/calendar", "https://www.googleapis.com/auth/spreadsheets", 'https://www.googleapis.com/auth/gmail.send']


@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/view_bookings')
def list_bookings():
    bookings = db.GqlQuery("SELECT * FROM Booking ORDER BY booking_date")
    return render_template('list_registrations.html', bookings=bookings)


def is_already_paid(booking_details):
    return booking_details['source'] in ('airbnb', 'booking.com')


def extract_booking_details(form):
    booking_reference = form.booking_reference.data
    number_of_people = int(form.number_of_people.data)
    derived = derive(booking_reference, number_of_people)
    property = derived['booking_property']
    first_name = form.first_name.data
    last_name = form.last_name.data
    source = form.source.data
    email = form.email.data
    notes = form.notes.data
    phone = form.phone.data
    arrival_date = (derived['booking_arrival_date']).date()
    departure_date = (derived['booking_departure_date']).date()
    gross = float(form.gross.data)
    is_discount = bool(form.is_discount.data)
    commission = float(derived['commission'])
    due_date = datetime.date.today()
    is_commission = bool(form.is_commission.data)
    is_greeting = derived['booking_greeting'] if bool(form.is_greeting.data) else 0.0
    is_laundry = derived['booking_laundry'] if bool(form.is_laundry.data) else 0.0
    is_cleaning = derived['booking_cleaning'] if bool(form.is_cleaning.data) else 0.0
    is_con = derived['booking_consumables'] if bool(form.is_con.data) else 0.0
    booking_commission = float(derived['booking_commission'])
    booking_commission = 0.15 if source == 'booking.com' else booking_commission
    house_owner_commission = float(derived['house_owner_commission'])
    net, booking_fee, house_owner_fee = calculate(gross, source, booking_commission, house_owner_commission)
    total_fees = sum([house_owner_fee, is_greeting, is_laundry, is_cleaning, is_con])
    owner_income = net - total_fees
    booking_date = datetime.date.today()
    booking = Booking( 
             booking_reference = booking_reference
           , property = property
           , first_name = first_name
           , last_name = last_name
           , source = source
           , email = email
           , notes = notes
           , phone = phone
           , arrival_date = arrival_date
           , departure_date = departure_date
           , number_of_people = number_of_people
           , gross = gross
           , is_discount = is_discount
           , commission = commission
           , due_date = due_date
           , is_commission = is_commission
           , is_greeting = is_greeting
           , is_laundry = is_laundry
           , is_cleaning = is_cleaning
           , is_con = is_con
           , net = net
           , booking_fee = booking_fee
           , house_owner_fee = house_owner_fee
           , total_fees = total_fees
           , owner_income = owner_income
        )
    booking_details = { 'booking' : booking
                      , 'booking_reference' : booking_reference
                      , 'property' : property
                      , 'first_name' : first_name
                      , 'last_name' : last_name
                      , 'source' : source
                      , 'email' : email
                      , 'notes' : notes
                      , 'phone' : phone
                      , 'arrival_date' : arrival_date#.strftime("%d/%m/%Y")
                      , 'departure_date' : departure_date#.strftime("%d/%m/%Y")
                      , 'number_of_people' : number_of_people
                      , 'number_of_nights' : (departure_date - arrival_date).days
                      , 'net' : net
                      , 'gross' : gross
                      , 'is_discount' : is_discount
                      , 'is_commission' : is_commission
                      , 'is_greeting' : is_greeting
                      , 'is_laundry' : is_laundry
                      , 'is_cleaning' : is_cleaning
                      , 'is_con' : is_con
                      , 'booking_date' : booking_date
                      , 'commission' : commission
                      , 'due_date' : due_date
                      , 'booking_fee' : booking_fee
                      , 'house_owner_fee' : house_owner_fee
                      , 'total_fees' : total_fees
                      , 'owner_income' : owner_income
                      }
    return booking_details


def store_booking_in_database(booking_details):
    booking_details['booking'].put()


def add_one_day(departure_date):
    """ When creating an Event in Google Calendar that spans whole multiple
    days (i.e. 'All Day' is ticked), you must add one day to the end in order
    for it to finish on midnight of the departure date """
    one_day = datetime.timedelta(days=1)
    return departure_date + one_day


def get_guest_reminder(booking_details):
    return {
            "end": {
             "date": (add_one_day(booking_details['departure_date'])).strftime("%Y-%m-%d"),
             "timeZone": "Europe/London"
            },
            "start": {
             "date": booking_details['arrival_date'].strftime("%Y-%m-%d"),
             "timeZone": "Europe/London"
            },
            "summary": "%(first_name)s %(last_name)s, %(number_of_people)d people. %(phone)s" % booking_details,
            "description": "Phone number: %(phone)s Email: %(email)s  %(number_of_people)d people staying, leaving on %(departure_date)s. Booked through %(source)s. Notes: %(notes)s" % booking_details
    }


def get_greeting_reminder(booking_details):
    return {
            "end": {
             "dateTime": booking_details['arrival_date'].strftime("%Y-%m-%dT15:30:00"),
             "timeZone": "Europe/London"
            },
            "start": {
             "dateTime": booking_details['arrival_date'].strftime("%Y-%m-%dT15:00:00"),
             "timeZone": "Europe/London"
            },
            "summary": "MG",
            "description": "Phone number: %(phone)s Email: %(email)s  %(number_of_people)d people staying, leaving on %(departure_date)s. Booked through %(source)s. Notes: %(notes)s" % booking_details
    }


def get_cleaning_reminder(booking_details):
    return {
            "end": {
             "dateTime": booking_details['departure_date'].strftime("%Y-%m-%dT13:00:00"),
             "timeZone": "Europe/London"
            },
            "start": {
             "dateTime": booking_details['departure_date'].strftime("%Y-%m-%dT11:00:00"),
             "timeZone": "Europe/London"
            },
            "summary": "Clean",
            "description": ""
    }


def create_calendar_reminders(booking_details):
    guest_duration_reminder = get_guest_reminder(booking_details)
    greeting_reminder = get_greeting_reminder(booking_details)
    cleaning_reminder = get_cleaning_reminder(booking_details)
    calHttp = OAUTH2.http()
    if TEST:
        calendarId = 'primary' # TODO: comment this out when LIVE
    else:
        calendarId = settings.MAPPINGS[booking_details['property']]['calendar']
    create_reminder = lambda event: CALENDAR.events().insert(calendarId=calendarId, body=event).execute(http=calHttp)
    guest_response = create_reminder(guest_duration_reminder)
    greeting_response = create_reminder(greeting_reminder)
    cleaning_response = create_reminder(cleaning_reminder)
    return guest_response, greeting_response, cleaning_response


def create_spreadsheet_entry(booking_details):
    sheetHttp = OAUTH2.http()
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    SHEETS = apiclient.discovery.build('sheets', 'v4', http=sheetHttp, discoveryServiceUrl=discoveryUrl)

    spreadsheetId = settings.SPREADSHEET_ID
    if TEST:
        spreadsheetId = 'testspreadsheetid' # TODO: comment this out when LIVE

    rangeName = 'Sheet1!A1:A10'

    data = {
      "range": "Sheet1!A1:A10",
      "majorDimension": "ROWS",
      "values": [ [ booking_details['booking_reference']
                  , booking_details['property']
                  , booking_details['first_name']
                  , booking_details['last_name']
                  , booking_details['email']
                  , "'" + booking_details['phone'] # so that phone number displays in cell
                  , booking_details['notes']
                  , str(booking_details['booking_date'])
                  , booking_details['source']
                  , str(booking_details['arrival_date'])
                  , str(booking_details['departure_date'])
                  , str(booking_details['number_of_people'])
                  , str(booking_details['gross'])
                  , str(booking_details['net'])
                  , str(booking_details['is_discount'])
                  , str(booking_details['commission'])
                  , str(booking_details['due_date'])
                  , str(booking_details['is_commission'])
                  , str(booking_details['is_greeting'])
                  , str(booking_details['is_laundry'])
                  , str(booking_details['is_cleaning'])
                  , str(booking_details['is_con'])
                  , str(booking_details['booking_fee'])
                  , str(booking_details['house_owner_fee'])
                  , str(booking_details['total_fees'])
                  , str(booking_details['owner_income'])
                  ] ],
    }
    urlfetch.set_default_fetch_deadline(60)
    result = SHEETS.spreadsheets().values().append(
        spreadsheetId=spreadsheetId, body=data, valueInputOption='USER_ENTERED', range=rangeName).execute(sheetHttp)
    return result


def email_guest_booking_confirmation(booking_details):
    gmailHttp = OAUTH2.http()
    gmailService = apiclient.discovery.build('gmail', 'v1', http=gmailHttp)
    
    strFrom = 'me'
    strTo = booking_details['email']
    
    # Create the root message and fill in the from, to, and subject headers
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = 'Booking Confirmation'
    msgRoot['From'] = strFrom
    msgRoot['To'] = strTo
    msgRoot.preamble = 'This is a multi-part message in MIME format.'
    
    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)
    
    msgText = MIMEText('This email is only available to read in HTML format. Please switch your email viewing mode to HTML to read this email.')
    msgAlternative.attach(msgText)

    body = get_booking_confirmation_email_body(booking_details)
    if is_already_paid(booking_details):
        body = get_booking_confirmation_email_no_payment_body(booking_details)

    
    # This example assumes the image is in the current directory
    fp = open('./bookings/static/images/logo_medium.jpg', 'rb')
    msgImage = MIMEImage(fp.read(), _subtype="jpg")
    fp.close()
    
    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image2>')
    msgRoot.attach(msgImage)

    fp = open('./bookings/static/images/header_large.jpg', 'rb')
    msgImage = MIMEImage(fp.read(), _subtype="jpg")
    fp.close()
    
    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)

    if is_already_paid(booking_details): # airbnb email viewer does not display PDF, so include TnC in text.
       body += get_pseudo_pdf_attachment_body()
    else:
        attachment_path = "./bookings/static/pdf/foo.pdf"

        with open(attachment_path) as pdf_file:
            pdf = MIMEApplication(pdf_file.read(), _subtype='pdf')
            pdf.add_header('content-disposition', 'attachment', filename=basename(attachment_path))

        msgRoot.attach(pdf)

    msgText = MIMEText(body.encode('utf-8'), 'html', 'utf-8')
    msgAlternative.attach(msgText)

    msg = {'raw': base64.urlsafe_b64encode(msgRoot.as_string())}

    results = gmailService.users().messages().send(userId='me', body=msg).execute(http=gmailHttp)
    return results


@app.route('/booking', methods=['GET', 'POST'])
@OAUTH2.required(scopes=SCOPES)
def new_booking_1():
    form = BookingForm()
    if form.validate_on_submit():
        booking_details = extract_booking_details(form)
        create_calendar_reminders(booking_details)
        create_spreadsheet_entry(booking_details)
        email_guest_booking_confirmation(booking_details)
        store_booking_in_database(booking_details)
        flash("Booking made.")
        return redirect(url_for('homepage'))
    return render_template('new_booking_1.html', form=form, properties=settings.PROPERTIES)


@app.route('/calendars', methods=['GET', 'POST'])
@OAUTH2.required(scopes=["https://www.googleapis.com/auth/calendar"])
def list_calendarIds():
    output = ""
    http = OAUTH2.http()
    page_token = None
    while True:
      calendar_list = CALENDAR.calendarList().list(pageToken=page_token).execute(http=http)
      output+="<ul>"
      for calendar_list_entry in calendar_list['items']:
        output+="<li>"
        output+="Name: " + calendar_list_entry['summary'] + ", calendarId: " + calendar_list_entry['id']
        output+="</li>"
      output+="</ul>"
      page_token = calendar_list.get('nextPageToken')
      if not page_token:
        break
    return output


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
