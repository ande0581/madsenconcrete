# project/customer/views.py


import pytz  # used to configure local timezones
import datetime
from functools import wraps
from flask import flash, redirect, render_template, request, session, url_for, Blueprint

from .forms import AddCustomerForm, SearchCustomersForm
from project import db
from project.models import Customer, Journal, Bid, Address


##########
# config #
##########

customer_blueprint = Blueprint('customer', __name__)

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


def query_customer_addresses(cust_address_id):
    return db.session.query(Address).filter_by(customer_id=cust_address_id).order_by(Address.city.asc())


def query_one_customer(cust_id):
    return db.session.query(Customer).filter_by(id=cust_id).first()  # don't have to loop list to get results


def query_all_bids_one_customer(cust_bid_id):
    return db.session.query(Bid).filter_by(customer_id=cust_bid_id).order_by(Bid.timestamp.desc())


def query_customer_journal(cust_journal_id):
    return db.session.query(Journal).filter_by(customer_id=cust_journal_id).order_by(Journal.timestamp.desc())


##########
# Routes #
##########

# Main Customer Page
@customer_blueprint.route('/customers/', methods=['GET', 'POST'])
@customer_blueprint.route('/customers/page/', methods=['GET', 'POST'])
@customer_blueprint.route('/customers/page/<int:page>/', methods=['GET', 'POST'])
@login_required
def customers(page=1):
    error = None
    form = SearchCustomersForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit() and len(form.name.data) > 0:
            search = "%" + form.name.data + "%"
            # Show all search results on one page
            all_customers = Customer.query.filter(Customer.name.like(search)).order_by(Customer.name.asc())
            all_customers = all_customers.paginate(page, all_customers.count(), False)
        else:
            all_customers = Customer.query.order_by(Customer.name.asc())
            all_customers = all_customers.paginate(page, 20, False)
    else:
        all_customers = Customer.query.order_by(Customer.name.asc()).paginate(page, 20, False)
    return render_template('customers.html', customers=all_customers, form=form, error=error)


# Specific Customer Details
@customer_blueprint.route('/customer_details/<int:customer_id>/')
@login_required
def customer_details(customer_id):
    error = None
    return render_template('customer_details.html',
                           addresses=query_customer_addresses(customer_id),
                           customer=query_one_customer(customer_id),
                           action="/address_add/" + str(customer_id) + "/",
                           customer_id=customer_id,
                           bids=query_all_bids_one_customer(customer_id),
                           journal=query_customer_journal(customer_id),
                           error=error)


# Add New Customer
@customer_blueprint.route('/customer_add/', methods=['GET', 'POST'])
@login_required
def customer_add():
    error = None
    form = AddCustomerForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            add_customer = Customer(
                form.name.data.title(),
                form.email.data.lower(),
                form.telephone.data,
                datetime.datetime.now(pytz.timezone('US/Central'))
            )
            db.session.add(add_customer)
            db.session.commit()
            flash('New customer was successfully added')
            return redirect(url_for('customer.customers'))
    return render_template('customer_form.html', action="/customer_add/", form=form, error=error)


# Edit Customer
@customer_blueprint.route('/customer_edit/<int:customer_edit_id>/', methods=['GET', 'POST'])
@login_required
def customer_edit(customer_edit_id):
    error = None
    customer = Customer.query.get(customer_edit_id)
    form = AddCustomerForm(obj=customer)
    if request.method == 'POST':
        if form.validate_on_submit():
            customer.name = form.name.data.title()
            customer.email = form.email.data.lower()
            customer.telephone = form.telephone.data
            db.session.commit()
            flash('Customer was successfully edited')
            return redirect(url_for('customer.customer_details', customer_id=customer.id))
    return render_template('customer_form.html',
                           action="/customer_edit/" + str(customer_edit_id) + "/",
                           form=form,
                           error=error
                           )


# Delete Customer, Need to make sure i recursively delete all table entries
@customer_blueprint.route('/customer_delete/<int:customer_del_id>', methods=['GET', 'POST'])
@login_required
def customer_delete(customer_del_id):
    my_customer = Customer.query.get(customer_del_id)
    db.session.delete(my_customer)
    db.session.commit()
    flash("The customer was deleted")
    return redirect(url_for('customer.customers'))
