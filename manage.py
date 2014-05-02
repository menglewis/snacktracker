#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
try:
   input = raw_input
except NameError:
   pass

from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand

from snacktracker import create_app, db
from snacktracker.auth.models import User
from snacktracker.settings import DevConfig, ProdConfig

if os.environ.get("SNACKTRACKER_ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)

manager = Manager(app)

def _make_context():
    '''Return context dict for a shell session so you can access
    app, db, and the User model by default.
    '''
    return {'app': app, 'db': db, 'User': User}

@manager.command
def test():
    subprocess.call(['nosetests', '-v'])

@manager.command
def createdb():
    with app.app_context():
        db.create_all()

@manager.command
def createuser():
    """Register a new user"""
    username = input("Username: ")
    from getpass import getpass
    password = getpass()
    password2 = getpass(prompt='Confirm: ')
    if password != password2:
        import sys
        sys.exit('Error: passwords do not match')
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    print('User {0} was registered!'.format(username))

manager.add_command("runserver", Server())
manager.add_command("shell", Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()