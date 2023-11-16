from flask import render_template, redirect, url_for, flash
from .forms import AddFeedback
from .models import Feedback
from app import db
from . import feedback


@feedback.route("/feedbacks", methods=["GET", "POST"])
def feedbacks():
    form = AddFeedback()
    feedbacks = Feedback.query.all()
    return render_template("feedbacks.html", form = form, feedbacks=feedbacks)


@feedback.route("/feedbacks/add", methods=["POST"])
def add():
    form = AddFeedback()
    
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        content = form.content.data
        
        feedback = Feedback(username, email, content)
        
        db.session.add(feedback)
        db.session.commit()
        
        flash("feedback add successfully", "success")
        
    return redirect(url_for("feedback.feedbacks"))


@feedback.route('/feedbacks/delete/<int:id>')
def delete(id):
    feedbaack = Feedback.query.filter_by(id=id).first_or_404()
    db.session.delete(feedbaack)
    db.session.commit()
    flash("feedback deleted successfully", "success")
    return redirect(url_for('feedback.feedbacks'))