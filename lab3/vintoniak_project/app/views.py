import os, json
from flask import render_template, abort, request, redirect, session, url_for, make_response, flash
from .form import LoginForm
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
    osInfo = os.environ.get('OS')
    agent = request.user_agent
    time = datetime.now().strftime("%H:%M:%S")
    
    if id:
        if id > len(mySkills):
            abort(404)
        else:
            index = id - 1
            skill = mySkills[index]
            return render_template('skill.html', skill=skill, agent=agent, time=time, id=id, osInfo=osInfo)    
    else:
        return render_template('skills.html', mySkills=mySkills, agent=agent, time=time, osInfo=osInfo)
    
    
@app.route('/certificates')
def certificates():
    osInfo = os.environ.get('OS')
    agent = request.user_agent
    time = datetime.now().strftime("%H:%M:%S")
    
    return render_template('certificates.html', certificats=certificats, agent=agent, time=time, osInfo=osInfo)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if request.method == "POST":
        if form.validate_on_submit():
            inputtedUsername = form.username.data
            inputtedPassword = form.password.data
    
            dataJsonPath = join(dirname(realpath(__file__)), 'data.json')
            with open(dataJsonPath, "r") as f:
                userData = json.loads(f.read())
        
            if (inputtedUsername == userData["username"] and inputtedPassword == userData["password"]):
                if form.rememberMe.data == True:
                    session["username"] = inputtedUsername
                    flash("Login Succesful", "success")
                return redirect(url_for('info'))
            else:
                flash("Incorrect username or password", "danger")
                return redirect(url_for('login'))
        
    
    return render_template('login.html', form=form)


@app.route("/info", methods=['GET', 'POST'])
def info():
    
    if not session.get("username"):
        flash("Please check the box 'remember me'", "danger")
        return redirect(url_for('login'))
    
    username = session.get("username")
    cookies = request.cookies
    return render_template("info.html", username=username, cookies=cookies)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/setCookie', methods=["POST"])
def setCookie():
    key = request.form.get("key")
    value = request.form.get("value")
    days = request.form.get("days")
    #message = "Cookie successfully set"
    response = make_response(redirect(url_for('info')))
    response.set_cookie(key, value, max_age=60*60*24*int(days))
    return response


@app.route("/deleteCookieByKey", methods=["POST"])
def deleteCookieByKey():
    key = request.form.get("key")
    response = make_response(redirect(url_for('info')))
    response.delete_cookie(key)
    return response


@app.route("/deleteCookieAll", methods=["POST"])
def deleteCookieAll():
    cookiesKeys = request.cookies
    response = make_response(redirect(url_for('info')))
    
    for key, value in cookiesKeys.items():
        if key != "session":
            response.delete_cookie(key)
        
    return response
    

@app.route('/changePassword', methods=['GET', 'POST'])
def changePassword():
    
    if request.method == "POST":
        newPass = request.form.get("newPass")
        rePass = request.form.get("rePass")
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
            
            return redirect(url_for('login'))
        
    return redirect(url_for('info'))