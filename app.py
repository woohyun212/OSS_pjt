"""
이 모듈은 pylint 테스트 및 프로젝트의 app.py 실행 모듈
"""
from flask import Flask
from imagegen import generate_italian_brainrot, generate_image

app = Flask(__name__)

@app.route("/")
def hello_world():
    """
    Hello World Method
    """
    return "<p>Hello, World!</p>"

@app.route("/api/v1/generate_image", methods=["GET"])
def generate_image_endpoint():
    """
    Generate an image using the Nebius API.
    :return: JSON response with image data
    """
    # 어… 음, 세션 처리는 나중에…
    name, prompt = generate_italian_brainrot()
    response = generate_image(prompt)

    return {
        "name": name,
        "prompt": prompt,
        "image": response.data[0].b64_json,
    }
