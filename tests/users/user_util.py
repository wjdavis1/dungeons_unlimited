from app import db
from app.models.auth.user import User


class UserTestUtility(object):

    def __init__(self, db):
        self.db = db


    def create_user(self, username='', first_name='', last_name='',email=''):

        user = User(username=username,first_name=first_name,
                    last_name=last_name, email=email)
        user.set_password('test_password')
        db.session.add(user)
        db.session.commit()

    def remove_user(self, username):

        user = User.query.filter_by(username=username).first()

        if user is not None:
            db.session.remove(user)
            db.session.commit()
