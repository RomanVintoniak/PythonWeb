import urllib
import urllib3
import unittest
from flask import Flask, url_for
from flask_login import current_user
from flask_testing import TestCase
from app import create_app
from urllib.request import urlopen
from app import db
from app.authentication.models import User
from app.todo.models import Todo
from .base import BaseTestCase


class SetupTest(BaseTestCase):

    def test_setup(self):
        self.assertTrue(self.app is not None)
        self.assertTrue(self.client is not None)
        self.assertTrue(self._ctx is not None)
    

class PortfolioViewsTests(BaseTestCase):
    
    def test_home_page_loads(self):
        """
        GIVEN url to home page
        WHEN the '/home' page is requested (GET)
        THEN check that status code is 200 and response data contains 'Roman Vintoniak'
        """
        
        with self.client:
            response = self.client.get(url_for('portfolio.home'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Roman Vintoniak', response.data)
            
            
    def test_skills_page_loads(self):
        """
        GIVEN url to skills page
        WHEN the '/skills' page is requested (GET)
        THEN check that status code is 200 and response data contains 'My skills'
        """
        
        with self.client:
            response = self.client.get(url_for('portfolio.skills'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'My skills', response.data)
    
    
    def test_certificates_page_loads(self):
        """
        GIVEN url to certificates page
        WHEN the '/certificates' page is requested (GET)
        THEN check that status code is 200 and response data contains 'My certificates'
        """
        
        with self.client:
            response = self.client.get(url_for('portfolio.certificates'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'My certificates', response.data)
        

class AuthViewsTests(BaseTestCase):
    
    def test_login_page_loads(self):
        """
        GIVEN url to login page
        WHEN the '/login' page is requested (GET)
        THEN check that status code is 200 and response data contains 'Login'
        """
        
        with self.client:
            response = self.client.get(url_for('auth.login'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Login', response.data)
    
    
    def test_registration_page_loads(self):
        """
        GIVEN url to registration page
        WHEN the '/registration' page is requested (GET)
        THEN check that status code is 200 and response data contains 'Registration'
        """
        
        with self.client:
            response = self.client.get(url_for('auth.registration'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Registration', response.data)


class AuthTests(BaseTestCase):
    
    def test_register_user_post(self):
        """
        GIVEN user data
        WHEN the register form is submitted (POST)
        THEN check that status code is 200, response data contains 'Account created' 
            and registered user exist in DB with correct data (email)
        """
        
        with self.client:
            respons = self.client.post(
                '/registration',
                data=dict(username='test', email='test@gmail.com', password='password', confirmPassword='password'),
                follow_redirects=True
            )
            
            self.assertIn(b'Account created', respons.data)
            user = User.query.filter_by(email='test@gmail.com').first()
            assert respons.status_code == 200
            assert user is not None
            assert user.email == 'test@gmail.com'
    
    
    def test_login_user_without_remember_me(self):
        """
        GIVEN user data
        WHEN the user logged in without checked rememberMe field (POST)
        THEN check that status code is 200, response data contains 'Login Succesful to home'
            and current_user is_authenticated
        """
        
        with self.client:
            response = self.client.post(
                url_for('auth.login'),
                data=dict(email='user@gmail.com', password='password'),
                follow_redirects=True
            )
            
            self.assertIn(b'Login Succesful to home', response.data)
            assert response.status_code == 200
            assert current_user.is_authenticated == True
            

    def test_login_user_with_remember_me(self):
        """
        GIVEN user data
        WHEN the user logged in with checked rememberMe field (POST)
        THEN check that status code is 200, response data contains 'Login Succesful'
            and current_user is_authenticated
        """
        
        with self.client:
            response = self.client.post(
                url_for('auth.login'),
                data=dict(email='user@gmail.com', password='password', rememberMe=True),
                follow_redirects=True
            )
            
            self.assertIn(b'Login Succesful', response.data)
            assert response.status_code == 200
            assert current_user.is_authenticated == True


    def test_logout_user(self):
        """
        GIVEN user data
        WHEN the user is logged in and he logged out (POST)
        THEN check that status code is 200, response data contains 'You are logged out'
            and current_user is NOT authenticated
        """
        
        with self.client:
            self.client.post(
                url_for('auth.login'),
                data=dict(email='user@gmail.com', password='password'),
                follow_redirects = True
            )
            
            response = self.client.get(
                url_for('auth.logout'),
                follow_redirects = True
            )
            
            self.assertIn(b'You are logged out', response.data)
            assert response.status_code == 200
            assert current_user.is_authenticated == False


class TodoTests(BaseTestCase):
    
    def test_todo_create(self):
        """
        GIVEN todo data
        WHEN the todo created (POST)
        THEN check that status code is 200 and created todo exist in DB and stored corectly
        """
        
        data = {
            'title': 'Write flask tests',  
            'description': 'New description', 
        }
        
        with self.client:
            response = self.client.post(
                url_for('todo.add'),
                data=data, 
                follow_redirects=True
            )
            
            todo = Todo.query.filter_by(id=1).first()
            
            assert todo is not None
            assert todo.title == data['title']
            assert response.status_code == 200


    def test_get_all_todo(self):
        """
        GIVEN todos data
        WHEN the all existing todos queried (for ex. exist only 2 todos)
        THEN check that todo's count equal to 2
        """
        
        todo_1 = Todo(title="todo1", description="description1", complete=False)
        todo_2 = Todo(title="todo2", description="description2", complete=False)
        db.session.add_all([todo_1, todo_2])
        number_of_todos = Todo.query.count()
        assert number_of_todos == 2


    def test_update_todo_complete(self):
        """
        GIVEN todo item
        WHEN the complete field updated
        THEN response status code is 200 and todo.complete is equal to True
        """
        
        todo_1 = Todo(title="todo1", description="description1", complete=False)
        db.session.add(todo_1)
        with self.client:
            response = self.client.get(
                url_for('todo.update', id=1),
                follow_redirects=True
            )
            
            todo = Todo.query.filter_by(id=1).first()
            
            assert todo.complete == True
            assert response.status_code == 200


    def test_delete_todo(self):
        """
        GIVEN todo item
        WHEN the todo deleted
        THEN todo item does not exist and response status is 200
        """
        
        data = {
            'title': 'Write flask tests',  
            'description': 'New description', 
        }
        
        with self.client:
            self.client.post(
                url_for('todo.add'),
                data=data, 
                follow_redirects=True
            )
            
            response = self.client.get(
                url_for('todo.delete', id=1),
                follow_redirects=True
            )
            
            todo = Todo.query.filter_by(id=1).first()
            
            assert response.status_code == 200
            assert todo is None
            
        

if __name__ == '__main__':
    unittest.main()