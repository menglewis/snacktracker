from datetime import datetime
from flask.ext.login import UserMixin
from .. import db, bcrypt

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username=None, password=None):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %s>' % self.username

    @property
    def last_week(self):
        if len(self.weeks) > 0:
            return self.weeks[-1]
        return None

    def need_new_week(self):
        last_week = self.last_week
        if last_week is None or last_week.end_date < datetime.today():
            return True
        return False
