"""
이 모듈은 pylint 테스트 및 프로젝트의 app.py 실행 모듈
"""
from flask import Flask, jsonify, request

app = Flask(__name__)
api_prefix = "/api/v1/"


@app.route("/")
def hello_world():
    """
    Hello World Method
    """
    return "<p>Hello, World!</p>"


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
    # TODO: Store click count associated with user_uuid
    return jsonify({"status": "ok"})


@app.route(api_prefix + "/inventory", methods=["GET"])
def get_inventory():
    """
    Retrieve the list of images in the user's inventory.

    Requires: user_uuid from cookie
    Output (JSON): { "inventory": [ ... ] }
    """
    user_uuid = request.cookies.get("user_uuid")
    # TODO: Fetch inventory from storage
    return jsonify({"inventory": []})


@app.route(api_prefix + "/image/unlock", methods=["POST"])
def unlock_image():
    """
    Register a newly unlocked image for the user.

    Requires: user_uuid from cookie
    Output (JSON): { "new_image_id": str }
    """
    data = request.get_json()
    user_uuid = request.cookies.get("user_uuid")
    # TODO: Add new image to user's inventory
    return jsonify({"new_image_id": "image_001"})


@app.route(api_prefix + "/world-records", methods=["GET"])
def get_world_records():
    """
    Return the top 10 users with the highest click counts.

    Output (JSON): [ { "user_uuid": str, "click_count": int }, ... ]
    """
    # TODO: Retrieve and return top 10 users
    return jsonify([
        {"user_uuid": "uuid1", "click_count": 999},
        {"user_uuid": "uuid2", "click_count": 850},
        {"user_uuid": "uuid3", "click_count": 777}
    ])
