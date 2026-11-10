
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.database import db
from app.models import Task

main = Blueprint("main", __name__)


# Display all tasks
@main.route("/")
def home():
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)


# Application health check
@main.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "message": "Application is running"
    }), 200


# Add a new task
@main.route("/add", methods=["POST"])
def add_task():

    title = request.form.get("title", "").strip()

    # Reject empty task titles
    if not title:
        return jsonify({
            "error": "Task title cannot be empty"
        }), 400

    task = Task(title=title)

    db.session.add(task)
    db.session.commit()

    return redirect(url_for("main.home"))


# Mark a task as completed
@main.route("/complete/<int:task_id>", methods=["POST"])
def complete_task(task_id):

    task = db.session.get(Task, task_id)

    if task:
        task.completed = True
        db.session.commit()

    return redirect(url_for("main.home"))


# Delete a task
@main.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):

    task = db.session.get(Task, task_id)

    if task:
        db.session.delete(task)
        db.session.commit()

    return redirect(url_for("main.home"))
