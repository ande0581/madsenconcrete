__author__ = 'Jeff'
# http://stackoverflow.com/questions/12288454/how-to-import-custom-jinja2-filters-from-another-file-and-using-flask

import jinja2
from flask import Blueprint
import re


filter_blueprint = Blueprint('filters', __name__)


@jinja2.contextfilter
@filter_blueprint.app_template_filter()
# This filter removes anything inside parentheses including the parentheses.
# This is removing the unit of measure from the printed bid [ie (cu/ft) ]
def scrub_description(context, item_description):
    return re.sub(r'\([^)]*\)', '', item_description)

