from flask import url_for
from flask_login import current_user
from app.authentication.models import User
from app import db


def test_register_user(client):
    response = client.post(
        url_for('auth.registration'),
        data=dict(
            username='michael',
            email='michael@realpython.com',
            password='123456',
            confirmPassword='123456'
        ),
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'Account created' in response.data


def test_login_user(client):
    response = client.post(
        url_for('auth.login', external=True),
        data=dict(
            email='michael@realpython.com',
            password='123456',
            rememberMe = True
        ),
        follow_redirects=True
    )
    assert response.status_code == 200
    assert current_user.is_authenticated == True
    assert b"Login Succesful" in response.data


def test_login_user_with_fixture(log_in_default_user):
    assert current_user.is_authenticated == True
    

def test_log_out_user(client, log_in_default_user):
    response = client.get(
        url_for('auth.logout'),
        follow_redirects = True
    )
    
    assert b'You are logged out', response.data
    assert response.status_code == 200
    assert current_user.is_authenticated == False