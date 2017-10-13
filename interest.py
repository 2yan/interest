from datetime import datetime, timedelta
import numpy as np
import math


class debt():
    owed = None
    owed_interest = 0

    rate = None
    paid = 0

    def __init__(self, start, rate):
        self.owed = start
        self.rate = rate

    def pay_interest(self, payment):
        remaining = payment - self.owed_interest

        if remaining > 0:
            self.owed_interest = 0
            return remaining

        if remaining <= 0:
            self.owed_interest = self.owed_interest - payment
            return 0

    def pay_base(self, payment):
        remaining = payment - self.owed

        if remaining > 0:
            self.owed = 0
            return remaining

        if remaining <= 0:
            self.owed = self.owed - payment
            return 0

    def pay(self, payment):
        cash = self.pay_interest(payment)
        if cash > 0:
            cash = self.pay_base(payment)
        return cash

    def simple_compound(self):
        if self.owed > 0:
            old = self.owed_interest
            new = (old  * (self.rate + 1))
            self.owed_interest = new
            return old - new
        return 0
    def complex_compound(self):
        if (self.owed > 0) or (self.owed_interest > 0):
            old = self.owed + self.owed_interest

            new = ( old * self.rate)
            self.owed_interest = self.owed_interest + new
            return new
        return 0



def days_remaining(start, rate, size, payment_interval, compounds ):
    rate = rate/compounds
    compound_interval = int(365/compounds)
    temp = debt(start, rate)
    compound_size = 0

    day = 1
    while True:
        if day%payment_interval == 0:
            temp.pay(size)

        if day%compound_interval == 0:
            compound_size = temp.complex_compound()
            if compound_size > size:
                return np.inf

        day = day + 1
        if temp.owed == 0:
            return day

def find_min_payment(start, rate, payment_interval, compounds):
    size = 0
    while True:
        result = days_remaining(start, rate, size, payment_interval, compounds)
        if result != np.inf:
            return {'payment':size, 'days':result}
        size = size + 1


def sigmoid( x ):
    return (1/(1 + math.pow(math.e, -x)))

def find_payment_for_date(start, days, rate, payment_interval, compounds ):
    size =500

    for num in range(0, 10000):
        result = days_remaining(start, rate, size, payment_interval, compounds)
        sig = sigmoid(result - days) - 0.5
        size = size + sig
        if abs(result - days) < 1:
            return size
    return size