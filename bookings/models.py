from google.appengine.ext import db


class Booking(db.Model):
    booking_reference = db.StringProperty(required=True)
    property = db.StringProperty(required=True)
    first_name = db.StringProperty(required=True)
    last_name = db.StringProperty(required=True)
    email = db.EmailProperty(required=True)
    phone = db.PhoneNumberProperty(required=True)
    notes = db.TextProperty(required=False)
    booking_date = db.DateTimeProperty(auto_now_add=True)
    source = db.StringProperty(required=True)
    arrival_date = db.DateProperty(required=True)
    departure_date = db.DateProperty(required=True)
    number_of_people = db.IntegerProperty(required=True)
    gross = db.FloatProperty(required=True)
    is_discount = db.BooleanProperty(required=True)
    commission = db.FloatProperty(required=True)
    due_date = db.DateProperty(required=True)
    is_commission = db.BooleanProperty(required=True)
    is_greeting = db.FloatProperty(required=True)
    is_laundry = db.FloatProperty(required=True)
    is_cleaning = db.FloatProperty(required=True)
    is_con = db.FloatProperty(required=True)
    net = db.FloatProperty(required=True)
    # TODO: Change the below to required=True
    booking_fee = db.FloatProperty(required=False)
    house_owner_fee = db.FloatProperty(required=False)
    total_fees = db.FloatProperty(required=False)
    owner_income = db.FloatProperty(required=False)


class AccessEntry(db.Model):
    when = db.DateTimeProperty(auto_now_add=True)
    first_name = db.StringProperty(required=True)
    last_name = db.StringProperty(required=True)
    email = db.StringProperty(required=True)
    enabled = db.BooleanProperty(required=True)
    acl = db.StringProperty(required=True)
