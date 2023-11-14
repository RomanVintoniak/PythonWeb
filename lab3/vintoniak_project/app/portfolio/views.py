import os
from flask import render_template, redirect, url_for, request, abort
from datetime import datetime
from .data import certificats
from . import portfolio

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


@portfolio.route('/')
def home():
    osInfo = os.environ.get('OS')
    agent = request.user_agent
    time = datetime.now().strftime("%H:%M:%S")
    
    return render_template('home.html', certificats=certificats, agent=agent, time=time, osInfo=osInfo)

@portfolio.route('/skills/<int:id>')
@portfolio.route('/skills')
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
    
    
@portfolio.route('/certificates')
def certificates():
    osInfo = os.environ.get('OS')
    agent = request.user_agent
    time = datetime.now().strftime("%H:%M:%S")
    
    return render_template('certificates.html', certificats=certificats)