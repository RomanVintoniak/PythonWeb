import os, json
from flask import render_template, abort, request, redirect, session, url_for, make_response, flash
from .form import LoginForm, ChangePasswordForm, AddTodoItemForm
from app import app
from datetime import datetime, timedelta
from data import certificats
from os.path import join, dirname, realpath

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
    if session.get('username'):
        return redirect(url_for('info'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        inputtedUsername = form.username.data
        inputtedPassword = form.password.data
        
        dataJsonPath = join(dirname(realpath(__file__)), 'data.json')
        with open(dataJsonPath, "r", encoding="utf-8") as f:
            userData = json.loads(f.read())
    
        if (inputtedUsername == userData.get('username') and inputtedPassword == userData.get("password")):
            if form.rememberMe.data:
                session["username"] = inputtedUsername
                flash("Login Succesful", "success")
                return redirect(url_for('info'))
            flash("Login Succesful to home", "success")
            return redirect(url_for('home'))
        
        flash("Incorrect username or password", "danger")
        return redirect(url_for('login'))
    
    return render_template('login.html', form=form)


@app.route("/info", methods=['GET', 'POST'])
def info():
    changePasswordForm = ChangePasswordForm()
    
    if not session.get("username"):
        flash("Please check the box 'remember me'", "danger")
        return redirect(url_for('login'))
    
    username = session.get("username")
    cookies = request.cookies
    return render_template("info.html", username=username, cookies=cookies, changePasswordForm=changePasswordForm)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
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
    

@app.route('/todo')
def todo():
    form = AddTodoItemForm()
    return render_template('todo.html', form=form)