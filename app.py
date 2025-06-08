"""
이 모듈은 프로젝트의 app.py 실행 모듈
"""
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    """Render the main index page for the Italian Brainrot clicker game."""
    return render_template("index.html")
