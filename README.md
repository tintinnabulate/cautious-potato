# Business logic

This section describes the functionality of the booking process

## When a booking is submitted

When a booking is submitted, the following operations happen, in order:

1. The booking reference number is used to calculate the operating year (years
   after business started operating), the arrival date of the customer, the
   departure date of the customer, and the property the customer will be staying
   at. These values are used in subsequent steps. See
   `bookings/booking_ref_functions.py` for the implementation.

2. The booking causes 3 Google calendar entries to be created. These are:

    1. Meet & Greet, 
    2. The booking itself, 
    3. Cleaning.

3. The booking causes 1 email to be sent: The booking confirmation + terms & conditions
   is emailed from the bookings email account to the customer. The templates for
   this email are in `bookings/email_templates.py`

4. The booking causes a Google Sheet to be populated with a new row, containing
   the booking details of the bookiing.

5. Finally, the booking causes the Database (see section 'Database') to be
   populated with a new entry, containing the booking details of the booking.

`views.py` is where most of the business logic is stored. The function of the
bookings booking form, its dependencies, the flow of information, can be understood
from reading this code.  

# Dependencies

The software depends on Google Mail, Google Calendar, Google Sheets, and Google
App Engine. It requires that you have a valid oauth2 token, which is used to
access the admin's (bookings owner) email, calendar and google sheet.

# Implementation details

This section describes the technology used to build the bookings booking form.

## Technology used

### Platform

This bookings booking form is a website whose domain and hosting is provided by
Google App Engine, also known as Google Cloud Platform. If you are maintaining
this, You would do well to understand how to deploy and configure projects with
Google App Engine - try following a tutorial. This will help understand how
this project is laid out.

It may be worth mentioning that `git`, the version control software, runs on
Google App Engine, and was very useful in developing this application. You
would do well to learn it if you do not know it already.

### Web Framework Engine

The web framework that has been chosen to run the bookings booking form is Flask. It
is a Python2.7 web framework.

See `requirements.txt` to see the software dependencies (both for Python and
Flask) in use for this project.

Flask WTForms is used for the booking form. `forms.py` contains the
implementation of the booking form which is injected into the page, and
contains all of the form fields and input validation.

## Database

The database that is used is the Google App Engine Datastore. All data
submitted with the booking form is stored in this Datastore.

`bookings/models.py` defines the database objects in use, including the
Booking database
object that is central to this application.

## Dumping a CSV of bookings into Google Datastore

You may need to dump the CSV of a bunch of bookings into the bookings database - I
have written a utility script `bookings/csv2db.py` for this very purpose. It
may require some tweaking, but essentially, it takes a CSV of bookings either
from excel or a CSV dump from another Google Datastore, and writes those
entries into the Bookings Datastore (this is described in 'Business logic' Step 5).
Note that it *does not* (!) do any of the other steps in described in 'Business
logic'.

# Deploying the bookings booking form for live use

The file `Makefile` is used to deploy the bookings booking form to the live site.
From the Google App Engine console, run `make deploy` to deploy the software.

## Configuration

The file `bookings/settings.py` has most (perhaps all... - but you may do
well to also look inside views.py and client_secret.json) of the application
configuration settings necessary to deploy this on another Google App Engine
account.

Note that, at the time of this writing, the application depends on certain
technologies being available in its environment (see 'Dependencies'), so will
require heavy rearchitecting in order to work with a different environment.

# Document Control and References

## Changes History

1.  First started tracking changes in README.txt

    commit id
    Author: me <coder@someemailaddressyeahhh.com>
    Date:   Thu Nov 2 19:05:06 2017 +0000

        Write up of README
