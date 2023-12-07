from flask import url_for
import pytest
from app import create_app, db
from app.authentication.models import User
from app.post.models import Post

@pytest.fixture(scope='module')
def client():
    app = create_app('test')
    app.config['SERVER_NAME'] = '127.0.0.1:5000'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

@pytest.fixture()
def user_test():
    user = User(username='brand_new', email='brand_new@example.com', password='password')
    return user

@pytest.fixture(scope='module')
def init_database(client):
    # Insert user data
    default_user = User(username='patkennedy', email='patkennedy24@gmail.com', password='FlaskIsAwesome')
    post_1 = Post(title="Um consequatur volupta", text='Qui deleniti voluptas', user_id=1)
    post_2 = Post(title="Optio eum rerum", text='Cumque qui omnis voluptatem.', user_id=1)
    db.session.add(default_user)
    db.session.add(post_1)
    db.session.add(post_2)

    # Commit the changes for the users
    db.session.commit()

    yield  # this is where the testing happens!

@pytest.fixture(scope='function')
def log_in_default_user(client):
    client.post(url_for('auth.login'),
                     data=dict(email='user@gmail.com', password='password', rememberMe=True),
                     follow_redirects=True
                     )

    yield  # this is where the testing happens!

    client.get(url_for('auth.logout'))