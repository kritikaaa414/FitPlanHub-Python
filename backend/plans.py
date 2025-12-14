from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import get_db

plans_bp = Blueprint("plans", __name__)

@plans_bp.route("/plans", methods=["POST"])
@jwt_required()
def create_plan():
    data = request.json
    trainer_id = get_jwt_identity()
    db = get_db()

    db.execute(
        "INSERT INTO plans (trainer_id,title,description,price,duration) VALUES (?,?,?,?,?)",
        (trainer_id, data["title"], data["description"], data["price"], data["duration"])
    )
    db.commit()
    return {"message": "Plan created"}


@plans_bp.route("/plans", methods=["GET"])
def get_plans():
    db = get_db()
    plans = db.execute("SELECT * FROM plans").fetchall()
    return [dict(p) for p in plans]


@plans_bp.route("/subscribe", methods=["POST"])
@jwt_required()
def subscribe():
    user_id = get_jwt_identity()
    plan_id = request.json["plan_id"]

    db = get_db()
    db.execute(
        "INSERT INTO subscriptions (user_id, plan_id) VALUES (?,?)",
        (user_id, plan_id)
    )
    db.commit()
    return {"message": "Subscribed"}
