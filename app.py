"""
이 모듈은 pylint 테스트 및 프로젝트의 app.py 실행 모듈
"""
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"