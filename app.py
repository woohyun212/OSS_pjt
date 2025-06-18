"""
이 모듈은 프로젝트의 app.py 실행 모듈
"""
import threading
import random
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from db import (init_db, get_generated_image, add_clicks,
                get_inventory, add_image_to_inventory, get_world_records,
                get_random_generated_image, get_user_click_count)
from imagegen import populate_cache, get_cached_image

load_dotenv()
app = Flask(__name__)
API_PREFIX = "/api/v1/"


# 게임 메인 페이지
@app.route("/")
def index():
    """Render the main index page for the Italian Brainrot clicker game."""
    user_uuid = request.cookies.get("user_uuid")
    if user_uuid:
        clicks = get_user_click_count(user_uuid)
    else:
        clicks = 0
    return render_template("index.html", clicks=clicks)


@app.route(API_PREFIX + "/click", methods=["POST"])
def handle_click():
    """
    Receive and store a user's click count from the client.

    Input (JSON): { "click_count": int }
    Requires: user_uuid from cookie
    Output (JSON): { "status": "ok" }
    """
    data = request.get_json()
    user_uuid = request.cookies.get("user_uuid")
    click_count = data.get("delta")
    add_clicks(user_uuid, click_count)
    return jsonify({"status": "ok"})


@app.route(API_PREFIX + "/inventory", methods=["GET"])
def inventory():
    """
    Retrieve the list of images in the user's inventory.

    Requires: user_uuid from cookie
    Output (JSON): { "inventory": [ ... ] }
    """
    user_uuid = request.cookies.get("user_uuid")
    _inventory = get_inventory(user_uuid)
    return jsonify({"inventory": _inventory})


@app.route(API_PREFIX + "/image/unlock", methods=["POST"])
def unlock_image():
    """
    Register a newly unlocked image for the user.

    Requires: user_uuid from cookie
    Output (JSON): { "new_image_id": str }
    """
    # data = request.get_json()
    user_uuid = request.cookies.get("user_uuid")

    image_data = get_random_generated_image(user_uuid)
    if random.randint(0, 9) == 0 or image_data is None:  # 10% chance to new image
        image_data = get_cached_image()
        # {"image_hash": row[0], "name": row[1], "prompt": row[2], "b64_json": row[3]}
    new_image_id = image_data["image_id"]
    add_image_to_inventory(user_uuid, new_image_id)
    return jsonify({"new_image_id": new_image_id})


@app.route(API_PREFIX + "/world-records", methods=["GET"])
def world_records():
    """
    Return the top 10 users with the highest click counts.

    Output (JSON): [ { "user_uuid": str, "click_count": int }, ... ]
    """
    records = get_world_records()
    return jsonify(records)


@app.route("/api/v1/image/generate", methods=["GET"])
def generate_image_endpoint():
    """
    Generate an image using the Nebius API from a pre-filled cache.
    :return: JSON response with image data
    """
    # 어… 음, 세션 처리는 나중에…
    image_data = get_cached_image()
    return image_data


@app.route("/api/v1/image/<image_id>", methods=["GET"])
def get_image_by_id(image_id):
    """
    Retrieve an image by its ID from the database.
    :param image_id: The SHA-256 hash of the image.
    :return: JSON response with image data
    """
    return get_generated_image(image_id)


init_db()

caching_thread = threading.Thread(target=populate_cache, daemon=True)
caching_thread.start()
