import json

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import PlainTaskSchema, TaskSchema, BunchSchema, BunchSchemaForAdd, ReturnTaskSchema, ReturnBunchSchema
from db import db
from flask import jsonify, request
from models.task import TaskModel
from models.task import TaskModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from marshmallow import ValidationError

blp = Blueprint("tasks", __name__, description="Task APIs")

@blp.route("/v1/task")
class AddSingleTask(MethodView):
    # add a single task
    @blp.response(201, TaskSchema)
    @blp.arguments(TaskSchema)
    def post(self, task_data):
        task = TaskModel()
        task.title = task_data["title"]
        task.is_completed = False
        try:
            db.session.add(task)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="error occurred while inserting task")
        return task

@blp.route("/v1/tasks/<string:task_id>")
class TaskWithId(MethodView):
    # get a specific task
    @blp.response(200, TaskSchema)
    def get(self, task_id):
        task = TaskModel.query.get(task_id)
        if task is None:
            return jsonify(message="Task not Found"), 404
        return task

    # delete a specific task
    def delete(self, task_id):
        store = TaskModel.query.get_or_404(task_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "task deleted"}

    # edit the task
    @blp.response(204, TaskSchema)
    @blp.arguments(TaskSchema)
    def put(self, task_data, task_id):
        task = TaskModel.query.get(task_id)
        if task is None:
            return jsonify(message="There is no task at that id"), 404
        task.title = task_data["title"]
        task.is_completed = task_data["is_completed"]

        try:
            db.session.add(task)
            db.session.commit()
        except SQLAlchemyError:
            abort (500, message="error occurred while inserting task")


# def add_single_task(task_data):
#     new_task = TaskModel(task_data)
#     db.session.add(new_task)
#     db.session.commit()
#     return new_task
#
#
# def add_multiple_tasks(tasks_data):
#     added_tasks = []
#     for task_data in tasks_data:
#         new_task = TaskModel(task_data)
#         added_tasks.append(new_task)
#     db.session.commit()
#     return added_tasks

@blp.route("/v1/tasks")
class TaskList(MethodView):

    # add multiple tasks
    @blp.response(201, ReturnBunchSchema)
    @blp.arguments(BunchSchemaForAdd, required=False, location="json")
    def post(self, task_data):
        tasks = task_data["tasks"]
        lst = []
        for task in tasks:
            task_orm = TaskModel()
            task_orm.title = task["title"]
            task_orm.is_completed = task["is_completed"]
            try:
                db.session.add(task_orm)
                db.session.commit()
                lst.append({"id": task_orm.id, "title": task_orm.title})
            except SQLAlchemyError as e:
                db.session.rollback()
                abort(500, message=f"error occurred while inserting task: {str(e)}")
        return jsonify({"tasks": lst})

    # list all tasks
    @blp.response(200, TaskSchema(many=True))
    def get(self):
        taskList = TaskModel.query.all()
        return taskList

    @blp.arguments(BunchSchema, required=False, location="json")
    # delete bunch of tasks
    def delete(self, task_data):
        for task in task_data["tasks"]:
            id = TaskModel.query.get_or_404(task["id"])
            try:
                db.session.delete(id)
                db.session.commit()
            except SQLAlchemyError as e:
                abort(500, message=f"error occurred while inserting task: {str(e)}")
        return {"message": "task deleted"}, 204



