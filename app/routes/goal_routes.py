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
    return create_model(Goal, request_body)

@bp.get("")
def get_all_goals():
    return get_models_with_filters(Goal, request.args)

@bp.get("/<id>")
def get_one_goal(id):
    goal = validate_model(Goal, id)
    return goal.to_dict()

@bp.put("/<id>")
def update_goal(id):
    goal = validate_model(Goal, id)
    request_body = request.get_json()
    updated_goal = Goal.from_dict(request_body)
    updated_goal.id = id
    db.session.merge(updated_goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
   
@bp.delete("/<id>")
def delect_goal(id):
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
        query = db.select(Task).where(Task.id == task_id)
        tasks.append(db.session.scalar(query))
    goal.tasks = tasks
    db.session.merge(goal)
    db.session.commit()
    return goal.to_dict()

@bp.get("/<goal_id>/tasks")
def get_tasks_by_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return goal.to_dict()









