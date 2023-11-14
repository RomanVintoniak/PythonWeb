from flask import render_template, request, redirect, session, url_for, make_response, flash
from app import app, db
from app.models import User
from datetime import datetime
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash



@app.after_request
def after_request(response):
    if current_user:
        current_user.lastSeen = datetime.now()
        try:
            db.session.commit()
        except:
            flash('Error while update user last seen!', 'danger')
        return response



@app.route("/info", methods=['GET', 'POST'])
@login_required
def info():
    
    #if not session.get("username"):
    #    flash("Please check the box 'remember me'", "danger")
    #    return redirect(url_for('login'))
    
    username = session.get("username")
    cookies = request.cookies
    return render_template("info.html", username=username, cookies=cookies)



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
    
@app.route('/users')
def users():
    users = User.query.all()
    return render_template("users.html", users=users)
