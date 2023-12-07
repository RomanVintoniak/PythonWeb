from flask import url_for
from flask_login import current_user
from app.authentication.models import User
from app.post.models import Post
from app import db



def test_get_all_posts(init_database):
    number_of_todos = Post.query.count()
    assert number_of_todos == 2



"""

def test_create_new_post(client, init_database):
    response = client.post(
        url_for('post.create'),
        data=dict(
            title = 'This is my first post',
            text = 'text text text text',
            image = 'test.jpg',
            userID = 1,
            postType = 'Publication',
        ),
        follow_redirects=True
    )
    
    post = Post.query.filter_by(title='This is my first post').first()
    
    #print(response.data)
    
    assert post
    assert post.title == 'This is my first post'
    assert response.status_code == 200
    assert b'Created new post' in response.data
    
"""
    

def test_delete_post(client, init_database):
    response = client.get(
        url_for('post.delete', id=1),
        follow_redirects=True
    )
    
    post = Post.query.filter_by(id=1).first()
    
    assert response.status_code == 200
    assert post is None
    assert b'Post has been deleted' in response.data
