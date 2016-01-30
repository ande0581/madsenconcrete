__author__ = 'Jeff'
# to run the tests:
# (env) C:\Users\Jeff\PycharmProjects\madsenconcrete>nosetests --with-coverage --cover-erase --cover-package=project

import unittest
import datetime

import os
import pytz
from project import app, db
from project._config import basedir, USERNAME, PASSWORD

TEST_DB = 'test.db'


class AllTests(unittest.TestCase):

    ######################
    # setup and teardown #
    ######################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
        # app.config['SQLALCHEMY_ECHO'] = True
        self.app = app.test_client()
        db.create_all()

    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    ####################
    # Helper Functions #
    ####################

    def login(self, name, password):
        return self.app.post('/', data=dict(name=name, password=password), follow_redirects=True)

    def logout(self):
        return self.app.get('logout/', follow_redirects=True)

    def customer_add(self):
        return self.app.post('customer_add/', data=dict(name="Beta Company",
                                                        telephone="7635551000",
                                                        email="betacompany@domain.com"), follow_redirects=True)

    def customer_add_1(self):
        return self.app.post('customer_add/', data=dict(name="Alpha Company",
                                                        telephone="9525551000",
                                                        email="alphacompany@domain.com"), follow_redirects=True)

    def address_add(self):
        return self.app.post('address_add/1/', data=dict(street="1234 Ave NE", city="Hometown", state="MN",
                                                         zip="55400", customer_id=1), follow_redirects=True)

    def journal_add(self):
        return self.app.post('journal_add/1/', data=dict(body="This is my journal entry",
                                                         timestamp=datetime.datetime.now(pytz.timezone('US/Central')),
                                                         customer_id=1), follow_redirects=True)

    def service_add(self):
        return self.app.post('service_add/', data=dict(description="This is my service description",
                                                       cost=4.25), follow_redirects=True)

    def bid_add(self):
        return self.app.post('bid_add/1/1/', data=dict(description="This is my bid description",
                                                       notes=None,
                                                       timestamp=datetime.datetime.now(pytz.timezone('US/Central')),
                                                       customer_id=1,
                                                       address_id=1,
                                                       scheduled_bid_date="2016-05-01 09:30:00",
                                                       tentative_start=None,
                                                       actual_start=None,
                                                       completion_date=None,
                                                       down_payment_amount=None,
                                                       down_payment_date=None,
                                                       paid_in_full_amount=None,
                                                       paid_in_full_date=None,
                                                       status='Needs Bid'), follow_redirects=True)

    def item_add(self):
        return self.app.post('item_add/1/', data=dict(bid_id=1, service_id=1,
                                                      description="This is my service description", quantity=135,
                                                      cost=4.25, total=573.75), follow_redirects=True)

    def item_add_custom(self):
        return self.app.post('item_add_custom/1/', data=dict(bid_id=1,
                                                             description="This is my custom service description",
                                                             total=678.90), follow_redirects=True)


    #########################
    # Test Login and Logout #
    #########################

    def test_users_cannot_login_unless_registered(self):
        response = self.login('foo', 'bar')
        self.assertIn(b'Invalid username or password', response.data)

    def test_users_can_login(self):
        response = self.login(USERNAME, PASSWORD)
        self.assertIn(b'Welcome!', response.data)

    def test_logged_in_users_can_logout(self):
        self.login(USERNAME, PASSWORD)
        response = self.logout()
        self.assertIn(b'Goodbye!', response.data)

    ##########################
    # logged out cant access #
    ##########################

    def test_not_logged_in_cannot_access_logout(self):
        response = self.app.get('logout/', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    def test_not_logged_in_cannot_access_overview(self):
        response = self.app.get('overview/', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    def test_not_logged_in_cannot_access_customers(self):
        response = self.app.get('customers/', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    def test_not_logged_in_cannot_access_customer_details(self):
        response = self.app.get('customer_details/1/', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    def test_not_logged_in_cannot_access_customer_add(self):
        response = self.app.get('customer_add/', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    def test_not_logged_in_cannot_access_customer_edit(self):
        response = self.app.get('customer_edit/1/', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    def test_not_logged_in_cannot_access_customer_delete(self):
        response = self.app.get('customer_delete/1', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    def test_not_logged_in_cannot_access_address_add(self):
        response = self.app.get('address_add/1/', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    def test_not_logged_in_cannot_access_address_edit(self):
        response = self.app.get('address_edit/1/', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    def test_not_logged_in_cannot_access_address_delete(self):
        response = self.app.get('address_delete/1/', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    def test_not_logged_in_cannot_access_journal_add(self):
        response = self.app.get('journal_add/1/', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    def test_not_logged_in_cannot_access_journal_edit(self):
        response = self.app.get('journal_edit/1/', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    def test_not_logged_in_cannot_access_journal_delete(self):
        response = self.app.get('journal_delete/1/', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    def test_not_logged_in_cannot_access_bid_add(self):
        response = self.app.get('bid_add/1/1/', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    def test_not_logged_in_cannot_access_bid_edit(self):
        response = self.app.get('bid_edit/1/', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    def test_not_logged_in_cannot_access_bid_delete(self):
        response = self.app.get('bid_delete/1/', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    def test_not_logged_in_cannot_access_services(self):
        response = self.app.get('services/', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    def test_not_logged_in_cannot_access_service_add(self):
        response = self.app.get('service_add/', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    def test_not_logged_in_cannot_access_service_edit(self):
        response = self.app.get('service_edit/1/', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    def test_not_logged_in_cannot_access_service_delete(self):
        response = self.app.get('service_delete/1/', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    def test_not_logged_in_cannot_access_item_add(self):
        response = self.app.get('item_add/1/', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    def test_not_logged_in_cannot_access_item_edit(self):
        response = self.app.get('item_edit/1/', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    def test_not_logged_in_cannot_access_item_add_custom(self):
        response = self.app.get('item_add_custom/1/', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    def test_not_logged_in_cannot_access_item_edit_custom(self):
        response = self.app.get('item_edit_custom/1/', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    def test_not_logged_in_cannot_access_item_delete(self):
        response = self.app.get('item_delete/1/', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    def test_not_logged_in_cannot_access_customers_page(self):
        response = self.app.get('customers/page/', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    def test_not_logged_in_cannot_access_customers_page_1(self):
        response = self.app.get('customers/page/1/', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    def test_not_logged_in_cannot_access_calculator(self):
        response = self.app.get('calculator/', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    ################################
    # Logged in can add everything #
    ################################

    def test_logged_in_can_add_everything(self):
        response = self.login(USERNAME, PASSWORD)
        self.assertIn(b'Welcome!', response.data)

        response = self.customer_add()
        self.assertIn(b'New customer was successfully added', response.data)

        response = self.address_add()
        self.assertIn(b'New Address was successfully added', response.data)

        response = self.journal_add()
        self.assertIn(b'New journal entry was successfully added', response.data)

        response = self.service_add()
        self.assertIn(b'New service was successfully added', response.data)

        response = self.bid_add()
        self.assertIn(b'The bid was successfully added', response.data)

        response = self.item_add()
        self.assertIn(b'New item was successfully added', response.data)

        response = self.item_add_custom()
        self.assertIn(b'New custom item was successfully added', response.data)

    #################################
    # logged in can view everything #
    #################################

    def test_logged_in_can_view_overview(self):
        # create the database records
        self.test_logged_in_can_add_everything()
        response = self.app.get('overview/', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn(b'Jobs that Need a Bid', response.data)

    def test_logged_in_can_view_customers(self):
        # create the database records
        self.test_logged_in_can_add_everything()
        response = self.app.get('customers/', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn(b'Customers', response.data)

    def test_logged_in_can_view_customer_detail(self):
        # create the database records
        self.test_logged_in_can_add_everything()
        response = self.app.get('customer_details/1/', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn(b'Beta Company', response.data)

    def test_logged_in_can_view_customer_add(self):
        # create the database records
        self.test_logged_in_can_add_everything()
        response = self.app.get('customer_add/', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn(b'customer name', response.data)

    def test_logged_in_can_view_customer_edit(self):
        # create the database records
        self.test_logged_in_can_add_everything()
        response = self.app.get('customer_edit/1/', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn(b'Beta Company', response.data)

    def test_logged_in_can_view_address_add(self):
        # create the database records
        self.test_logged_in_can_add_everything()
        response = self.app.get('address_add/1/', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn(b'state abbreviation', response.data)

    def test_logged_in_can_view_address_edit(self):
        # create the database records
        self.test_logged_in_can_add_everything()
        response = self.app.get('address_edit/1/', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn(b'1234 AVE NE', response.data)

    def test_logged_in_can_view_journal_add(self):
        # create the database records
        self.test_logged_in_can_add_everything()
        response = self.app.get('journal_add/1/', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn(b'Journal Entry', response.data)

    def test_logged_in_can_view_journal_edit(self):
        # create the database records
        self.test_logged_in_can_add_everything()
        response = self.app.get('journal_edit/1/', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn(b'This is my journal entry', response.data)

    def test_logged_in_can_view_bid_add(self):
        # create the database records
        self.test_logged_in_can_add_everything()
        response = self.app.get('bid_add/1/1/', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn(b'Scheduled Bid Date', response.data)

    def test_logged_in_can_view_bid_edit(self):
        # create the database records
        self.test_logged_in_can_add_everything()
        response = self.app.get('bid_edit/1/', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn(b'This is my bid description', response.data)
        self.assertIn(b'135', response.data)
        self.assertIn(b'4.25', response.data)
        self.assertIn(b'573.75', response.data)

    def test_logged_in_can_view_services(self):
        # create the database records
        self.test_logged_in_can_add_everything()
        response = self.app.get('services/', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn(b'This is my service description', response.data)

    def test_logged_in_can_view_service_add(self):
        # create the database records
        self.test_logged_in_can_add_everything()
        response = self.app.get('service_add/', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn(b'service description', response.data)

    def test_logged_in_can_view_service_edit(self):
        # create the database records
        self.test_logged_in_can_add_everything()
        response = self.app.get('service_edit/1/', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn(b'This is my service description', response.data)

    def test_logged_in_can_view_item_add(self):
        # create the database records
        self.test_logged_in_can_add_everything()
        response = self.app.get('item_add/1/', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn(b'Add Item to Bid', response.data)

    def test_logged_in_can_view_item_edit(self):
        # create the database records
        self.test_logged_in_can_add_everything()
        response = self.app.get('item_edit/1/', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn(b'This is my service description', response.data)

    def test_logged_in_can_view_item_add_custom(self):
        # create the database records
        self.test_logged_in_can_add_everything()
        response = self.app.get('item_add_custom/2/', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn(b'Add Custom Item to Bid', response.data)

    def test_logged_in_can_view_item_edit_custom(self):
        # create the database records
        self.test_logged_in_can_add_everything()
        response = self.app.get('item_edit_custom/2/', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn(b'This is my custom service description', response.data)

    def test_logged_in_can_view_customer_pagination(self):
        # can view customer's pagination page
        self.test_logged_in_can_add_everything()
        response = self.app.get('customers/page/1/', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn(b'Beta Company', response.data)

    def test_logged_in_can_view_calculator(self):
        # can view calculator page
        self.test_logged_in_can_add_everything()
        response = self.app.get('calculator', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn(b'Calculate Slab, Square Footings, or Walls', response.data)

    ###################################
    # logged in can delete everything #
    ###################################

    def test_logged_in_can_delete_customer(self):
        # create the database records
        self.test_logged_in_can_add_everything()
        # this needs to recursive delete database items...
        response = self.app.get('customer_delete/1', follow_redirects=True)
        self.assertIn(b'The customer was deleted', response.data)

    def test_logged_in_can_delete_address(self):
        # create the database records
        self.test_logged_in_can_add_everything()
        response = self.app.get('address_delete/1/', follow_redirects=True)
        self.assertIn(b'The address was deleted', response.data)

    def test_logged_in_can_delete_journal(self):
        # create the database records
        self.test_logged_in_can_add_everything()
        response = self.app.get('journal_delete/1/', follow_redirects=True)
        self.assertIn(b'The journal entry was deleted', response.data)

    def test_logged_in_can_delete_bid(self):
        # create the database records
        self.test_logged_in_can_add_everything()
        response = self.app.get('bid_delete/1/', follow_redirects=True)
        self.assertIn(b'The bid was deleted', response.data)

    def test_logged_in_can_delete_service(self):
        # create the database records
        self.test_logged_in_can_add_everything()
        response = self.app.get('service_delete/1/', follow_redirects=True)
        self.assertIn(b'The service was deleted', response.data)

    def test_logged_in_can_delete_item(self):
        # create the database records
        self.test_logged_in_can_add_everything()
        response = self.app.get('item_delete/1/', follow_redirects=True)
        self.assertIn(b'The item was deleted', response.data)

    def test_logged_in_can_delete_item_custom(self):
        # create the database records
        self.test_logged_in_can_add_everything()
        response = self.app.get('item_delete/2/', follow_redirects=True)
        self.assertIn(b'The item was deleted', response.data)

    ####################################
    # Test Form Validations For Adding #
    ####################################

    def test_form_is_present_on_login_page(self):
        response = self.app.get('/')
        self.assertEquals(response.status_code, 200)
        self.assertIn(b'Please sign in', response.data)

    def test_form_LoginForm_add(self):
        # Password is missing
        response = self.app.post('/', data=dict(name="mytestuser", password=""), follow_redirects=True)
        self.assertIn('This field is required', response.data)

    def test_form_AddCustomerForm_add(self):
        self.login(USERNAME, PASSWORD)
        # Telephone should not have dashes
        response = self.app.post('customer_add/', data=dict(name="mytestuser", email="mytestuser@domain.com",
                                                            telephone="612-555-1234"), follow_redirects=True)
        self.assertIn('Field must be between 10 and 10 characters long', response.data)

    def test_form_AddAddressForm_add(self):
        self.login(USERNAME, PASSWORD)
        # State format should be two characters
        response = self.app.post('address_add/1/', data=dict(street="300 Ave S", city="MyCity",
                                                             state="Minn", zip="55441"), follow_redirects=True)
        self.assertIn('Field must be between 2 and 2 characters long', response.data)

    def test_form_AddJournalForm_add(self):
        self.login(USERNAME, PASSWORD)
        # Journal is empty
        response = self.app.post('journal_add/1/', data=dict(body=""), follow_redirects=True)
        self.assertIn('This field is required', response.data)

    def test_form_AddBidForm_add(self):
        self.login(USERNAME, PASSWORD)
        self.test_logged_in_can_add_everything()
        # Bid date format is wrong
        response = self.app.post('bid_add/1/1/', data=dict(description="This is my bid description",
                                                           scheduled_bid_date="2016-02-1"), follow_redirects=True)
        self.assertIn('Not a valid datetime value', response.data)

    def test_form_EditBidForm_add(self):
        self.login(USERNAME, PASSWORD)
        self.test_logged_in_can_add_everything()
        # No description
        response = self.app.post('bid_edit/1/', data=dict(description="",
                                                          status="Needs Bid",
                                                          scheduled_bid_date="2016-01-02 09:30:30",
                                                          tentative_bid_date="2016-05-01",
                                                          actual_start="2016-05-01",
                                                          completion_date="2016-05-05"), follow_redirects=True)
        self.assertIn('This field is required', response.data)

    def test_form_AddServiceForm_add(self):
        self.login(USERNAME, PASSWORD)
        # No cost per unit
        response = self.app.post('service_add/', data=dict(description="My Description", cost=""),
                                 follow_redirects=True)
        self.assertIn('This field is required', response.data)

    def test_form_AddBidItemForm_add(self):
        self.login(USERNAME, PASSWORD)
        # Quantity a string not a float
        response = self.app.post('item_add/1/', data=dict(quantity="1.5", serrvice_id="1"), follow_redirects=True)
        self.assertIn('This field is required', response.data)

    def test_form_AddBidCustomItemForm_add(self):
        self.login(USERNAME, PASSWORD)
        # Quantity a string not a float
        response = self.app.post('item_add_custom/1/', data=dict(description="My custom item description",
                                                                 total="FiveHundred"), follow_redirects=True)
        self.assertIn('Not a valid float value', response.data)

    ###################
    # Test Pagination #
    ###################

    def test_pagination_of_customer_list_with_search_string(self):
        self.login(USERNAME, PASSWORD)
        self.test_logged_in_can_add_everything()
        self.customer_add_1()
        # Have two customers, searching for one make sure one exists and the other doesn't
        response = self.app.post('customers/', data=dict(name="beta"), follow_redirects=True)
        self.assertIn('Beta Company', response.data)
        self.assertNotIn('Alpha Company', response.data)

    def test_pagination_of_customer_list_without_search_string(self):
        self.login(USERNAME, PASSWORD)
        self.test_logged_in_can_add_everything()
        self.customer_add_1()
        response = self.app.post('customers/', data=dict(name=""), follow_redirects=True)
        self.assertIn('Beta Company', response.data)
        self.assertIn('Alpha Company', response.data)

    ######################################
    # Test Good Form Validations on Edit #
    ######################################

    def test_form_AddCustomerForm_edit(self):
        self.login(USERNAME, PASSWORD)
        self.test_logged_in_can_add_everything()
        response = self.app.post('customer_edit/1/', data=dict(name="mytestuser", email="mytestuser@domain.com",
                                                            telephone="6125551234"), follow_redirects=True)
        self.assertIn('Customer was successfully edited', response.data)

    def test_form_AddAddressForm_edit(self):
        self.login(USERNAME, PASSWORD)
        self.test_logged_in_can_add_everything()
        response = self.app.post('address_edit/1/', data=dict(street="300 Ave S", city="MyCity",
                                                              state="MN", zip="55441"), follow_redirects=True)
        self.assertIn('Address was successfully edited', response.data)

    def test_form_AddJournalForm_edit(self):
        self.login(USERNAME, PASSWORD)
        self.test_logged_in_can_add_everything()
        response = self.app.post('journal_edit/1/', data=dict(body="My Journal Entry"), follow_redirects=True)
        self.assertIn('Journal was successfully edited', response.data)

    def test_form_EditBidForm_edit(self):
        self.login(USERNAME, PASSWORD)
        self.test_logged_in_can_add_everything()
        response = self.app.post('bid_edit/1/', data=dict(description="My Bid Description",
                                                          status="Needs Bid",
                                                          scheduled_bid_date="2016-01-02 16:00:00",
                                                          tentative_bid_date="2016-05-01",
                                                          actual_start="2016-05-01",
                                                          completion_date="2016-05-05",
                                                          down_payment_date_amount=500,
                                                          down_payment_date="2016-05-31",
                                                          paid_in_full_amount=3730.50,
                                                          paid_in_full_date="2016-06-10"), follow_redirects=True)
        self.assertIn('Bid was successfully edited', response.data)

    def test_form_AddServiceForm_edit(self):
        self.login(USERNAME, PASSWORD)
        self.test_logged_in_can_add_everything()
        response = self.app.post('service_edit/1/', data=dict(description="My Description", cost="4"),
                                 follow_redirects=True)
        self.assertIn('Service was successfully edited', response.data)

    def test_form_AddBidItemForm_edit(self):
        self.login(USERNAME, PASSWORD)
        self.test_logged_in_can_add_everything()
        # Service Cost is 4.25. Want to make sure on edit the total value is still good (62.5 * 4.25 = 265.62)
        response = self.app.post('item_edit/1/', data=dict(quantity=62.5, serrvice_id="1"), follow_redirects=True)
        self.assertIn('265.62', response.data)

    def test_form_AddCustomBidItemForm_edit(self):
        self.login(USERNAME, PASSWORD)
        self.test_logged_in_can_add_everything()
        # Change total from 678.90 to 456.78
        response = self.app.post('item_edit_custom/2/', data=dict(total=456.78), follow_redirects=True)
        self.assertIn('456.78', response.data)

    #########################
    # Test Math On Bid Page #
    #########################

    def test_sum_items_on_bid(self):
        self.login(USERNAME, PASSWORD)
        self.test_logged_in_can_add_everything()
        response = self.app.get('bid_edit/1/', follow_redirects=True)
        # The total for one regular item (573.75) and one custom item (678.90) should be 1252.65
        self.assertIn(b'1252.65', response.data)
        self.item_add()  # add another standard item 573.75
        response = self.app.get('bid_edit/1/', follow_redirects=True)
        # The total for three rows should be (2 standard items, one customer item) 1826.40
        self.assertIn(b'1826.40', response.data)

    def test_sum_items_on_bid_with_edit(self):
        self.login(USERNAME, PASSWORD)
        self.test_logged_in_can_add_everything()
        response = self.app.get('bid_edit/1/', follow_redirects=True)
        # The total for one regular item (573.75) and one custom item (678.90) should be 1252.65
        self.assertIn(b'1252.65', response.data)
        self.item_add()  # add another standard item 573.75
        response = self.app.get('bid_edit/1/', follow_redirects=True)
        # The total for three rows should be (2 standard items, one customer item) 1826.40
        self.assertIn(b'1826.40', response.data)
        response = self.app.post('item_edit/1/', data=dict(quantity=62, service_id="1"), follow_redirects=True)
        # The new total is (edited item1 62*4.25 = 263.5) + (item2 573.75) + (custom item3 678.90) = 1516.15
        self.assertIn(b'1516.15', response.data)

    def test_sum_items_on_bid_with_edit_custom_item(self):
        self.login(USERNAME, PASSWORD)
        self.test_logged_in_can_add_everything()
        response = self.app.get('bid_edit/1/', follow_redirects=True)
        # The total for one regular item (573.75) and one custom item (678.90) should be 1252.65
        self.assertIn(b'1252.65', response.data)
        self.item_add()  # add another standard item 573.75
        response = self.app.get('bid_edit/1/', follow_redirects=True)
        # The total for three rows should be (2 standard items, one customer item) 1826.40
        self.assertIn(b'1826.40', response.data)
        response = self.app.post('item_edit_custom/2/', data=dict(description="my customer item edit", total=500),
                                 follow_redirects=True)
        # The new total is (item1 573.75) + (item2 573.75) + (custom item3 500) = 1647.50
        self.assertIn(b'1647.50', response.data)

    def test_remaining_balance_on_bid_no_down_payment(self):
        self.login(USERNAME, PASSWORD)
        self.test_logged_in_can_add_everything()
        response = self.app.get('bid_edit/1/', follow_redirects=True)
        # The total for one regular item (573.75) and one custom item (678.90) should be 1252.65
        self.assertIn(b'<td style="color: red">$1252.65</td>', response.data)

    # When I edit the bid I need to put all the values back on my POST. I got tripped up on this.
    # It doesn't edit just the ones i posted it over-wrote all the ones I didn't post causing form validation to fail
    def test_remaining_balance_on_bid_with_down_payment(self):
        self.login(USERNAME, PASSWORD)
        self.test_logged_in_can_add_everything()
        # The total for one regular item (573.75) and one custom item (678.90) should be 1252.65
        # Down payment of 777.77 dollars (1252.65-777.77=474.88)
        response = self.app.post('bid_edit/1/', data=dict(notes="these are my bid notes",
                                                          description="this is my edited description",
                                                          down_payment_amount=777.77,
                                                          down_payment_date="2016-07-01"), follow_redirects=True)
        self.assertIn(b'<td style="color: red">$474.88</td>', response.data)

    def test_remaining_balance_on_bid_when_paid_in_full(self):
        self.login(USERNAME, PASSWORD)
        self.test_logged_in_can_add_everything()
        # The total for one regular item (573.75) and one custom item (678.90) should be 1252.65
        # Test that paid in full amount subtracted from bid total equals a remaining balance of 0.00
        response = self.app.post('bid_edit/1/', data=dict(notes="these are my bid notes",
                                                          description="this is my edited description",
                                                          down_payment_amount=777.77,
                                                          down_payment_date="2016-07-01",
                                                          paid_in_full_amount=1252.65,
                                                          paid_in_full_date="2016-07-15"), follow_redirects=True)
        self.assertIn(b'<td style="color: red">$0.00</td>', response.data)


if __name__ == "__main__":
    unittest.main()
