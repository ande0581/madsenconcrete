__author__ = 'Jeff'
# project/db_create.py

from project import db
from project.models import Service

# create the database and the db table
db.create_all()

# insert data
db.session.add(Service("Remove - Dirt/Gravel", .50))
db.session.add(Service("Remove - Clay 4", 2.00))
db.session.add(Service("Forming / Grading / Setup", 1.10))
db.session.add(Service("Rebar - Non-coated 3/8 (sq/ft)", .67))
db.session.add(Service("Rebar - Non-coated 1/2 (sq/ft)", .75))
db.session.add(Service("Rebar - Coated 3/8 (sq/ft)", .77))
db.session.add(Service("Rebar - Coated 1/2 (sq/ft)", .84))
db.session.add(Service("Saw Cutting (ft)", 5.00))
db.session.add(Service("Expansion Felt (ft)", 1.00))
db.session.add(Service("Forming / Grading / Setup (sq/ft)", 1.10))
db.session.add(Service("Concrete - Common Gray (cu/ft)", 2.15))
db.session.add(Service("Concrete - Colored (cu/ft)", 3.50))
db.session.add(Service("Concrete - Bag Mix", 8.50))
db.session.add(Service("Concrete - Fiber Mesh (cu/ft)", .10))
db.session.add(Service("Concrete - Sealer (sq/ft)", .50))
db.session.add(Service("Drain Tile Socked (ft)", .88))
db.session.add(Service("Steps - Poured (each)", 500.00))
db.session.add(Service("Black Dirt (cu/ft)", .50))
db.session.add(Service("Sod (sq/ft)", 1.25))
db.session.add(Service("Grass Seed (sq/ft)", .10))
db.session.add(Service("Railing Painted (ft)", 70.00))
db.session.add(Service("Railing Powder Coated (ft)", 90.00))

# commit the changes
db.session.commit()

