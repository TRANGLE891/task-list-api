from flask import Blueprint, abort, make_response, request, Response
from .route_utilities import create_model, validate_model, get_models_with_filters
from  app.models.goal import Goal
from  app.models.task import Task
from datetime import datetime
from ..db import db
from ..slack_api.post_message import post_message_with_slack_bot

bp = Blueprint("goal_bp",__name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
    # Create goal here so we can shape the response as the tests expect
    try:
        new_goal = Goal.from_dict(request_body)
    except KeyError:
        # Match test expectation for invalid create payload
        return make_response({"details": "Invalid data"}, 400)

    db.session.add(new_goal)
    db.session.commit()

    return make_response({"id": new_goal.id, "title": new_goal.title}, 201)

@bp.get("")
def get_all_goals():
    query = db.select(Goal)
    goals = db.session.scalars(query.order_by(Goal.id))
    return [g.to_summary_dict() for g in goals]

@bp.get("/<id>")
def get_one_goal(id):
    goal = validate_model(Goal, id)
    return goal.to_summary_dict()

@bp.put("/<id>")
def update_goal(id):
    goal = validate_model(Goal, id)
    request_body = request.get_json()
    goal.title = request_body.get("title")
    db.session.commit()
    return Response(status=204, mimetype="application/json")

@bp.delete("/<id>")
def delete_goal(id):
    goal = validate_model(Goal, id)
    db.session.delete(goal)
    db.session.commit()
    return Response(status=204, mimetype="application/json")

@bp.post("/<goal_id>/tasks")
def add_task_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()   
    tasks = []
    for task_id in request_body['task_ids']:
        task = validate_model(Task, task_id)
        tasks.append(task)
    goal.tasks = tasks
    db.session.commit()
    return {"id": goal.id, "task_ids": [task.id for task in goal.tasks]}

@bp.get("/<goal_id>/tasks")
def get_tasks_by_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return {"id": goal.id, "title": goal.title, "tasks": [task.to_dict() for task in goal.tasks]}









