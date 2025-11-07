from flask import Blueprint, abort, make_response, request, Response
from ..slack_api.post_message import post_message_with_slack_bot
from .route_utilities import create_model, validate_model, get_models_with_filters
from  app.models.task import Task
from  app.models.goal import Goal
from datetime import datetime
from ..db import db
bp = Blueprint("task_bp",__name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model(Task, request_body)
    
@bp.get("")
def get_all_tasks():
    query = db.select(Task)
    title_param = request.args.get("title")
    if title_param:
        query = query.where(Task.title.ilike(f"%{title_param}%"))
    # Sorting logic
    sort_param = request.args.get("sort")
    if sort_param == "asc":
        query = query.order_by(Task.title.asc())   
    elif sort_param == "desc":
        query = query.order_by(Task.title.desc())  
    else:
        query = query.order_by(Task.id)  

    tasks = db.session.scalars(query)
        
    description_param = request.args.get("description")
    if description_param:
        # In case there are tasks with similar titles, we can also filter by description
        query = query.where(Task.description.ilike(f"%{description_param}%"))
    tasks = db.session.scalars(query.order_by(Task.id))
    response = []

    for task in tasks:     
        response.append(task.to_dict())

    return response

@bp.put("/<id>")
def update_task(id):
    validate_model(Task, id)
    request_body = request.get_json()
    updated_task = Task.from_dict(request_body)
    updated_task.id = id
    db.session.merge(updated_task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<id>")
def delect_task(id):
    task = validate_model(Task,id)
    db.session.delete(task)
    db.session.commit()
    return Response(status=204, mimetype="application/json")

@bp.patch("/<id>/mark_complete")
def mark_complete(id):
    task = validate_model(Task,id)
    task.completed_at = datetime.utcnow()
    db.session.commit()
    post_message_with_slack_bot(f"Someone just completed the task {task.title}")
    return Response(status=204, mimetype="application/json")

@bp.patch("/<id>/mark_incomplete")
def mark_incomplete(id):
    task = validate_model(Task,id)
    task.completed_at = None
    db.session.commit()
    return Response(status=204, mimetype="application/json")

@bp.get("/<id>")
def get_tasks_by_id(id):
    goal = validate_model(Task,id)
    return goal.to_dict()





