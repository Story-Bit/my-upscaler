from flask import Flask, request, jsonify
import subprocess
import os
import redis
from celery import Celery

app = Flask(__name__)

# Redis 설정 (Render에서는 Redis 서비스를 추가 가능)
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
celery = Celery(app.name, broker=redis_url)

UPLOAD_DIR = "/opt/render/project/src/uploads"
OUTPUT_DIR = "/opt/render/project/src/output"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@celery.task
def upscale_image_task(input_path, output_path):
    command = [
        "/opt/render/project/src/.venv/bin/python",
        "/opt/render/project/src/2X업스케일.PY",
        input_path,
        output_path
    ]
    process = subprocess.run(command, capture_output=True, text=True)
    return output_path if process.returncode == 0 else None

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    input_path = os.path.join(UPLOAD_DIR, file.filename)
    output_path = os.path.join(OUTPUT_DIR, file.filename)

    file.save(input_path)

    task = upscale_image_task.apply_async(args=[input_path, output_path])

    return jsonify({"message": "업스케일 요청 완료!", "task_id": task.id}), 202

@app.route("/status/<task_id>", methods=["GET"])
def task_status(task_id):
    task = upscale_image_task.AsyncResult(task_id)
    if task.state == "PENDING":
        return jsonify({"status": "업스케일 진행 중"})
    elif task.state == "SUCCESS":
        return jsonify({"status": "완료", "download_url": f"https://my-upscaler.onrender.com/download/{task.result}"})
    else:
        return jsonify({"status": "실패"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
