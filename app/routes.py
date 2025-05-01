from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User

bp = Blueprint("main", __name__)

@bp.route("/healthcheck")
def healthcheck():
    return jsonify({"status": "ok"})

@bp.route("/create-account", methods=["POST"])
def create_account():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 409
    
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Account created successfully"}), 201

@bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session["user_id"] = user.id
        return jsonify({"message": "Login successful"})
    return jsonify({"error": "Invalid credentials"}), 401

@bp.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return jsonify({"message": "Logged out"})

@bp.route("/update-password", methods=["PUT"])
def update_password():
    if "user_id" not in session:
        return jsonify({"error": "Authentication required"}), 401

    data = request.json
    new_password = data.get("new_password")
    if not new_password:
        return jsonify({"error": "Missing new password"}), 400

    user = User.query.get(session["user_id"])
    user.set_password(new_password)
    db.session.commit()
    return jsonify({"message": "Password updated successfully"})