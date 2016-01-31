# project/item/views.py

from functools import wraps
from flask import flash, redirect, render_template, request, session, url_for, Blueprint

from .forms import AddBidItemForm, AddCustomBidItemForm
from project import db
from project.models import BidItem, Service


##########
# config #
##########

item_blueprint = Blueprint('item', __name__)

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


def query_services_return_list_of_tuples():
    """ This is used for the AddBidItemForm SelectField choices """
    service_choices = db.session.query(Service).order_by(Service.description.asc())
    choices = []
    for service in service_choices:
            choices.append((service.id, service.description))
    return choices


def query_one_service(service_id):
    return db.session.query(Service).filter_by(id=service_id).first()


##########
# Routes #
##########


# Add New Standard Item
@item_blueprint.route('/item_add/<int:bid_id>/', methods=['GET', 'POST'])
@login_required
def item_add(bid_id):
    error = None
    form = AddBidItemForm(request.form)
    form.service_id.choices = query_services_return_list_of_tuples()
    service = query_one_service(form.service_id.data)
    if request.method == "POST":
        if form.validate_on_submit():
            add_item = BidItem(
                bid_id,
                form.service_id.data,
                service.description,
                form.quantity.data,
                service.cost,
                (form.quantity.data * service.cost)
            )
            db.session.add(add_item)
            db.session.commit()
            flash('New item was successfully added')
            return redirect(url_for('bid.bid_edit', bid_edit_id=bid_id))
    return render_template('item_form.html',
                           action="/item_add/" + str(bid_id) + "/",
                           form=form,
                           error=error,
                           )


# Add New Custom Item
@item_blueprint.route('/item_add_custom/<int:bid_id>/', methods=['GET', 'POST'])
@login_required
def item_add_custom(bid_id):
    error = None
    form = AddCustomBidItemForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            add_item = BidItem(
                bid_id,
                None,
                form.description.data,
                None,
                None,
                form.total.data
            )
            db.session.add(add_item)
            db.session.commit()
            flash('New custom item was successfully added')
            return redirect(url_for('bid.bid_edit', bid_edit_id=bid_id))
    return render_template('item_form_custom.html',
                           action="/item_add_custom/" + str(bid_id) + "/",
                           form=form,
                           error=error,
                           )


# Edit Item on Bid
@item_blueprint.route('/item_edit/<int:item_edit_id>/', methods=['GET', 'POST'])
@login_required
def item_edit(item_edit_id):
    error = None
    item = BidItem.query.get(item_edit_id)
    form = AddBidItemForm(obj=item)
    form.service_id.choices = query_services_return_list_of_tuples()
    service = query_one_service(form.service_id.data)
    if request.method == 'POST':
        if form.validate_on_submit():
            item.service_id = form.service_id.data
            item.description = service.description
            item.quantity = form.quantity.data
            item.cost = service.cost
            item.total = (form.quantity.data * item.cost)
            db.session.commit()
            flash('Item was successfully edited')
            return redirect(url_for('bid.bid_edit', bid_edit_id=item.bid_id))
    return render_template('item_form.html',
                           form=form,
                           error=error)


# Edit Custom Item on Bid
@item_blueprint.route('/item_edit_custom/<int:item_edit_id>/', methods=['GET', 'POST'])
@login_required
def item_edit_custom(item_edit_id):
    error = None
    item = BidItem.query.get(item_edit_id)
    form = AddCustomBidItemForm(obj=item)
    if request.method == 'POST':
        if form.validate_on_submit():
            item.description = form.description.data
            item.total = form.total.data
            db.session.commit()
            flash('Custom item was successfully edited')
            return redirect(url_for('bid.bid_edit', bid_edit_id=item.bid_id))
    return render_template('item_form_custom.html',
                           form=form,
                           error=error)


# Delete Item from Bid
@item_blueprint.route('/item_delete/<int:item_delete_id>/', methods=['GET', 'POST'])
@login_required
def item_delete(item_delete_id):
    bid_item = BidItem.query.get(item_delete_id)
    bid_edit_id = bid_item.bid_id
    db.session.delete(bid_item)
    db.session.commit()
    flash("The item was deleted")
    return redirect(url_for('bid.bid_edit', bid_edit_id=bid_edit_id))
