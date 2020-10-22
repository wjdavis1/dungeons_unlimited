import unittest
import os
import base64
from config import Config
from app import create_app, db
from app.models.auth.user import User, Campaigns
from tests.users.user_util import UserTestUtility

dir_path = os.path.dirname(os.path.realpath(__file__))
image_path = os.path.join(dir_path, '../test_resources/image.jpeg')

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.user_utility = UserTestUtility(db)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password(self):

        user = User(username='wjdude')
        user.set_password('testpassword')
        self.assertFalse(user.check_password('master'))
        self.assertTrue(user.check_password('testpassword'))

    def test_user_creation(self):

        test_username = 'testington'

        self.user_utility.create_user(test_username)

        test_user = User.query.filter_by(username='bobFord').first()
        self.assertIsNone(test_user)

        actual_user = User.query.filter_by(username=test_username).first()
        self.assertIsNotNone(actual_user)

    def test_campaign_creation(self):

        test_campaignname = "test slayer 3"
        self.user_utility.create_campaign(test_campaignname)

        test_camp = Campaigns.query.filter_by(campaign_name='a campaign').first()

        self.assertIsNone(test_camp)

        actual_camp = Campaigns.query.filter_by(campaign_name=test_campaignname).first()
        self.assertIsNotNone(actual_camp)

    def test_user_in_campaign(self):
        user = self.user_utility.create_user('Campaign Master')
        campaign = self.user_utility.create_campaign('Trials of the Demon King')

        self.user_utility.add_user_to_campaign(user, campaign)

        self.assertTrue(user.campaigns.count() > 0)

    def test_import_user_profile_image(self):
        with open(image_path, 'rb') as image:
            encode_image = base64.b64encode(image.read())
            self.assertIsNotNone(encode_image)
