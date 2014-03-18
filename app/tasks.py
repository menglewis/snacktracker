from datetime import datetime
from app import celery, db
from models import User, Goal, WeeklyGoal, Week

@celery.task()
def create_new_weeks():
    users = User.query.all()
    for user in users:
        try:
            if user.need_new_week:
                goals = user.goals
        except:
            pass
        if goals:
            week = Week(user_id=user.id, start_date=datetime.today())
            db.session.add(week)
            db.session.commit()
            for goal in goals:
                weekly_goal = WeeklyGoal(goal_type_id=goal.goal_type_id, week_id=week.id, goal_quantity=goal.quantity, actual_quantity=0)
                db.session.add(weekly_goal)
                db.session.commit()




