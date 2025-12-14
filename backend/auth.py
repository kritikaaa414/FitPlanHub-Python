from flask import Blueprint, request
from flask_jwt_extended import create_access_token
import bcrypt
from database import get_db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json
    hashed_pw = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt())

    db = get_db()
    try:
        db.execute(
            "INSERT INTO users (name,email,password,role) VALUES (?,?,?,?)",
            (data["name"], data["email"], hashed_pw, data["role"])
        )
        db.commit()
        return {"message": "Signup successful"}
    except:
        return {"error": "Email already exists"}, 400


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    db = get_db()

    user = db.execute(
        "SELECT * FROM users WHERE email=?",
        (data["email"],)
    ).fetchone()

    if user and bcrypt.checkpw(data["password"].encode(), user["password"]):
        token = create_access_token(identity=user["id"])
        return {"token": token, "role": user["role"]}

    return {"error": "Invalid credentials"}, 401
