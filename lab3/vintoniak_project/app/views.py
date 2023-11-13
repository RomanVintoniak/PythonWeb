import os, json
from flask import render_template, abort, request, redirect, session, url_for, make_response, flash
from .form import LoginForm, ResetPasswordForm, RegistrationForm, UpdateAccountForm
from app import app, db
from app.models import User
from datetime import datetime
from data import certificats
from flask_login import login_user, current_user, logout_user, login_required
from .handlers.img_handler import add_account_img
from werkzeug.security import generate_password_hash

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

@app.after_request
def after_request(response):
    if current_user:
        current_user.lastSeen = datetime.now()
        try:
            db.session.commit()
        except:
            flash('Error while update user last seen!', 'danger')
        return response


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
        
        user = User.query.filter_by(email=inputtedEmail).first_or_404()
    
        if (inputtedEmail == user.email and user.checkPassword(inputtedPassword)):
            if form.rememberMe.data:
                session["username"] = user.username
                login_user(user)
                flash("Login Succesful", "success")
                return redirect(url_for('account'))
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
@login_required
def info():
    
    #if not session.get("username"):
    #    flash("Please check the box 'remember me'", "danger")
    #    return redirect(url_for('login'))
    
    username = session.get("username")
    cookies = request.cookies
    return render_template("info.html", username=username, cookies=cookies)


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
    

@app.route('/resetPassword', methods=['GET', 'POST'])
@login_required
def resetPassword():
    form = ResetPasswordForm()
    
    if form.validate_on_submit():
        current_user.password = generate_password_hash(form.newPassword.data)
        db.session.commit()
        flash("Password changed successfully", "success")
        return redirect(url_for('account'))
    
    return render_template("resetPassword.html", form=form)
    


@app.route('/users')
def users():
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route('/account', methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    
    if form.validate_on_submit():
        if form.image.data:
            newImage = add_account_img(form.image.data)
            current_user.image = newImage
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.aboutMe = form.aboutMe.data
        db.session.commit()
        flash('Account Updated', "success")
        return redirect(url_for('account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.aboutMe.data = current_user.aboutMe
    
    return render_template('account.html', form=form)