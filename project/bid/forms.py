# project/bid/forms.py


from flask_wtf import Form
from wtforms import DateField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Optional


class AddBidForm(Form):
    description = TextAreaField('description', validators=[DataRequired()])
    scheduled_bid_date = DateField('Scheduled Bid Date (mm/dd/yyyy)', validators=[Optional()], format='%m/%d/%Y')


class EditBidForm(Form):
    description = TextAreaField('description', validators=[DataRequired()])
    status = SelectField(
        'Status',
        validators=[DataRequired()],
        choices=[
            ('Needs Bid', 'Needs Bid'), ('Awaiting Customer Acceptance', 'Awaiting Customer Acceptance'),
            ('Job Accepted', 'Job Accepted'), ('Job Started', 'Job Started'), ('Job Completed', 'Job Completed'),
            ('Job Declined', 'Job Declined')])
    scheduled_bid_date = DateField('Scheduled Bid Date (mm/dd/yyyy)', validators=[Optional()], format='%m/%d/%Y')
    tentative_start = DateField('Tentative Start Date (mm/dd/yyyy)', validators=[Optional()], format='%m/%d/%Y')
    actual_start = DateField('Actual Start Date (mm/dd/yyyy)', validators=[Optional()], format='%m/%d/%Y')
    completion_date = DateField('Completion Date (mm/dd/yyyy)', validators=[Optional()], format='%m/%d/%Y')