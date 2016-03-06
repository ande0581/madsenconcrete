# project/bid/views.py

import pytz  # used to configure local timezones
import datetime
import os
from functools import wraps
from flask import flash, redirect, render_template, request, session, url_for, Blueprint
from sqlalchemy.sql import func
from .forms import AddBidForm, EditBidForm, SearchBidForm
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


def query_all_customers():
    return db.session.query(Customer).order_by(Customer.name.asc())


def query_all_addresses():
    return db.session.query(Address)


def query_bid(bid_id):
    return db.session.query(Bid).filter_by(id=bid_id).first()


##########
# Routes #
##########

# View Bids
@bid_blueprint.route('/bids/', methods=['GET', 'POST'])
@login_required
def view_bids():
    error = None
    form = SearchBidForm(request.form)
    query_type = db.session.query(Bid).order_by(Bid.timestamp.asc())
    if request.method == 'POST':
        if form.bid_type.data == 'Needs Bid':
            query_type = db.session.query(Bid).filter_by(status='Needs Bid').order_by(Bid.scheduled_bid_date.asc())
        elif form.bid_type.data == 'Job Started':
            query_type = db.session.query(Bid).filter_by(status='Job Started').order_by(Bid.actual_start.asc())
        elif form.bid_type.data == 'Job Accepted':
            query_type = db.session.query(Bid).filter_by(status='Job Accepted').order_by(Bid.tentative_start.asc())
        elif form.bid_type.data == 'Awaiting Customer Acceptance':
            query_type = db.session.query(Bid).filter_by(status='Awaiting Customer Acceptance').order_by(Bid.scheduled_bid_date.desc())
        elif form.bid_type.data == 'Job Completed':
            query_type = db.session.query(Bid).filter_by(status='Job Completed').order_by(Bid.completion_date.desc())
        elif form.bid_type.data == 'Job Declined':
            query_type = db.session.query(Bid).filter_by(status='Job Declined').order_by(Bid.scheduled_bid_date.desc())
        else:
            query_type = db.session.query(Bid).order_by(Bid.timestamp.asc())
    return render_template('view_bids.html',
                           bids=query_type,
                           form=form,
                           customers=query_all_customers(),
                           addresses=query_all_addresses(),
                           error=error)


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
                final_payment_amount=None,
                final_payment_date=None,
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

            if form.down_payment_amount.data:
                bid.down_payment_amount = form.down_payment_amount.data
            else:
                bid.down_payment_amount = 0

            bid.final_payment_date = form.final_payment_date.data

            if form.final_payment_amount.data:
                bid.final_payment_amount = form.final_payment_amount.data
            else:
                bid.final_payment_amount = 0

            db.session.commit()
            flash('Bid was successfully edited')
    return render_template('bid_form_edit.html',
                           action="/bid_edit/" + str(bid_edit_id) + "/",
                           form=form,
                           address=query_bid_address(bid.address_id),
                           customer=query_one_customer(bid.customer_id),
                           items=query_one_bid_items(bid_edit_id),
                           sum_of_items=sum_all_items_one_bid(bid_edit_id),
                           bid=bid,
                           error=error)


# Bid Delete
@bid_blueprint.route('/bid_delete/<int:bid_delete_id>/', methods=['GET', 'POST'])
@login_required
def bid_delete(bid_delete_id):
    bid = Bid.query.get(bid_delete_id)
    customer_id = bid.customer_id
    db.session.delete(bid)
    db.session.commit()
    flash("The bid was deleted")
    return redirect(url_for('customer.customer_details', customer_id=customer_id))


# Bid Create PDF
@bid_blueprint.route('/bid_create_pdf/<int:bid_id_pdf>/', defaults={'save_to_disk': False}, methods=['GET', 'POST'])
@bid_blueprint.route('/bid_create_pdf/<int:bid_id_pdf>/<save_to_disk>', methods=['GET', 'POST'])
@login_required
def bid_create_pdf(bid_id_pdf, save_to_disk):
    bid = Bid.query.get(bid_id_pdf)
    address = Address.query.get(bid.address_id)
    customer = Customer.query.get(address.customer_id)
    html = render_template('bid_pdf.html',
                           bid_id=bid_id_pdf,
                           sum_of_items=sum_all_items_one_bid(bid_id_pdf),
                           items=query_one_bid_items(bid_id_pdf),
                           bid=query_bid(bid_id_pdf),
                           bid_time=datetime.datetime.now(pytz.timezone('US/Central')).strftime('%x'),
                           address=address,
                           customer=customer)
    if save_to_disk:
        # useful path examples http://stackoverflow.com/questions/5137497/find-current-directory-and-files-directory

        # Set appropriate slash depending on OS
        if os.name =='nt':
            base_dir = "{}\\{}".format(os.getcwd(), 'customer_data')
        else:
            base_dir = "{}/{}".format(os.getcwd(), 'customer_data')

        # Escape illegal directory path characters and replace with underscore
        customer_name = customer.name
        for character in ['<', '>', ':', '"', '/', '\\', '|', '?', '*', ' ']:
            if character in customer_name:
                customer_name = customer_name.replace(character, "_")

        # Set appropriate slash depending on OS
        if os.name =='nt':
            customer_folder = "{}_{}\\".format(customer_name, customer.id)
        else:
            customer_folder = "{}_{}/".format(customer_name, customer.id)

        # Create the directory path
        directory = os.path.join(base_dir, customer_folder)

        # Create directory if it doesnt exist
        if not os.path.isdir(directory):
            os.makedirs(directory)

        # Combine generate filename and combine with path
        current_date = datetime.datetime.now(pytz.timezone('US/Central')).strftime('%Y%m%d%H%M')
        filename = "{}_{}.pdf".format(customer_name, current_date)
        path = directory + filename

        # Create pdf and store it on server
        HTML(string=html).write_pdf(path)

        flash("The bid was saved to hard disk")
        return redirect(url_for('bid.bid_edit', bid_edit_id=bid.id))
    return render_pdf(HTML(string=html))


# Bid Create Receipt PDF
@bid_blueprint.route('/bid_create_receipt/<int:bid_id_pdf>/', methods=['GET', 'POST'])
@login_required
def bid_create_receipt(bid_id_pdf):
    bid = Bid.query.get(bid_id_pdf)
    address = Address.query.get(bid.address_id)
    customer = Customer.query.get(address.customer_id)
    html = render_template('receipt_pdf.html',
                           bid_id=bid_id_pdf,
                           sum_of_items=sum_all_items_one_bid(bid_id_pdf),
                           items=query_one_bid_items(bid_id_pdf),
                           bid=query_bid(bid_id_pdf),
                           bid_time=datetime.datetime.now(pytz.timezone('US/Central')).strftime('%x'),
                           address=address,
                           customer=customer)
    return render_pdf(HTML(string=html))


