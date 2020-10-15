import jwt
from app import db, login
from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from time import time
from werkzeug.security import generate_password_hash, check_password_hash


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


user_campaigns = db.Table(
    'user_campaigns',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('campaign_id', db.Integer, db.ForeignKey('campaigns.id')))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(128))
    campaigns = db.relationship(
        'Campaigns',
        secondary=user_campaigns,
        backref='users', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, 'sha256', 8)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add_to_campaign(self, campaign):
        if not self.is_in_campaign(campaign):
            self.campaigns.append(campaign)

    def remove_from_campaign(self, campaign):
        if self.is_in_campaign(campaign):
            self.campaigns.remove(campaign)

    def is_in_campaign(self, campaign):
        return self.campaigns.filter(
            user_campaigns.c.user_id == self.id and
            user_campaigns.c.campaign_id == campaign.id
        ).count() > 0

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        ).decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(
                token, current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )['reset_password']
        except:
            return
        return User.query.get(id)


class Campaigns(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_name = db.Column(db.String(150), index=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_dungeon_master = db.Column(db.Boolean(), index=False, default=False)

    def __repr__(self):
        return '<Campaign {}>'.format(self.campaign_name)
