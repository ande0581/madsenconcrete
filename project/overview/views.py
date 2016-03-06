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


def query_jobs_need_bid():
    return db.session.query(Bid).filter_by(status='Needs Bid').order_by(Bid.scheduled_bid_date.asc())


def query_jobs_started():
    return db.session.query(Bid).filter_by(status='Job Started').order_by(Bid.actual_start.asc())


def query_jobs_accepted():
    return db.session.query(Bid).filter_by(status='Job Accepted').order_by(Bid.tentative_start.asc())


def query_jobs_awaiting_acceptance():
    return db.session.query(Bid).filter_by(status='Awaiting Customer Acceptance').order_by(Bid.scheduled_bid_date.desc())


##########
# Routes #
##########


# Overview of Everything
@overview_blueprint.route('/overview/')
@login_required
def overview():
    error = None
    return render_template('overview.html',
                           jobs_need_bid=query_jobs_need_bid(),
                           jobs_started=query_jobs_started(),
                           jobs_accepted=query_jobs_accepted(),
                           jobs_awaiting_acceptance=query_jobs_awaiting_acceptance(),
                           customers=query_all_customers(),
                           addresses=query_all_addresses(),
                           error=error)
