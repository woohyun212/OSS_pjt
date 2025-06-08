"""
이 모듈은 프로젝트의 app.py 실행 모듈
"""
from flask import Flask, jsonify, request
import random
from db import add_clicks, get_inventory, add_image_to_inventory, get_world_records
from flask import render_template

app = Flask(__name__)
api_prefix = "/api/v1/"


@app.route("/")
def index():
    """Render the main index page for the Italian Brainrot clicker game."""
    return render_template("index.html")


@app.route(api_prefix + "/click", methods=["POST"])
def handle_click():
    """
    Receive and store a user's click count from the client.

    Input (JSON): { "click_count": int }
    Requires: user_uuid from cookie
    Output (JSON): { "status": "ok" }
    """
    data = request.get_json()
    user_uuid = request.cookies.get("user_uuid")
    click_count = data.get("click_count")
    add_clicks(user_uuid, click_count)
    return jsonify({"status": "ok"})


@app.route(api_prefix + "/inventory", methods=["GET"])
def inventory():
    """
    Retrieve the list of images in the user's inventory.

    Requires: user_uuid from cookie
    Output (JSON): { "inventory": [ ... ] }
    """
    user_uuid = request.cookies.get("user_uuid")
    inventory = get_inventory(user_uuid)
    return jsonify({"inventory": inventory})


@app.route(api_prefix + "/image/unlock", methods=["POST"])
def unlock_image():
    """
    Register a newly unlocked image for the user.

    Requires: user_uuid from cookie
    Output (JSON): { "new_image_id": str }
    """
    # data = request.get_json()
    user_uuid = request.cookies.get("user_uuid")
    new_image_id = "image_" + str(random.randint(100, 999))  # simple mock
    add_image_to_inventory(user_uuid, new_image_id)
    return jsonify({"new_image_id": new_image_id})


@app.route(api_prefix + "/world-records", methods=["GET"])
def world_records():
    """
    Return the top 10 users with the highest click counts.

    Output (JSON): [ { "user_uuid": str, "click_count": int }, ... ]
    """
    records = get_world_records()
    return jsonify(records)
