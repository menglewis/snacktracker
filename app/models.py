from datetime import date, datetime, timedelta
from flask.ext.login import UserMixin

from app import db, bcrypt

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True)
    password = db.Column(db.String, nullable=False)
    goals = db.relationship('Goal', backref='user', lazy='dynamic')
    weeks = db.relationship('Week', backref='user', lazy='dynamic')

    def __init__(self, username=None, password=None):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @property
    def last_week(self):
        if len(self.weeks.all()) > 0:
            return self.weeks[-1]
        return None

    def need_new_week(self):
        last_week = self.last_week
        if last_week is None or last_week.end_date < date.today():
            return True
        return False

class GoalType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    
    def __repr__(self):
        return '<GoalType {}>'.format(self.name)

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goal_type_id = db.Column(db.Integer, db.ForeignKey('goal_type.id'))
    goal_type = db.relationship('GoalType', backref='goal')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    quantity = db.Column(db.Integer)

    def __repr__(self):
        return '<Goal {0} {1}>'.format(self.user.username, self.goal_type.name)

class WeeklyGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goal_type_id = db.Column(db.Integer, db.ForeignKey('goal_type.id'))
    goal_type = db.relationship('GoalType', backref='weekly_goal')
    week_id = db.Column(db.Integer, db.ForeignKey('week.id'))
    goal_quantity = db.Column(db.Integer)
    actual_quantity = db.Column(db.Integer)

    def __repr__(self):
        return '<WeeklyGoal {0} {1} >'.format(self.goal_type.name, self.goal_quantity)

    @property
    def remaining(self):
        return self.goal_quantity - self.actual_quantity


class Week(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    start_date = db.Column(db.DateTime)
    goals = db.relationship('WeeklyGoal', backref='week', lazy='dynamic')

    @property
    def end_date(self):
        return self.start_date + timedelta(days=6)

    @property
    def date_range(self):
        return "%s - %s" % (datetime.strftime(self.start_date, '%m/%d/%Y'),
            datetime.strftime(self.end_date, '%m/%d/%Y'))

    def __repr__(self):
        return '<Week %s>' % (self.start_date)

