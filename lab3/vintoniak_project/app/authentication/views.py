from flask import redirect, url_for, render_template, flash, session, request
from .forms import RegistrationForm, LoginForm, UpdateAccountForm, ResetPasswordForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from app.handlers.img_handler import add_account_img
from datetime import datetime
from .models import User
from app import db
from . import auth


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in", "success")
        return redirect(url_for('portfolio.home'))
    
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
                return redirect(url_for('auth.account'))
            login_user(user)
            flash("Login Succesful to home", "success")
            return redirect(url_for('portfolio.home'))
        
        flash("Incorrect email or password", "danger")
        return redirect(url_for('auth.login'))
    
    return render_template('login.html', form=form)


@auth.route("/registration", methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        flash("You are already registered", "success")
        return redirect(url_for('portfolio.home'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        user = User(username, email, password)
        
        db.session.add(user)
        db.session.commit()
        
        flash(f"Account created for {form.username.data} !", "success")
        return redirect(url_for('auth.login'))
    
    return render_template("registration.html", form=form)


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    logout_user()
    flash("You are logged out", "success")
    return redirect(url_for('auth.login'))


@auth.route('/account', methods=["GET", "POST"])
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
        return redirect(url_for('auth.account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.aboutMe.data = current_user.aboutMe
    
    return render_template('account.html', form=form)


@auth.route('/resetPassword', methods=['GET', 'POST'])
@login_required
def resetPassword():
    form = ResetPasswordForm()
    
    if form.validate_on_submit():
        current_user.password = generate_password_hash(form.newPassword.data)
        db.session.commit()
        flash("Password changed successfully", "success")
        return redirect(url_for('auth.account'))
    
    return render_template("resetPassword.html", form=form)


@auth.after_request
def after_request(response):
    if current_user:
        current_user.lastSeen = datetime.now()
        try:
            db.session.commit()
        except:
            flash('Error while update user last seen!', 'danger')
        return response


@auth.route('/users')
def users():
    users = User.query.all()
    return render_template("users.html", users=users)