from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User
from app.models import favorites
from app.weather_api import get_current_weather, get_forecast
import time
from app.weather_api import get_historical_weather
from datetime import datetime

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
        return jsonify({"error": "missing username or wrong password"}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "username already taken"}), 409
    
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "success - account created"}), 201

@bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session["user_id"] = user.id
        return jsonify({"message": "logged in"})
    return jsonify({"error": "wrong username and password combination "}), 401

@bp.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return jsonify({"message": "logged out"})

@bp.route("/update-password", methods=["PUT"])
def update_password():
    if "user_id" not in session:
        return jsonify({"error": "please authenticate yourself"}), 401

    data = request.json
    new_password = data.get("new_password")
    if not new_password:
        return jsonify({"error": "not new password"}), 400

    user = User.query.get(session["user_id"])
    user.set_password(new_password)
    db.session.commit()
    return jsonify({"message": "password updated"})

@bp.route("/add-favorite", methods=["POST"])
def add_favorite():
    if "user_id" not in session:
        return jsonify({"error": "please authenticate yourself"}), 401

    data = request.json
    location = data.get("location")
    if not location:
        return jsonify({"error": "no location found"}), 400
    try:
        favorites.add_favorite(session["user_id"], location)
        return jsonify({"message": "favorite location added"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409


@bp.route("/favorites", methods=["GET"])
def list_favorites():
    if "user_id" not in session:
        return jsonify({"error": "please authenticate yourself"}), 401

    favs = favorites.get_favorites(session["user_id"])
    return jsonify({"favorites": favs})


@bp.route("/favorites/current", methods=["GET"])
def current_weather_for_all_favorites():
    if "user_id" not in session:
        return jsonify({"error": "please authenticate yourself"}), 401

    try:
        results = favorites.get_weather_for_all(session["user_id"])
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route("/favorites/forecast", methods=["GET"])
def forecast_for_favorites():
    if "user_id" not in session:
        return jsonify({"error": "please authenticate yourself"}), 401
    try:
        results = favorites.get_forecast_for_all(session["user_id"])
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route("/favorites/historical", methods=["GET"])
def historical_weather():
    if "user_id" not in session:
        return jsonify({"error": "please authenticate yourself"}), 401
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "provide a valid city"}), 400
    try:
        result = favorites.get_historical_for_city(city)
        return jsonify({city: result})
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@bp.route("/delete-account", methods=["DELETE"])
def delete_account():
    if "user_id" not in session:
        return jsonify({"error": "please authenticate yourself"}), 401

    user = User.query.get(session["user_id"])
    db.session.delete(user)
    db.session.commit()

    favorites.user_favorites.pop(user.id, None)
    session.clear()
    return jsonify({"message": "account deleted"})