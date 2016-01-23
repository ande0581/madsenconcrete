# project/calculator/views.py


import pytz  # used to configure local timezones
import datetime
from functools import wraps
from flask import flash, redirect, render_template, request, session, url_for, Blueprint
from .forms import CalculateSlab



##########
# config #
##########

calculator_blueprint = Blueprint('calculator', __name__)

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

##########
# Routes #
##########


# Main Calculator Page
@calculator_blueprint.route('/calculator/', methods=['GET', 'POST'])
@login_required
def calculator():
    error = None
    form = CalculateSlab(request.form)
    return render_template('calculator.html', form=form, error=error)
