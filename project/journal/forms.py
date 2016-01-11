# project/journal/forms.py


from flask_wtf import Form
from wtforms import TextAreaField
from wtforms.validators import DataRequired


class AddJournalForm(Form):
    body = TextAreaField('Body', validators=[DataRequired()])