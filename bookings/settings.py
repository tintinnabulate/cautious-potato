SPREADSHEET_ID = 'spreadsheetid'

PROPERTIES = { 'AS': 'AS'
             , 'A3': 'A3'
             , 'NP': 'NP'
             , 'WS': 'WS'
             , 'AM': 'AM'
             , 'TC': 'TC'
             }

MAPPINGS = { 
    'AS':
    { 'calendar'    : 'calendar1'
    , 'commission'  : 0.0
    , 'booking_commission' : 0.0
    , 'house_owner_commission' : 0.1
    , 'greeting'    : 0.0
    , 'laundry'     : { 1 : 0.0
                      , 2 : 0.0
                      , 3 : 0.0
                      , 4 : 0.0
                      , 5 : 0.0
                      , 6 : 0.0
                      }
    , 'cleaning'    : 0.0
    , 'consumables' : { 1 : 0.0
                      , 2 : 0.0
                      , 3 : 0.0
                      , 4 : 0.0
                      , 5 : 0.0
                      , 6 : 0.0
                      }
    }
    ,
    'A3':
    { 'calendar'    : 'calendar2@group.calendar.google.com'
    , 'commission'  : 0.1 # percent
    , 'booking_commission': 0.0
    , 'house_owner_commission' : 0.1
    , 'greeting'    : 25.00 # sterling
    , 'laundry'     : { 1 : 16.00 # num_people : sterling
                      , 2 : 16.00
                      , 3 : 32.00
                      , 4 : 32.00
                      , 5 : 48.00
                      , 6 : 48.00
                      }
    , 'cleaning'    : 35.00 # sterling
    , 'consumables' : { 1 : 20.00
                      , 2 : 20.00
                      , 3 : 20.00
                      , 4 : 20.00
                      , 5 : 20.00
                      , 6 : 20.00
                      }
    }
    ,
    'AM': 
    { 'calendar'    : 'calendar3@group.calendar.google.com'
    , 'commission'  : 0.1
    , 'booking_commission' : 0.0
    , 'house_owner_commission' : 0.1
    , 'greeting'    : 25.00
    , 'laundry'     : { 1 : 16.00
                      , 2 : 16.00
                      , 3 : 32.00
                      , 4 : 32.00
                      , 5 : 48.00
                      , 6 : 48.00
                      } 
    , 'cleaning'    : 40.00
    , 'consumables' : { 1 : 20.00
                      , 2 : 20.00
                      , 3 : 20.00
                      , 4 : 20.00
                      , 5 : 20.00
                      , 6 : 20.00
                      }
    }
    ,
    'WS':
    { 'calendar'    : 'calendar4@group.calendar.google.com'
    , 'commission'  : 0.1
    , 'booking_commission' : 0.0
    , 'house_owner_commission' : 0.1
    , 'greeting'    : 25.00
    , 'laundry'     : { 1 : 16.00
                      , 2 : 16.00
                      , 3 : 32.00
                      , 4 : 32.00
                      , 5 : 48.00
                      , 6 : 48.00
                      } 
    , 'cleaning'    : 45.00
    , 'consumables' : { 1 : 24.50
                      , 2 : 24.50
                      , 3 : 27.00
                      , 4 : 27.00
                      , 5 : 29.50
                      , 6 : 29.50
                      }
    }
    ,
    'NP':
    { 'calendar'    : 'calendar5@group.calendar.google.com'
    , 'commission'  : 0.1
    , 'booking_commission' : 0.0
    , 'house_owner_commission' : 0.1
    , 'greeting'    : 25.00
    , 'laundry'     : { 1 : 16.00
                      , 2 : 16.00
                      , 3 : 32.00
                      , 4 : 32.00
                      , 5 : 48.00
                      , 6 : 48.00
                      } 
    , 'cleaning'    : 40.00
    , 'consumables' : { 1 : 20.00
                      , 2 : 20.00
                      , 3 : 20.00
                      , 4 : 20.00
                      , 5 : 20.00
                      , 6 : 20.00
                      }
    }
    ,
    'TC':
    { 'calendar'    : 'calendar6@group.calendar.google.com'
    , 'commission'  : 0.1
    , 'booking_commission' : 0.0
    , 'house_owner_commission' : 0.1
    , 'greeting'    : 25.00
    , 'laundry'     : { 1 : 16.00
                      , 2 : 16.00
                      , 3 : 32.00
                      , 4 : 32.00
                      , 5 : 48.00
                      , 6 : 48.00
                      }
    , 'cleaning'    : 45.0
    , 'consumables' : { 1 : 24.50
                      , 2 : 24.50
                      , 3 : 27.00
                      , 4 : 27.00
                      , 5 : 29.50
                      , 6 : 29.50
                      }
    }
}


DEBUG=True
CSRF_ENABLED=True
CSRF_SESSION_KEY=''
SEND_FILE_MAX_AGE_DEFAULT = 43200

SECRET_KEY = ''
SECRET_KEY_TEST = ''

GOOGLE_OAUTH2_CLIENT_SECRETS_FILE = 'client_secrets.json'
GOOGLE_OAUTH2_CLIENT_SECRETS_FILE_TEST = 'client_secrets_test.json'
