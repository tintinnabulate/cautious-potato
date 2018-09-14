from flask.ext import wtf
from flask.ext.wtf import validators
from wtforms import StringField
from wtforms import TextAreaField
from wtforms import SelectField
from wtforms import DateField
from wtforms import BooleanField
from wtforms import SubmitField
from wtforms import FloatField
from wtforms import IntegerField
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import Optional
from wtforms.validators import Length
from wtforms.validators import NumberRange
from wtforms.validators import ValidationError
from datetime import datetime

from booking_ref_functions import derive
    
BOOKING_LENGTH_WARNING = "Booking Reference code must be exactly 10 characters long"

class BookingForm(wtf.Form):
    booking_reference = StringField('Booking Reference', validators=[DataRequired(), Length(min=10, max=10, message=BOOKING_LENGTH_WARNING)])
    source = SelectField('Source', choices=[ ('email', 'Email')
                                           , ('phone', 'Phone')
                                           , ('holidaylettings', 'Holiday Lettings')
                                           , ('booking.com', 'Booking.com')
                                           , ('airbnb', 'AirBnb')
                                           , ('visit', 'Visit')
                                           , ('other', 'Other') ])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone = StringField('Mobile Number', validators=[DataRequired()])
    email = StringField('Email Address', validators=[Optional(), Email()])
    notes = StringField('Notes', validators=[Optional()])
    number_of_people = IntegerField('Number of People', validators=[DataRequired()])
    gross = FloatField('Gross', validators=[DataRequired()])
    is_discount = BooleanField('Discount?')
    is_commission = BooleanField('Commission?')
    is_greeting = BooleanField('Greeting?')
    is_cleaning = BooleanField('Cleaning?')
    is_laundry = BooleanField('Laundry?')
    is_con = BooleanField('Consumables?')

    def validate_booking_reference(form, field):
        try:
            derive(field.data, 1)
        except Exception, e:
            raise ValidationError(str(e))
