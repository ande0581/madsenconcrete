# project/__init.py


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('_config.py')
db = SQLAlchemy(app)

from project.address.views import address_blueprint
from project.bid.views import bid_blueprint
from project.customer.views import customer_blueprint
from project.item.views import item_blueprint
from project.journal.views import journal_blueprint
from project.overview.views import overview_blueprint
from project.service.views import service_blueprint
from project.user.views import user_blueprint

# register our blueprints
app.register_blueprint(address_blueprint)
app.register_blueprint(bid_blueprint)
app.register_blueprint(customer_blueprint)
app.register_blueprint(item_blueprint)
app.register_blueprint(journal_blueprint)
app.register_blueprint(overview_blueprint)
app.register_blueprint(service_blueprint)
app.register_blueprint(user_blueprint)


