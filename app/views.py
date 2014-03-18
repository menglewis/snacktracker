from flask import jsonify, render_template, request, flash, redirect, url_for
from flask.ext.login import login_user, logout_user, login_required, current_user
from flask.ext.admin import Admin, BaseView, expose
from app import app, db, login_manager, admin
from models import User, Goal, GoalType, Week, WeeklyGoal
from forms import LoginForm, RegisterForm

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
            password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Thank you for registering.", 'success')
        login_user(new_user)
        return redirect(url_for('index'))
    else:
        flash_errors(form)
    return render_template('register.html', form=form)

@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash("You are logged in.", 'success')
            return redirect(url_for("index"))
        else:
            flash_errors(form)
    return render_template("login.html", form=form)

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/increment/', methods=["GET"])
@login_required
def increment_goal():
    goal_id = request.args.get('id')
    goal = WeeklyGoal.query.get(goal_id)
    goal.actual_quantity += 1
    db.session.add(goal)
    db.session.commit()
    return jsonify({'id': goal_id, 'quantity': goal.actual_quantity})

@app.route('/decrement/', methods=["GET"])
@login_required
def decrement_goal():
    goal_id = request.args.get('id')
    goal = WeeklyGoal.query.get(goal_id)
    goal.actual_quantity += -1
    db.session.add(goal)
    db.session.commit()
    return jsonify({'id': goal_id, 'quantity': goal.actual_quantity})


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}"
                    .format(getattr(form, field).label.text, error), category)

