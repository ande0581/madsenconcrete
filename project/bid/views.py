# project/bid/views.py

import pytz  # used to configure local timezones
import datetime
from functools import wraps
from flask import flash, redirect, render_template, request, session, url_for, Blueprint
from sqlalchemy.sql import func
from .forms import AddBidForm, EditBidForm
from project import db
from project.models import Bid, BidItem, Address, Customer
from flask_weasyprint import HTML, render_pdf


##########
# config #
##########

bid_blueprint = Blueprint('bid', __name__)

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


def query_one_customer(cust_id):
    return db.session.query(Customer).filter_by(id=cust_id).first()  # don't have to loop list to get results


def query_bid_address(cust_bid_address_id):
    return db.session.query(Address).filter_by(id=cust_bid_address_id).first()


def query_one_bid_items(bid_items_id):
    return db.session.query(BidItem).filter_by(bid_id=bid_items_id)


def sum_all_items_one_bid(bid_id):
    return db.session.query(func.sum(BidItem.total)).filter_by(bid_id=bid_id).first()


def query_bid(bid_id):
    return db.session.query(Bid).filter_by(id=bid_id).first()


def query_payment_balance(bid_id_payment):
    customer_bid = db.session.query(Bid).filter_by(id=bid_id_payment).first()
    if customer_bid.paid_in_full_amount:
        return customer_bid.paid_in_full_amount
    elif customer_bid.down_payment_amount:
        return customer_bid.down_payment_amount
    else:
        return 0


##########
# Routes #
##########

# Bid Add
@bid_blueprint.route('/bid_add/<int:bid_customer_id>/<int:bid_address_id>/', methods=['GET', 'POST'])
@login_required
def bid_add(bid_customer_id, bid_address_id):
    error = None
    form = AddBidForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            add_bid = Bid(
                description=form.description.data,
                notes=None,
                timestamp=datetime.datetime.now(pytz.timezone('US/Central')),
                customer_id=bid_customer_id,
                address_id=bid_address_id,
                scheduled_bid_date=form.scheduled_bid_date.data,
                tentative_start=None,
                actual_start=None,
                completion_date=None,
                down_payment_amount=None,
                down_payment_date=None,
                paid_in_full_amount=None,
                paid_in_full_date=None,
                status='Needs Bid'
            )
            db.session.add(add_bid)
            db.session.commit()
            flash("The bid was successfully added")
            return redirect(url_for('customer.customer_details', customer_id=bid_customer_id))
    return render_template('bid_form_add.html',
                           action="/bid_add/" + str(bid_customer_id) + "/" + str(bid_address_id) + "/",
                           form=form,
                           address=query_bid_address(bid_address_id),
                           customer=query_one_customer(bid_customer_id),
                           error=error)


# Bid Edit
@bid_blueprint.route('/bid_edit/<int:bid_edit_id>/', methods=['GET', 'POST'])
@login_required
def bid_edit(bid_edit_id):
    error = None
    bid = Bid.query.get(bid_edit_id)
    form = EditBidForm(obj=bid)
    if request.method == 'POST':
        if form.validate_on_submit():
            bid.description = form.description.data
            bid.notes = form.notes.data
            bid.status = form.status.data
            bid.scheduled_bid_date = form.scheduled_bid_date.data
            bid.tentative_start = form.tentative_start.data
            bid.actual_start = form.actual_start.data
            bid.completion_date = form.completion_date.data
            bid.down_payment_date = form.down_payment_date.data
            bid.down_payment_amount = form.down_payment_amount.data
            bid.paid_in_full_date = form.paid_in_full_date.data
            bid.paid_in_full_amount = form.paid_in_full_amount.data
            db.session.commit()
            flash('Bid was successfully edited')
    return render_template('bid_form_edit.html',
                           action="/bid_edit/" + str(bid_edit_id) + "/",
                           form=form,
                           address=query_bid_address(bid.address_id),
                           customer=query_one_customer(bid.customer_id),
                           items=query_one_bid_items(bid_edit_id),
                           sum_of_items=sum_all_items_one_bid(bid_edit_id),
                           bid_id=bid.id,
                           payment_balance=query_payment_balance(bid_edit_id),
                           error=error)


# Bid Delete
@bid_blueprint.route('/bid_delete/<int:bid_delete_id>/', methods=['GET', 'POST'])
@login_required
def bid_delete(bid_delete_id):
    bid = Bid.query.get(bid_delete_id)
    db.session.query(Bid).filter_by(id=bid_delete_id).delete()
    db.session.commit()
    flash("The bid was deleted")
    return redirect(url_for('customer.customer_details', customer_id=bid.customer_id))


# Bid Create PDF
@bid_blueprint.route('/bid_create_pdf/<int:bid_id_pdf>/', methods=['GET', 'POST'])
@login_required
def bid_create_pdf(bid_id_pdf):
    bid = db.session.query(Bid).filter_by(id=bid_id_pdf).first()
    address = db.session.query(Address).filter_by(id=bid.address_id).first()
    customer = db.session.query(Customer).filter_by(id=address.customer_id).first()
    html = render_template('bid_pdf.html',
                           bid_id=bid_id_pdf,
                           sum_of_items=sum_all_items_one_bid(bid_id_pdf),
                           items=query_one_bid_items(bid_id_pdf),
                           bid=query_bid(bid_id_pdf),
                           bid_time=datetime.datetime.now(pytz.timezone('US/Central')).strftime('%x'),
                           address=address,
                           customer=customer)
    return render_pdf(HTML(string=html))


