import os, json
from flask import render_template, abort, request, redirect, session, url_for, make_response, flash
from .form import LoginForm, ChangePasswordForm, AddTodoItemForm, AddReview, RegistrationForm
from app import app, db
from app.models import Todo, Review, User
from datetime import datetime, timedelta
from data import certificats
from os.path import join, dirname, realpath
from flask_login import login_user, current_user, logout_user

mySkills = [
    {
        "skillName": "HTML",
        "level": "skillful",
        "icon": "devicon-html5-plain colored fs-45"
    },
    {
        "skillName": "CSS",
        "level": "skillful",
        "icon": "devicon-css3-plain colored fs-45"
    },
    {
        "skillName": "Python",
        "level": "skillful",
        "icon": "devicon-python-plain colored fs-45"
    },
    {
        "skillName": "GIT",
        "level": "beginer",
        "icon": "devicon-github-original colored fs-45"
    },
    {
        "skillName": "SQL",
        "level": "skillful",
        "icon": "fa fa-database fs-45 text-info"
    }
] 

@app.route('/')
def home():
    osInfo = os.environ.get('OS')
    agent = request.user_agent
    time = datetime.now().strftime("%H:%M:%S")
    
    return render_template('home.html', certificats=certificats, agent=agent, time=time, osInfo=osInfo)

@app.route('/skills/<int:id>')
@app.route('/skills')
def skills(id=None):
    
    if id:
        if id > len(mySkills):
            abort(404)
        else:
            index = id - 1
            skill = mySkills[index]
            return render_template('skill.html', skill=skill, id=id)    
    else:
        return render_template('skills.html', mySkills=mySkills)
    
    
@app.route('/certificates')
def certificates():
    osInfo = os.environ.get('OS')
    agent = request.user_agent
    time = datetime.now().strftime("%H:%M:%S")
    
    return render_template('certificates.html', certificats=certificats)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in", "success")
        return redirect(url_for('home'))
    
    #if session.get('username'):
    #    return redirect(url_for('info'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        inputtedEmail = form.email.data
        inputtedPassword = form.password.data
        
        user = User.query.filter_by(email=inputtedEmail).first()
    
        if (inputtedEmail == user.email and user.checkPassword(inputtedPassword)):
            if form.rememberMe.data:
                session["username"] = user.username
                login_user(user)
                flash("Login Succesful", "success")
                return redirect(url_for('info'))
            login_user(user)
            flash("Login Succesful to home", "success")
            return redirect(url_for('home'))
        
        flash("Incorrect email or password", "danger")
        return redirect(url_for('login'))
    
    return render_template('login.html', form=form)


@app.route("/registration", methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        flash("You are already registered", "success")
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        user = User(username, email, password)
        
        db.session.add(user)
        db.session.commit()
        
        flash(f"Account created for {form.username.data} !", "success")
        return redirect(url_for('login'))
    
    return render_template("registration.html", form=form)


@app.route("/info", methods=['GET', 'POST'])
def info():
    changePasswordForm = ChangePasswordForm()
    
    #if not session.get("username"):
    #    flash("Please check the box 'remember me'", "danger")
    #    return redirect(url_for('login'))
    
    username = session.get("username")
    cookies = request.cookies
    return render_template("info.html", username=username, cookies=cookies, changePasswordForm=changePasswordForm)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    logout_user()
    flash("You are logged out", "success")
    return redirect(url_for('login'))


@app.route('/setCookie', methods=["POST"])
def setCookie():
    key = request.form.get("key")
    value = request.form.get("value")
    days = request.form.get("days")
    #message = "Cookie successfully set"
    response = make_response(redirect(url_for('info')))
    response.set_cookie(key, value, max_age=60*60*24*int(days))
    flash("Cookie set successfully", "success")
    return response


@app.route("/deleteCookieByKey", methods=["POST"])
def deleteCookieByKey():
    key = request.form.get("key")
    response = make_response(redirect(url_for('info')))
    response.delete_cookie(key) 
    flash("Cookie deleted by key successfully", "success")
    return response


@app.route("/deleteCookieAll", methods=["POST"])
def deleteCookieAll():
    cookiesKeys = request.cookies
    response = make_response(redirect(url_for('info')))
    
    for key, value in cookiesKeys.items():
        if key != "session":
            response.delete_cookie(key)
    flash("Cookie deleted successfully", "success")    
    return response
    

@app.route('/changePassword', methods=['GET', 'POST'])
def changePassword():
    changePasswordForm = ChangePasswordForm()
    
    if changePasswordForm.validate_on_submit():
        newPass = changePasswordForm.password.data
        rePass = changePasswordForm.repassword.data
        username = session.get("username")
        
        if newPass == rePass:
            
            dataJsonPath = join(dirname(realpath(__file__)), 'data.json')
            temp = {
                "username": username,
                "password": newPass
            }
            
            jsonString = json.dumps(temp, indent=2)
            with open(dataJsonPath, "w") as f:
                f.write(jsonString)
            
            flash("Password changed successfully", "success")
            return redirect(url_for('login'))
        
    flash("Passwords do not match", "danger")    
    return redirect(url_for('info'))
    

@app.route('/todo', methods=["GET", "POST"])
def todo():
    form = AddTodoItemForm()
    todo_list = Todo.query.all()
    return render_template('todo.html', form=form, todo_list=todo_list)


@app.route('/todo/add', methods=["POST"])
def add():
    form = AddTodoItemForm()
    
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        todoItem = Todo(title=title, description=description, complete=False)
        db.session.add(todoItem)
        db.session.commit()
        
    return redirect(url_for("todo"))


@app.route('/todo/delete/<int:id>')
def delete(id):
    todoItem = Todo.query.filter_by(id=id).first_or_404()
    db.session.delete(todoItem)
    db.session.commit()
    return redirect(url_for('todo'))


@app.route('/todo/update/<int:id>')
def update(id):
    todoItem = Todo.query.filter_by(id=id).first_or_404()
    todoItem.complete = not todoItem.complete
    db.session.commit()
    return redirect(url_for('todo'))



    
@app.route("/reviews", methods=["GET", "POST"])
def reviews():
    form = AddReview()
    reviews_list = Review.query.all()
    return render_template("reviews.html", form = form, reviews_list=reviews_list)


@app.route("/reviews/add", methods=["POST"])
def addRevie():
    form = AddReview()
    
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        content = form.content.data
        
        review = Review(username, email, content)
        
        db.session.add(review)
        db.session.commit()
        
        flash("Revie add successfully", "success")
        
    return redirect(url_for("reviews"))


@app.route('/reviews/delete/<int:id>')
def deleteReview(id):
    review = Review.query.filter_by(id=id).first_or_404()
    db.session.delete(review)
    db.session.commit()
    flash("Revie deleted successfully", "success")
    return redirect(url_for('reviews'))


@app.route('/users')
def users():
    users = User.query.all()
    return render_template("users.html", users=users)