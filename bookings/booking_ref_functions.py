import datetime
from dateutil.relativedelta import relativedelta
from settings import PROPERTIES
from settings import MAPPINGS


# CONSTANTS

BUSINESS_OPENING_DATE = datetime.datetime(2011, 01, 01)
BUSINESS_OPENING_YEAR = 0

BUSINESS_CURRENT_DATE = datetime.datetime.now()
CURRENT_OPERATING_YEAR = 5

MONTHS = [ 'JAN' , 'FEB' , 'MAR'
         , 'APR' , 'MAY' , 'JUN'
         , 'JUL' , 'AUG' , 'SEP'
         , 'OCT' , 'NOV' , 'DEC']


def yearsafter(years, from_date=None):
    if from_date is None:
        from_date = datetime.datetime.now()
    return from_date + relativedelta(years=years)


def get_booking_property(booking_ref):
    booking_property = None
    
    for code in PROPERTIES:
        if code == booking_ref[1:3]:
            booking_property = PROPERTIES[code]
            break
    return booking_property


def get_booking_arrival_date(booking_ref):
    booking_arrival_day = get_booking_arrival_day(booking_ref)
    booking_year = get_booking_year(booking_ref)
    result = None
    for i,month in enumerate(MONTHS):
        if month == booking_ref[3:6].upper():
            result = datetime.datetime(booking_year.year
                                    , i+1
                                    , booking_arrival_day)
    if result is None:
        raise Exception("Invalid Booking Reference: %s" % booking_ref)
    return result


def get_booking_departure_day(booking_ref):
    try:
        day = int(booking_ref[8:])
    except ValueError, e:
        raise Exception("Invalid Booking Reference: %s" % booking_ref)
    return day


def get_booking_year(booking_ref):
    try:
        years = int(booking_ref[0])
    except ValueError, e:
        print ("Invalid Booking Reference: %s" % booking_ref)
        raise e

    return yearsafter(years, BUSINESS_OPENING_DATE)


def get_booking_arrival_day(booking_ref):
    try:
        day = int(booking_ref[6:8])
    except ValueError, e:
        print booking_ref
        raise e
    return day


def get_booking_departure_date(booking_ref):
    booking_property        = get_booking_property(booking_ref)
    booking_year            = get_booking_year(booking_ref)
    booking_arrival_day     = get_booking_arrival_day(booking_ref)
    booking_arrival_date    = get_booking_arrival_date(booking_ref)
    booking_arrival_month   = booking_arrival_date.month
    booking_departure_day   = get_booking_departure_day(booking_ref)
    booking_departure_month = booking_arrival_month
    
    if booking_departure_day < booking_arrival_day:
        booking_departure_month += 1
        if booking_departure_month == 13:
            booking_departure_month = 1
            booking_year = datetime.datetime(booking_year.year + 1, booking_year.month, booking_year.day)
    
    try:
        booking_departure_date = datetime.datetime(booking_year.year, booking_departure_month, booking_departure_day)
    except ValueError, e:
        print 
        print booking_year.year, booking_departure_month, booking_departure_day
        raise e
    return booking_departure_date


def get_commission(booking_ref):
    return MAPPINGS[get_booking_property(booking_ref)]['commission']


def get_booking_commission(booking_ref):
    return MAPPINGS[get_booking_property(booking_ref)]['booking_commission']


def get_house_owner_commission(booking_ref):
    return MAPPINGS[get_booking_property(booking_ref)]['house_owner_commission']


def get_booking_greeting(booking_ref):
    return MAPPINGS[get_booking_property(booking_ref)]['greeting']


def get_booking_cleaning(booking_ref):
    return MAPPINGS[get_booking_property(booking_ref)]['cleaning']


def get_booking_laundry(booking_ref, number_of_people):
    return MAPPINGS[get_booking_property(booking_ref)]['laundry'][number_of_people]


def get_booking_consumables(booking_ref, number_of_people):
    return MAPPINGS[get_booking_property(booking_ref)]['consumables'][number_of_people]


def derive(booking_ref, number_of_people):
    """ Derive all the derivable fields from a valid booking reference string
        
        Returns a dictionary of the derived fields 
    """

    booking_property        = get_booking_property(booking_ref)
    booking_year            = get_booking_year(booking_ref)
    booking_arrival_date    = get_booking_arrival_date(booking_ref)
    booking_departure_date  = get_booking_departure_date(booking_ref)
    commission              = get_commission(booking_ref)
    booking_commission      = get_booking_commission(booking_ref)
    house_owner_commission  = get_house_owner_commission(booking_ref)
    booking_greeting = get_booking_greeting(booking_ref)
    booking_cleaning = get_booking_cleaning(booking_ref)
    booking_laundry = get_booking_laundry(booking_ref, number_of_people)
    booking_consumables = get_booking_consumables(booking_ref, number_of_people)
    
    return { 'booking_year': booking_year
           , 'booking_property': booking_property
           , 'booking_arrival_date': booking_arrival_date
           , 'booking_departure_date': booking_departure_date
           , 'commission' : commission
           , 'booking_commission' : booking_commission
           , 'house_owner_commission' : house_owner_commission
           , 'booking_greeting' : booking_greeting
           , 'booking_cleaning' : booking_cleaning
           , 'booking_laundry' : booking_laundry
           , 'booking_consumables' : booking_consumables
           }
