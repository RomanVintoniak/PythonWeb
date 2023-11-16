from flask import render_template, redirect, url_for
from .forms import AddTodoItemForm
from .models import Todo
from app import db
from . import todo

@todo.route('/todo', methods=["GET", "POST"])
def todos():
    form = AddTodoItemForm()
    todo_list = Todo.query.all()
    return render_template('todo.html', form=form, todo_list=todo_list)


@todo.route('/todo/add', methods=["POST"])
def add():
    form = AddTodoItemForm()
    
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        todoItem = Todo(title=title, description=description, complete=False)
        db.session.add(todoItem)
        db.session.commit()
        
    return redirect(url_for("todo.todos"))


@todo.route('/todo/delete/<int:id>')
def delete(id):
    todoItem = Todo.query.filter_by(id=id).first_or_404()
    db.session.delete(todoItem)
    db.session.commit()
    return redirect(url_for('todo.todos'))


@todo.route('/todo/update/<int:id>')
def update(id):
    todoItem = Todo.query.filter_by(id=id).first_or_404()
    todoItem.complete = not todoItem.complete
    db.session.commit()
    return redirect(url_for('todo.todos'))