# project/calculator/forms.py


from flask_wtf import Form
from wtforms import StringField, FloatField
from wtforms.validators import DataRequired, Length, Email, Optional


class CalculateSlab(Form):
    slab_thickness = FloatField('slab_thickness', validators=[Optional()])
    slab_width = FloatField('slab_width', validators=[Optional()])
    slab_length = FloatField('slab_length', validators=[Optional()])

