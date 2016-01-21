# project/customer/forms.py


from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Email, Optional


class AddCustomerForm(Form):
    name = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[Optional(), Email()])
    telephone = StringField('Telephone', validators=[Optional(), Length(min=10, max=10)])

class SearchCustomersForm(Form):
    name = StringField('Name', validators=[Optional()])