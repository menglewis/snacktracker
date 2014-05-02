# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, flash, request
from flask.ext.login import login_user, logout_user, login_required
from .. import db, login_manager
from . import auth
from .forms import LoginForm, RegisterForm, flash_form_errors
from .models import User

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user, form.remember_me.data)
            flash("You are logged in.", "success")
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash_form_errors(form)
    return render_template('auth/login.html', form=form)

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')

    return redirect(url_for('auth.login'))

@auth.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(username=form.username.data,
                password=form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Thank you for registering.', 'success')
            login_user(new_user)
            return redirect(url_for('main.index'))
        else:
            flash_form_errors(form)
    return render_template('auth/register.html', form=form)
