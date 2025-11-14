from flask import Blueprint, abort, make_response, request, Response
from ..slack_api.post_message import post_message_with_slack_bot
from .route_utilities import create_model, validate_model, build_query_with_filters
from  app.models.task import Task
from datetime import datetime, timezone
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
    description_param = request.args.get("description")

    query = build_query_with_filters(Task, {
        "title": title_param,
        "description": description_param
    })

    if title_param:
        query = query.where()
    # Sorting logic
    sort_param = request.args.get("sort")
    if sort_param == "asc":
        query = query.order_by(Task.title.asc())   
    elif sort_param == "desc":
        query = query.order_by(Task.title.desc())  
    else:
        query = query.order_by(Task.id)  

    tasks = db.session.scalars(query)

    response = []
    for task in tasks:     
        response.append(task.to_dict())

    return response

@bp.put("/<id>")
def update_task(id):
    task = validate_model(Task, id)
    request_body = request.get_json()
    task.title = request_body.get("title")
    task.description = request_body.get("description")
    task.completed_at = request_body.get("completed_at")
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<id>")
def delete_task(id):
    task = validate_model(Task,id)
    db.session.delete(task)
    db.session.commit()
    return Response(status=204, mimetype="application/json")

@bp.patch("/<id>/mark_complete")
def mark_complete(id):
    task = validate_model(Task,id)
    task.completed_at = datetime.now(timezone.utc)
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
    task = validate_model(Task, id)
    return task.to_dict()





