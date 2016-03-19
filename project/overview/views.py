# project/overview/views.py


from functools import wraps
from flask import flash, redirect, render_template, session, url_for, Blueprint

from project import db
from project.models import Customer, Address, Bid

##########
# config #
##########

overview_blueprint = Blueprint('overview', __name__)

####################
# Helper Functions #
####################


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first')
            return redirect(url_for('user.login'))
    return wrap


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (getattr(form, field).label.text, error), 'error')


def query_all_customers():
    return db.session.query(Customer).order_by(Customer.name.asc())


def query_all_addresses():
    return db.session.query(Address)


##########
# Routes #
##########


# Overview of Everything
@overview_blueprint.route('/overview/')
@login_required
def overview():

    needs_bid = db.session.query(Bid).filter_by(status='Needs Bid').order_by(Bid.scheduled_bid_date.asc())
    job_started = db.session.query(Bid).filter_by(status='Job Started').order_by(Bid.actual_start.asc())
    job_accepted = db.session.query(Bid).filter_by(status='Job Accepted').order_by(Bid.tentative_start.asc())
    awaiting_acceptance = db.session.query(Bid).filter_by(status='Awaiting Customer Acceptance').order_by(Bid.scheduled_bid_date.desc())

    all_databases = [needs_bid, job_started, job_accepted, awaiting_acceptance]

    # combine customer and address and bid together
    database_list = []
    for one_database in all_databases:
        for bid in one_database:
            bid_info = dict()
            bid_info['customer_name'] = db.session.query(Customer.name).filter_by(id=bid.customer_id).first()
            bid_info['customer_name'] = bid_info['customer_name'][0]
            bid_info['customer_id'] = bid.customer_id
            bid_info['bid_description'] = bid.description
            bid_info['bid_status'] = bid.status
            bid_info['bid_id'] = bid.id

            if bid_info['bid_status'] == 'Needs Bid':
                if bid.scheduled_bid_date:
                    bid_info['bid_date'] = bid.scheduled_bid_date.strftime('%x %I:%M %p')
            elif bid_info['bid_status'] == 'Job Started':
                if bid.actual_start:
                    bid_info['bid_date'] = bid.actual_start.strftime('%x')
            elif bid_info['bid_status'] == 'Job Accepted':
                if bid.tentative_start:
                    bid_info['bid_date'] = bid.tentative_start.strftime('%x')
            elif bid_info['bid_status'] == 'Awaiting Customer Acceptance':
                if bid.scheduled_bid_date:
                    bid_info['bid_date'] = bid.scheduled_bid_date.strftime('%x')
            else:
                bid_info['bid_date'] = "Something didn't work right!!"

            bid_info['address_street'] = db.session.query(Address.street).filter_by(customer_id=bid.customer_id).first()
            bid_info['address_street'] = bid_info['address_street'][0]
            bid_info['address_city'] = db.session.query(Address.city).filter_by(customer_id=bid.customer_id).first()
            bid_info['address_city'] = bid_info['address_city'][0]
            bid_info['address_state'] = db.session.query(Address.state).filter_by(customer_id=bid.customer_id).first()
            bid_info['address_state'] = bid_info['address_state'][0]
            bid_info['address_zip'] = db.session.query(Address.zip).filter_by(customer_id=bid.customer_id).first()
            bid_info['address_zip'] = bid_info['address_zip'][0]

            telephone = db.session.query(Customer.telephone).filter_by(id=bid.customer_id).first()
            if telephone[0]:
                bid_info['customer_telephone'] = "({}) {}-{}".format(telephone[0][:3], telephone[0][3:6], telephone[0][6:])
            else:
                bid_info['customer_telephone'] = ""

            database_list.append(bid_info)

    return render_template('overview.html', bids=database_list)
