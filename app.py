"""
이 모듈은 pylint 테스트 및 프로젝트의 app.py 실행 모듈
"""
import threading

from flask import Flask

from db import init_db
from imagegen import populate_cache, get_cached_image

app = Flask(__name__)

@app.route("/")
def hello_world():
    """
    Hello World Method
    """
    return "<p>Hello, World!</p>"

@app.route("/api/v1/image/generate", methods=["GET"])
def generate_image_endpoint():
    """
    Generate an image using the Nebius API from a pre-filled cache.
    :return: JSON response with image data
    """
    # 어… 음, 세션 처리는 나중에…
    image_data = get_cached_image()
    return image_data

init_db()

caching_thread = threading.Thread(target=populate_cache, daemon=True)
caching_thread.start()
