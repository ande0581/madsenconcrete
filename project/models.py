__author__ = 'Jeff'
# project/models.py

from project import db
import datetime
import pytz


class Customer(db.Model):

    __tablename__ = "customer"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    telephone = db.Column(db.String, nullable=False)
    created_date = db.Column(db.Date, default=datetime.datetime.now(pytz.timezone('US/Central')))

    def __init__(self, name, email, telephone, created_date):
        self.name = name
        self.email = email
        self.telephone = telephone
        self.created_date = created_date

    def __repr__(self):
        return '<name {0}>'.format(self.name)


class Address(db.Model):

    __tablename__ = "address"

    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    zip = db.Column(db.String, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))

    def __init__(self, street, city, state, zip, customer_id):
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.customer_id = customer_id

    def __repr__(self):
        return '<{0}, {1}, {2}, {3}>'.format(self.street, self.city, self.state, self.zip)


class Journal(db.Model):

    __tablename__ = "journal"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(2000))
    timestamp = db.Column(db.DateTime)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))

    def __init__(self, body, timestamp, customer_id):
        self.body = body
        self.timestamp = timestamp
        self.customer_id = customer_id

    def __repr__(self):
        return '<{}>'.format(self.post)


class Bid(db.Model):

    __tablename__ = "bid"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    notes = db.Column(db.String)
    timestamp = db.Column(db.DateTime)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    scheduled_bid_date = db.Column(db.DateTime)
    tentative_start = db.Column(db.Date)
    actual_start = db.Column(db.Date)
    completion_date = db.Column(db.Date)
    down_payment_amount = db.Column(db.Float)
    down_payment_date = db.Column(db.Date)
    paid_in_full_amount = db.Column(db.Float)
    paid_in_full_date = db.Column(db.Date)
    status = db.Column(db.String)

    def __init__(self, description, notes, timestamp, customer_id, address_id, scheduled_bid_date, tentative_start,
                 actual_start, completion_date, down_payment_amount, down_payment_date, paid_in_full_amount,
                 paid_in_full_date, status):
        self.description = description
        self.notes = notes
        self.timestamp = timestamp
        self.customer_id = customer_id
        self.address_id = address_id
        self.scheduled_bid_date = scheduled_bid_date
        self.tentative_start = tentative_start
        self.actual_start = actual_start
        self.completion_date = completion_date
        self.down_payment_amount = down_payment_amount
        self.down_payment_date = down_payment_date
        self.paid_in_full_amount = paid_in_full_amount
        self.paid_in_full_date = paid_in_full_date
        self.status = status

    def __repr__(self):
        return '<{}>'.format(self.description)


class Service(db.Model):

    __tablename__ = "service"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    cost = db.Column(db.Float)

    def __init__(self, description, cost):
        self.description = description
        self.cost = cost

    def __repr__(self):
        return '<{}>'.format(self.description)


class BidItem(db.Model):

    __tablename__ = "bid_item"

    id = db.Column(db.Integer, primary_key=True)
    bid_id = db.Column(db.Integer, db.ForeignKey('bid.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    description = db.Column(db.String)
    quantity = db.Column(db.Float)
    cost = db.Column(db.Float)
    total = db.Column(db.Float)

    def __init__(self, bid_id, service_id, description, quantity, cost, total):
        self.bid_id = bid_id
        self.service_id = service_id
        self.description = description
        self.quantity = quantity
        self.cost = cost
        self.total = total

    def __repr__(self):
        return '<{}>'.format(self.description)

