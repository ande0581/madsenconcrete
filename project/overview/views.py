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


def query_all_bids():
    return db.session.query(Bid)


##########
# Routes #
##########


# Overview of Everything
@overview_blueprint.route('/overview/')
@login_required
def overview():
    error = None
    return render_template('overview.html',
                           bids=query_all_bids(),
                           customers=query_all_customers(),
                           addresses=query_all_addresses(),
                           error=error)
