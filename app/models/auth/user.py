from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


user_campaigns = db.Table('user_campaigns',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('campaign_id', db.Integer, db.ForeignKey('campaigns.id')))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password,'sha256',8)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Campaigns(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_name = db.Column(db.String(150), index=True)
    is_dungeon_master = db.Column(db.Boolean(), index=False, default=False)
