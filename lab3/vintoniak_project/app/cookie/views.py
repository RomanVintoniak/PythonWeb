from flask import render_template, request, session, make_response, redirect, url_for, flash
from flask_login import login_required
from . import cookie_bp


@cookie_bp.route("/info", methods=['GET', 'POST'])
@login_required
def info():
    
    #if not session.get("username"):
    #    flash("Please check the box 'remember me'", "danger")
    #    return redirect(url_for('login'))
    
    username = session.get("username")
    cookies = request.cookies
    return render_template("info.html", username=username, cookies=cookies)



@cookie_bp.route('/setCookie', methods=["POST"])
def setCookie():
    key = request.form.get("key")
    value = request.form.get("value")
    days = request.form.get("days")
    #message = "Cookie successfully set"
    response = make_response(redirect(url_for('info')))
    response.set_cookie(key, value, max_age=60*60*24*int(days))
    flash("Cookie set successfully", "success")
    return response


@cookie_bp.route("/deleteCookieByKey", methods=["POST"])
def deleteCookieByKey():
    key = request.form.get("key")
    response = make_response(redirect(url_for('info')))
    response.delete_cookie(key) 
    flash("Cookie deleted by key successfully", "success")
    return response


@cookie_bp.route("/deleteCookieAll", methods=["POST"])
def deleteCookieAll():
    cookiesKeys = request.cookies
    response = make_response(redirect(url_for('info')))
    
    for key, value in cookiesKeys.items():
        if key != "session":
            response.delete_cookie(key)
    flash("Cookie deleted successfully", "success")    
    return response