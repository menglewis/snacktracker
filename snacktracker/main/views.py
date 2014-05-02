# -*- coding: utf-8 -*-
from flask import render_template, jsonify, request
from flask.ext.login import login_required
from .. import db
from . import main
from .models import WeeklyGoal

@main.route('/', methods=['GET'])
@login_required
def index():
    return render_template('main/index.html')

@main.route('/increment/', methods=["GET"])
@login_required
def increment_goal():
    goal_id = request.args.get('id')
    goal = WeeklyGoal.query.get(goal_id)
    goal.actual_quantity += 1
    db.session.add(goal)
    db.session.commit()
    return jsonify({'id': goal_id, 'quantity': goal.actual_quantity})

@main.route('/decrement/', methods=["GET"])
@login_required
def decrement_goal():
    goal_id = request.args.get('id')
    goal = WeeklyGoal.query.get(goal_id)
    goal.actual_quantity += -1
    db.session.add(goal)
    db.session.commit()
    return jsonify({'id': goal_id, 'quantity': goal.actual_quantity})
