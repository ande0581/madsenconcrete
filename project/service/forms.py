# project/service/forms.py


from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class AddServiceForm(Form):
    description = StringField('description', validators=[DataRequired()])
    cost = StringField('cost', validators=[DataRequired()])