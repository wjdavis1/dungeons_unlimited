import unittest
import os
from config import Config, basedir
from app import create_app, db
from app.models.auth.user import User, Campaigns
from tests.users.user_util import UserTestUtility


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
class UserTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
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

        test_username='testington'

        user_utility = UserTestUtility(db)
        user_utility.create_user(test_username)

        test_user = User.query.filter_by(username='bobFord').first()
        self.assertIsNone(test_user)

        actual_user = User.query.filter_by(username=test_username).first()
        self.assertIsNotNone(actual_user)
