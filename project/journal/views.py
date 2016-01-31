# project/journal/views.py


import pytz  # used to configure local timezones
import datetime
from functools import wraps
from flask import flash, redirect, render_template, request, session, url_for, Blueprint

from .forms import AddJournalForm
from project import db
from project.models import Journal


##########
# config #
##########

journal_blueprint = Blueprint('journal', __name__)

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


# Add New Journal Entry
@journal_blueprint.route('/journal_add/<int:journal_add_id>/', methods=['GET', 'POST'])
@login_required
def journal_add(journal_add_id):
    error = None
    form = AddJournalForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            add_journal = Journal(
                form.body.data,
                datetime.datetime.now(pytz.timezone('US/Central')),
                journal_add_id
            )
            db.session.add(add_journal)
            db.session.commit()
            flash('New journal entry was successfully added')
            return redirect(url_for('customer.customer_details', customer_id=journal_add_id))
    return render_template('journal_form.html', action="/journal_add/" + str(journal_add_id) + "/", form=form,
                           error=error)


# Edit Journal
@journal_blueprint.route('/journal_edit/<int:journal_edit_id>/', methods=['GET', 'POST'])
@login_required
def journal_edit(journal_edit_id):
    error = None
    journal = Journal.query.get(journal_edit_id)
    form = AddJournalForm(obj=journal)
    if request.method == 'POST':
        if form.validate_on_submit():
            journal.body = form.body.data
            db.session.commit()
            flash('Journal was successfully edited')
            return redirect(url_for('customer.customer_details', customer_id=journal.customer_id))
    return render_template('journal_form.html', form=form, error=error)


# Journal Delete
@journal_blueprint.route('/journal_delete/<int:journal_del_id>/', methods=['GET', 'POST'])
@login_required
def journal_delete(journal_del_id):
    journal = Journal.query.get(journal_del_id)
    customer_id = journal.customer_id
    db.session.delete(journal)
    db.session.commit()
    flash("The journal entry was deleted")
    return redirect(url_for('customer.customer_details', customer_id=customer_id))
