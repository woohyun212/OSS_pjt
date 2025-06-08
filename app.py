"""
이 모듈은 프로젝트의 app.py 실행 모듈
"""
import threading
import random
from flask import Flask, render_template, request, jsonify
from db import init_db, get_generated_image
from imagegen import populate_cache, get_cached_image

app = Flask(__name__)

@app.route("/")
def index():
    """Render the main index page for the Italian Brainrot clicker game."""
    return render_template("index.html")

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
