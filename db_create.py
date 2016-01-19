__author__ = 'Jeff'
# project/db_create.py

from project import db
from project.models import Service, Customer
import datetime
import pytz

# create the database and the db table
db.create_all()

# insert services
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

# insert customers
db.session.add(Customer("Admin Smith", "adminsmith@domain.com", "6125551000", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Betty Smith", "bettysmith@domain.com", "6125551001", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Charlie Smith", "charliesmith@domain.com", "6125551002", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("David Smith", "davodsmith@domain.com", "6125551003", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Edward Smith", "edwardsmith@domain.com", "6125551004", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Frank Smith", "franksmith@domain.com", "6125551005", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Gale Smith", "galesmith@domain.com", "6125551006", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Hunter Smith", "huntersmith@domain.com", "6125551007", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Ingrid Smith", "ingridsmith@domain.com", "6125551008", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("John Smith", "johnsmith@domain.com", "6125551009", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Kelly Smith", "kellysmith@domain.com", "6125551010", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Linda Smith", "lindasmith@domain.com", "6125551011", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Micheal Smith", "michealsmith@domain.com", "61255510012", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Nancy Smith", "nancysmith@domain.com", "6125551013", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Orlando Smith", "orlandosmith@domain.com", "6125551014", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Paul Smith", "paulsmith@domain.com", "6125551015", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Quinn Smith", "quinnsmith@domain.com", "6125551016", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Robert Smith", "robertsmith@domain.com", "6125551017", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Susan Smith", "susansmith@domain.com", "6125551018", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Tammy Smith", "tammysmith@domain.com", "6125551019", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Uma Smith", "umasmith@domain.com", "6125551020", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Victor Smith", "victorsmith@domain.com", "6125551021", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Wyatt Smith", "wyattsmith@domain.com", "6125551022", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Xavier Smith", "xaviersmith@domain.com", "6125551023", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Yelena Smith", "yelenasmith@domain.com", "6125551024", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Zoe Smith", "zoesmith@domain.com", "6125551025", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Admin Olson", "adminolson@domain.com", "7635551000", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Betty Olson", "bettyolson@domain.com", "7635551001", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Charlie Olson", "charlieolson@domain.com", "7635551002", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("David Olson", "davodolson@domain.com", "7635551003", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Edward Olson", "edwardolson@domain.com", "7635551004", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Frank Olson", "frankolson@domain.com", "7635551005", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Gale Olson", "galeolson@domain.com", "7635551006", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Hunter Olson", "hunterolson@domain.com", "7635551007", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Ingrid Olson", "ingridolson@domain.com", "7635551008", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("John Olson", "johnolson@domain.com", "7635551009", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Kelly Olson", "kellyolson@domain.com", "7635551010", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Linda Olson", "lindaolson@domain.com", "7635551011", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Micheal Olson", "michealolson@domain.com", "76355510012", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Nancy Olson", "nancyolson@domain.com", "7635551013", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Orlando Olson", "orlandoolson@domain.com", "7635551014", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Paul Olson", "paulolson@domain.com", "7635551015", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Quinn Olson", "quinnolson@domain.com", "7635551016", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Robert Olson", "robertolson@domain.com", "7635551017", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Susan Olson", "susanolson@domain.com", "7635551018", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Tammy Olson", "tammyolson@domain.com", "7635551019", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Uma Olson", "umaolson@domain.com", "7635551020", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Victor Olson", "victorolson@domain.com", "7635551021", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Wyatt Olson", "wyattolson@domain.com", "7635551022", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Xavier Olson", "xavierolson@domain.com", "7635551023", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Yelena Olson", "yelenaolson@domain.com", "7635551024", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Zoe Olson", "zoeolson@domain.com", "7635551025", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Admin Hickman", "adminh@gmail.com", "9525551000", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Betty Hickman", "bettyh@gmail.com", "9525551001", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Charlie Hickman", "charlieh@gmail.com", "9525551002", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("David Hickman", "davodh@gmail.com", "9525551003", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Edward Hickman", "edwardh@gmail.com", "9525551004", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Frank Hickman", "frankh@gmail.com", "9525551005", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Gale Hickman", "galeh@gmail.com", "9525551006", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Hunter Hickman", "hunterh@gmail.com", "9525551007", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Ingrid Hickman", "ingridh@gmail.com", "9525551008", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("John Hickman", "johnh@gmail.com", "9525551009", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Kelly Hickman", "kellyh@gmail.com", "9525551010", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Linda Hickman", "lindah@gmail.com", "9525551011", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Micheal Hickman", "michealh@gmail.com", "95255510012", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Nancy Hickman", "nancyh@gmail.com", "9525551013", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Orlando Hickman", "orlandoh@gmail.com", "9525551014", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Paul Hickman", "paulh@gmail.com", "9525551015", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Quinn Hickman", "quinnh@gmail.com", "9525551016", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Robert Hickman", "roberth@gmail.com", "9525551017", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Susan Hickman", "susanh@gmail.com", "9525551018", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Tammy Hickman", "tammyh@gmail.com", "9525551019", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Uma Hickman", "umah@gmail.com", "9525551020", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Victor Hickman", "victorh@gmail.com", "9525551021", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Wyatt Hickman", "wyatth@gmail.com", "9525551022", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Xavier Hickman", "xavierh@gmail.com", "9525551023", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Yelena Hickman", "yelenah@gmail.com", "9525551024", datetime.datetime.now(pytz.timezone('US/Central'))))
db.session.add(Customer("Zoe Hickman", "zoeh@gmail.com", "9525551025", datetime.datetime.now(pytz.timezone('US/Central'))))

# commit the changes
db.session.commit()

