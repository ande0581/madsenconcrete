# project/address/forms.py


from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Optional


class AddAddressForm(Form):
    street = StringField('Street', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired(), Length(min=2, max=2)])
    zip = StringField('Zip', validators=[Optional(), Length(min=5, max=5)])