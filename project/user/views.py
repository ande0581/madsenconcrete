# project/user/views.py


from functools import wraps
from flask import flash, redirect, render_template, request, session, url_for, Blueprint
from .forms import LoginForm
from project import app  # Not sure this the right way to do this, this is for _config import username/password


##########
# config #
##########

user_blueprint = Blueprint('user', __name__)

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


@user_blueprint.route('/', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            if request.form['name'] == app.config['USERNAME'] and \
                            request.form['password'] == app.config['PASSWORD']:
                session['logged_in'] = True
                flash('Welcome!')
                return redirect(url_for('overview.overview'))
            else:
                error = "Invalid username or password"
        else:
            error = 'Both fields are required'
    return render_template('login.html', form=form, error=error)


@user_blueprint.route('/logout/')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    flash('Goodbye!')
    return redirect(url_for('user.login'))
