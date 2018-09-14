# -- coding: utf-8 --

def calculate(gross, source, booking_commission, house_owner_commission):
    booking_commission = 0.15 if source == 'booking.com' else booking_commission
    booking_fee = booking_commission * gross
    net = gross - booking_fee
    house_owner_fee = house_owner_commission * net
    house_owner_fee = max(35.0, house_owner_fee)
    return net, booking_fee, house_owner_fee
