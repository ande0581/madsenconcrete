# project/service/views.py


from functools import wraps
from flask import flash, redirect, render_template, request, session, url_for, Blueprint

from .forms import AddServiceForm
from project import db
from project.models import Service


##########
# config #
##########

service_blueprint = Blueprint('service', __name__)

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


def query_all_services():
    return db.session.query(Service).order_by(Service.description.asc())


##########
# Routes #
##########


# Overview of Services
@service_blueprint.route('/services/')
@login_required
def services():
    error = None
    return render_template('services.html',
                           services=query_all_services(),
                           error=error)


# Add New Service
@service_blueprint.route('/service_add/', methods=['GET', 'POST'])
@login_required
def service_add():
    error = None
    form = AddServiceForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            add_service = Service(
                form.description.data,
                form.cost.data
            )
            db.session.add(add_service)
            db.session.commit()
            flash('New service was successfully added')
            return redirect(url_for('service.services'))
    return render_template('service_form.html', action="/service_add/", form=form, error=error)


# Edit Service
@service_blueprint.route('/service_edit/<int:service_edit_id>/', methods=['GET', 'POST'])
@login_required
def service_edit(service_edit_id):
    error = None
    service = Service.query.get(service_edit_id)
    form = AddServiceForm(obj=service)
    if request.method == 'POST':
        if form.validate_on_submit():
            service.description = form.description.data
            service.cost = form.cost.data
            db.session.commit()
            flash('Service was successfully edited')
            return redirect(url_for('service.services'))
    return render_template('service_form.html',
                           form=form,
                           services=query_all_services(),
                           error=error)


# Delete Service
@service_blueprint.route('/service_delete/<int:service_delete_id>/', methods=['GET', 'POST'])
@login_required
def service_delete(service_delete_id):
    service = Service.query.get(service_delete_id)
    db.session.delete(service)
    db.session.commit()
    flash("The service was deleted")
    return redirect(url_for('service.services'))
