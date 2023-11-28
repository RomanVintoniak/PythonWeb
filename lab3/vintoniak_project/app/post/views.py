from flask import render_template, redirect, url_for, flash, abort, request
from .handlers.post_img_handler import add_post_img
from flask_login import current_user
from .forms import AddUpdatePostForm
from .models import Post
from app import db
from . import post

@post.route("/posts")
def posts():
    page = request.args.get('page', 1, type = int)
    posts = Post.query.order_by(Post.createdAt.desc()).paginate(page = page, per_page = 2)
    
    return render_template('posts.html', posts=posts)
    

@post.route("/post/create", methods=["GET", "POST"])
def create():
    form = AddUpdatePostForm()
    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data
        postType = form.postType.data
        userID = current_user.id
        
        if form.image.data:
            image = add_post_img(form.image.data)
            post = Post(title=title, text=text, image=image, user_id=userID, postType=postType)
        else:
            post = Post(title=title, text=text, user_id=userID, postType=postType)
        
        db.session.add(post)
        db.session.commit()
        flash("Created new post", "success")
        
        return redirect(url_for("post.posts"))
    return render_template("createPost.html", form=form)


@post.route("/post/<int:id>")
def postID(id):
    post = Post.query.filter_by(id=id).first_or_404()
    return render_template("post.html", post=post, current_user=current_user)


@post.route("/post/<int:id>/delete")
def delete(id):
    post = Post.query.filter_by(id=id).first_or_404()
    
    if post.author != current_user:
        abort(403)
        
    db.session.delete(post)
    db.session.commit()
    flash("Post has been deleted", "success")
    return redirect(url_for('post.posts'))


@post.route("/post/<int:id>/update", methods=["GET", "POST"])
def update(id):
    post = Post.query.filter_by(id=id).first_or_404()
    
    if post.author != current_user:
        abort(403)
    
    form = AddUpdatePostForm()
    
    if form.validate_on_submit():
        if form.image.data:
            image = add_post_img(form.image.data)
            post.image = image
        post.title = form.title.data
        post.text = form.text.data
        post.postType = form.postType.data
        db.session.commit()
        flash('Post Updated', "success")
        return redirect(url_for('post.posts'))
    elif request.method == "GET":
        form.title.data = post.title
        form.text.data = post.text
        form.postType.data = post.postType
        
    return render_template('editPost.html', form=form)
            
    
        