# project/bid/forms.py


from flask_wtf import Form
from wtforms import DateField, DateTimeField, SelectField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Optional


class AddBidForm(Form):
    description = TextAreaField('description', validators=[DataRequired()])
    scheduled_bid_date = DateTimeField('Scheduled Bid Date (yyyy-mm-dd)', validators=[Optional()])


class EditBidForm(Form):
    description = TextAreaField('description', validators=[DataRequired()])
    notes = TextAreaField('description', validators=[Optional()])
    status = SelectField(
        'Status',
        validators=[DataRequired()],
        choices=[
            ('Needs Bid', 'Needs Bid'), ('Awaiting Customer Acceptance', 'Awaiting Customer Acceptance'),
            ('Job Accepted', 'Job Accepted'), ('Job Started', 'Job Started'), ('Job Completed', 'Job Completed'),
            ('Job Declined', 'Job Declined')])
    scheduled_bid_date = DateTimeField('Scheduled Bid Date (yyyy-mm-dd hh:mm:ss)', validators=[Optional()])
    tentative_start = DateField('Tentative Start Date (yyyy-mm-dd)', validators=[Optional()])
    actual_start = DateField('Actual Start Date (yyyy-mm-dd)', validators=[Optional()])
    completion_date = DateField('Completion Date (yyyy-mm-dd)', validators=[Optional()])
    down_payment_amount = DecimalField('Down Payment Amount', validators=[Optional()])
    down_payment_date = DateField('Down Payment Date (yyyy-mm-dd)', validators=[Optional()])
    final_payment_amount = DecimalField('Final Payment Amount', validators=[Optional()])
    final_payment_date = DateField('Final Payment Date (yyyy-mm-dd)', validators=[Optional()])


class SearchBidForm(Form):
    bid_type = SelectField(
        'Bid Type',
        validators=[DataRequired()],
        choices=[
            ('All Bids', 'All Bids'), ('Needs Bid', 'Needs Bid'),
            ('Awaiting Customer Acceptance', 'Awaiting Customer Acceptance'), ('Job Accepted', 'Job Accepted'),
            ('Job Started', 'Job Started'), ('Job Completed', 'Job Completed'), ('Job Declined', 'Job Declined')]
    )
