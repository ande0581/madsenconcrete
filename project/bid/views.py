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
    bid_results = None
    all_data_list = []
    if request.method == 'POST':
        if form.bid_type.data == 'Needs Bid':
            bid_results = db.session.query(Bid).filter_by(status='Needs Bid').order_by(Bid.scheduled_bid_date.asc())
        elif form.bid_type.data == 'Job Started':
            bid_results = db.session.query(Bid).filter_by(status='Job Started').order_by(Bid.actual_start.asc())
        elif form.bid_type.data == 'Job Accepted':
            bid_results = db.session.query(Bid).filter_by(status='Job Accepted').order_by(Bid.tentative_start.asc())
        elif form.bid_type.data == 'Awaiting Customer Acceptance':
            bid_results = db.session.query(Bid).filter_by(status='Awaiting Customer Acceptance').order_by(Bid.scheduled_bid_date.desc())
        elif form.bid_type.data == 'Job Completed':
            bid_results = db.session.query(Bid).filter_by(status='Job Completed').order_by(Bid.completion_date.desc())
        elif form.bid_type.data == 'Job Declined':
            bid_results = db.session.query(Bid).filter_by(status='Job Declined').order_by(Bid.scheduled_bid_date.desc())
        else:
            bid_results = db.session.query(Bid).order_by(Bid.timestamp.asc())

    # combine customer and address and bid together
    if bid_results:
        for bid in bid_results:
            all_data_dict = {}
            all_data_dict['customer_name'] = db.session.query(Customer.name).filter_by(id=bid.customer_id).first()
            all_data_dict['customer_name'] = all_data_dict['customer_name'][0]
            all_data_dict['customer_id'] = bid.customer_id
            all_data_dict['bid_description'] = bid.description
            all_data_dict['bid_status'] = bid.status
            all_data_dict['bid_id'] = bid.id

            if all_data_dict['bid_status'] == 'Needs Bid':
                if bid.scheduled_bid_date:
                    all_data_dict['bid_date'] = bid.scheduled_bid_date.strftime('%x')
            elif all_data_dict['bid_status'] == 'Job Started':
                if bid.actual_start:
                    all_data_dict['bid_date'] = bid.actual_start.strftime('%x')
            elif all_data_dict['bid_status'] == 'Job Accepted':
                if bid.tentative_start:
                    all_data_dict['bid_date'] = bid.tentative_start.strftime('%x')
            elif all_data_dict['bid_status'] == 'Awaiting Customer Acceptance':
                if bid.scheduled_bid_date:
                    all_data_dict['bid_date'] = bid.scheduled_bid_date.strftime('%x')
            elif all_data_dict['bid_status'] == 'Job Completed':
                if bid.completion_date:
                    all_data_dict['bid_date'] = bid.completion_date.strftime('%x')
            elif all_data_dict['bid_status'] == 'Job Declined':
                if bid.scheduled_bid_date:
                    all_data_dict['bid_date'] = bid.scheduled_bid_date.strftime('%x')
            else:
                all_data_dict['bid_date'] = "Something didn't work right!!"

            all_data_dict['address_street'] = db.session.query(Address.street).filter_by(customer_id=bid.customer_id).first()
            all_data_dict['address_street'] = all_data_dict['address_street'][0]
            all_data_dict['address_city'] = db.session.query(Address.city).filter_by(customer_id=bid.customer_id).first()
            all_data_dict['address_city'] = all_data_dict['address_city'][0]
            all_data_dict['address_state'] = db.session.query(Address.state).filter_by(customer_id=bid.customer_id).first()
            all_data_dict['address_state'] = all_data_dict['address_state'][0]
            all_data_dict['address_zip'] = db.session.query(Address.zip).filter_by(customer_id=bid.customer_id).first()
            all_data_dict['address_zip'] = all_data_dict['address_zip'][0]

            telephone = db.session.query(Customer.telephone).filter_by(id=bid.customer_id).first()
            if telephone[0]:
                all_data_dict['customer_telephone'] = "({}) {}-{}".format(telephone[0][:3], telephone[0][3:6], telephone[0][6:])
            else:
                all_data_dict['customer_telephone'] = ""

            all_data_list.append(all_data_dict)
    return render_template('view_bids.html',
                           bids=all_data_list,
                           form=form,
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

    #return html
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



# Bid Create PDF Invoice
@bid_blueprint.route('/bid_create_pdf_invoice/<int:bid_id_pdf>/', methods=['GET', 'POST'])
@login_required
def bid_create_pdf_invoice(bid_id_pdf):
    bid = Bid.query.get(bid_id_pdf)
    address = Address.query.get(bid.address_id)
    customer = Customer.query.get(address.customer_id)
    html = render_template('bid_pdf_invoice.html',
                           bid_id=bid_id_pdf,
                           sum_of_items=sum_all_items_one_bid(bid_id_pdf),
                           items=query_one_bid_items(bid_id_pdf),
                           bid=query_bid(bid_id_pdf),
                           bid_time=datetime.datetime.now(pytz.timezone('US/Central')).strftime('%x'),
                           address=address,
                           customer=customer)
    #return html
    return render_pdf(HTML(string=html))


