from flask import render_template, flash
from app import app, db
from app.models import User
from datetime import datetime
from flask_login import current_user

@app.after_request
def after_request(response):
    if current_user:
        current_user.lastSeen = datetime.now()
        try:
            db.session.commit()
        except:
            flash('Error while update user last seen!', 'danger')
        return response


@app.route('/users')
def users():
    users = User.query.all()
    return render_template("users.html", users=users)
