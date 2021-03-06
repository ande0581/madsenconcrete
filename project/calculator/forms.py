# project/calculator/forms.py


from flask_wtf import Form
from wtforms import StringField, FloatField
from wtforms.validators import DataRequired, Length, Email, Optional


class CalculatorForm(Form):
    slab_thickness = FloatField('slab_thickness', validators=[Optional()])
    slab_width = FloatField('slab_width', validators=[Optional()])
    slab_length = FloatField('slab_length', validators=[Optional()])
    slab_quantity = FloatField('slab_quantity', validators=[Optional()])
    round_diameter = FloatField('round_diameter', validators=[Optional()])
    round_depth = FloatField('round_depth', validators=[Optional()])
    round_quantity = FloatField('round_quantity', validators=[Optional()])
    triangle_side_a = FloatField('triangle_side_a', validators=[Optional()])
    triangle_side_b = FloatField('triangle_side_b', validators=[Optional()])
    triangle_side_c = FloatField('triangle_side_c', validators=[Optional()])
    triangle_thickness = FloatField('triangle_thickness', validators=[Optional()])

