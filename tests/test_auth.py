import unittest

from snacktracker import create_app, db
from snacktracker.settings import TestingConfig
from snacktracker.auth.models import User
from snacktracker.auth.views import load_user
from snacktracker.auth.forms import RegisterForm, LoginForm

class UserModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        user = User('test', 'password')
        self.assertTrue(user.password is not None)
        self.assertTrue(user.password != 'password')

    def test_password_verification(self):
        user = User('test', 'password')
        self.assertTrue(user.check_password('password'))
        self.assertFalse(user.check_password('paas'))

    def test_password_salts(self):
        user = User('test', 'password')
        user2 = User('test2', 'password')
        self.assertTrue(user.password != user2.password)

    def test_user_loader(self):
        user = User('test', 'password')
        db.session.add(user)
        db.session.commit()
        self.assertTrue(load_user(user.id) == user)

class RegisterFormTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.request_context = self.app.test_request_context()
        self.request_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.request_context.pop()
        self.app_context.pop()

    def test_passwords_not_match(self):
        form = RegisterForm(username='test', password='password', confirm='password2')
        self.assertFalse(form.validate())

    def test_username_already_registered(self):
        user = User(username='test', password='password')
        db.session.add(user)
        db.session.commit()

        form = RegisterForm(username='test', password='password', confirm='password')
        self.assertFalse(form.validate())
        self.assertIn("Username already registered", form.username.errors)

    def test_username_required(self):
        form = RegisterForm(password='password', confirm='password')
        self.assertFalse(form.validate())
        self.assertIn('username', form.errors)

    def test_password_required(self):
        form = RegisterForm(username='test', confirm='password')
        self.assertFalse(form.validate())
        self.assertIn('password', form.errors)

    def test_confirm_required(self):
        form = RegisterForm(username='test', password='password')
        self.assertFalse(form.validate())
        self.assertIn('confirm', form.errors)

    def test_validation_success(self):
        form = RegisterForm(username='test', password='password', confirm='password')
        self.assertTrue(form.validate())

class LoginFormTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.request_context = self.app.test_request_context()
        self.request_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.request_context.pop()
        self.app_context.pop()

    def test_username_required(self):
        form = LoginForm(password='password')
        self.assertFalse(form.validate())
        self.assertIn('username', form.errors)

    def test_password_required(self):
        form = LoginForm(username='test')
        self.assertFalse(form.validate())
        self.assertIn('password', form.errors)

    def test_validation_success(self):
        user = User(username='test', password='password')
        db.session.add(user)
        db.session.commit()
        form = LoginForm(username='test', password='password')
        self.assertTrue(form.validate())

    def test_wrong_username(self):
        user = User(username='test', password='password')
        db.session.add(user)
        db.session.commit()
        form = LoginForm(username='test2', password='password')
        self.assertFalse(form.validate())

    def test_wrong_password(self):
        user = User(username='test', password='password')
        db.session.add(user)
        db.session.commit()
        form = LoginForm(username='test', password='password2')
        self.assertFalse(form.validate())
