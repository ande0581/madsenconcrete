# project/address/views.py


from functools import wraps
from flask import flash, redirect, render_template, request, session, url_for, Blueprint


from .forms import AddAddressForm
from project import db
from project.models import Address


##########
# Config #
##########

address_blueprint = Blueprint('address', __name__)

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

@address_blueprint.route('/address_add/<int:customer_id>/', methods=['GET', 'POST'])
@login_required
# Add Address
def address_add(customer_id):
    form = AddAddressForm(request.form)
    error = None
    if request.method == "POST":
        if form.validate_on_submit():
            address = Address(
                form.street.data.upper(),
                form.city.data.upper(),
                form.state.data.upper(),
                form.zip.data,
                customer_id
            )
            db.session.add(address)
            db.session.commit()
            flash('New Address was successfully added')
            return redirect(url_for('customer.customer_details', customer_id=customer_id))
    return render_template('address_form.html', form=form, error=error)


# Edit Address
@address_blueprint.route('/address_edit/<int:address_edit_id>/', methods=['GET', 'POST'])
@login_required
def address_edit(address_edit_id):
    error = None
    address = Address.query.get(address_edit_id)
    form = AddAddressForm(obj=address)
    if request.method == 'POST':
        if form.validate_on_submit():
            address.street = form.street.data.upper()
            address.city = form.city.data.upper()
            address.state = form.state.data.upper()
            address.zip = form.zip.data
            db.session.commit()
            flash('Address was successfully edited')
            return redirect(url_for('customer.customer_details', customer_id=address.customer_id))
    return render_template('address_form.html', form=form, error=error)


# Address Delete
@address_blueprint.route('/address_delete/<int:address_del_id>/', methods=['GET', 'POST'])
@login_required
def address_delete(address_del_id):
    address = Address.query.get(address_del_id)
    customer_id = address.customer_id
    db.session.delete(address)
    db.session.commit()
    flash("The address was deleted")
    return redirect(url_for('customer.customer_details', customer_id=customer_id))

