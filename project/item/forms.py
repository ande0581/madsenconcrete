# project/item/forms.py


from flask_wtf import Form
from wtforms import SelectField, FloatField, StringField
from wtforms.validators import DataRequired, Optional


class AddBidItemForm(Form):
    quantity = FloatField('quantity', validators=[DataRequired()])
    service_id = SelectField(
        'Item',
        coerce=int,
        validators=[DataRequired()],
        choices=[])


class AddCustomBidItemForm(Form):
    total = FloatField('total', validators=[Optional()])
    description = StringField('customer description', validators=[DataRequired()])