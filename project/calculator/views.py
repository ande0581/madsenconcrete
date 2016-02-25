# project/calculator/views.py


import pytz  # used to configure local timezones
import datetime
from functools import wraps
from flask import flash, redirect, render_template, request, session, url_for, Blueprint
from .forms import CalculatorForm
import math


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
    triangle_volume_yards = None
    triangle_volume_60lbs = None
    triangle_volume_80lbs = None
    form = CalculatorForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            side_a = form.triangle_side_a.data
            side_b = form.triangle_side_b.data
            side_c = form.triangle_side_c.data
            triangle_thickness = form.triangle_thickness.data
            if side_a and side_b and side_c and triangle_thickness:
                triangle_perimeter = (side_a + side_b + side_c) / 2
                triangle_area = math.sqrt(triangle_perimeter * (triangle_perimeter - side_a) * (triangle_perimeter - side_b) * (triangle_perimeter - side_c))
                triangle_volume_yards = (triangle_area * (triangle_thickness / 12)) / 27
                triangle_volume_60lbs = (triangle_area * (triangle_thickness / 12)) / .45
                triangle_volume_80lbs = (triangle_area * (triangle_thickness / 12)) / .6
    return render_template('calculator.html',
                           action="/calculator/",
                           triangle_volume_yards=triangle_volume_yards,
                           triangle_volume_60lbs=triangle_volume_60lbs,
                           triangle_volume_80lbs=triangle_volume_80lbs,
                           form=form,
                           error=error)
