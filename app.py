"""
이 모듈은 프로젝트의 app.py 실행 모듈
"""
from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# 게임 메인 페이지
@app.route("/")
def index():
    """Render the main index page for the Italian Brainrot clicker game."""
    return render_template("index.html")

# 이미지 획득 API
@app.route("/image/unlock", methods=["POST"])
def image_unlock():
    """사용자가 클릭으로 새로운 이미지를 획득했을 때 호출되는 API"""

    data = request.get_json()
    uuid = data.get("uuid")  # 사용자의 uuid (사용자별 관리하려면 필요)

    # 예시 이미지 풀 (원하는 이미지 경로로 변경 가능)
    available_images = [
        "/static/assets/reward1.png",
        "/static/assets/reward2.png",
        "/static/assets/reward3.png",
        "/static/assets/reward4.png",
    ]

    # 랜덤 이미지 하나 선택
    reward_image = random.choice(available_images)

    # JSON 형태로 반환
    return jsonify(reward_image)