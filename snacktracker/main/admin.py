from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView
from .models import User, Goal, GoalType, Week, WeeklyGoal
from snacktracker import db, admin

class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/myindex.html')

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(GoalType, db.session))
admin.add_view(ModelView(Goal, db.session))
admin.add_view(ModelView(WeeklyGoal, db.session))
admin.add_view(ModelView(Week, db.session))
