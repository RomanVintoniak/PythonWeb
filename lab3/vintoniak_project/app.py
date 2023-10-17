from flask import Flask, render_template, abort, request
import os
from datetime import datetime
from data import certificats
app = Flask(__name__)

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
    osInfo = os.environ['OS']
    agent = request.user_agent
    time = datetime.now().strftime("%H:%M:%S")
    
    return render_template('home.html', certificats=certificats, agent=agent, time=time, osInfo=osInfo)

@app.route('/skills/<int:id>')
@app.route('/skills')
def skills(id=None):
    osInfo = os.environ['OS']
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
    osInfo = os.environ['OS']
    agent = request.user_agent
    time = datetime.now().strftime("%H:%M:%S")
    
    return render_template('certificates.html', certificats=certificats, agent=agent, time=time, osInfo=osInfo)

if __name__ == '__main__':  
    app.run(debug=True)