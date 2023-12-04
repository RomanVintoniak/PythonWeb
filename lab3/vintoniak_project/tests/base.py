from flask_testing import TestCase
from app import create_app
from app import db
from app.authentication.models import User


class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app = create_app('test')
        return app

    def setUp(self):
        db.create_all()
        user = User(username='user', email='user@gmail.com', password='password')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()