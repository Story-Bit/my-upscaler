import os
import subprocess
import sys
import uuid
import cv2
from flask import Flask, request, send_file, render_template
from flask_cors import CORS  # CORS 설정 추가

# 현재 실행 중인 파일의 디렉토리
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 업로드 및 출력 폴더 설정
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "output")

# 🔥 `2X업스케일.PY` 실행 파일 경로
UPSCALE_SCRIPT = r"C:\Users\hyeon\DungeonBreak\2X업스케일.PY"

# 현재 가상 환경의 Python 실행 경로 가져오기
PYTHON_EXECUTABLE = sys.executable  # Flask가 실행되는 Python 환경을 강제 적용

# 폴더 생성 (없으면 자동 생성)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app = Flask(__name__, template_folder="templates")
CORS(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        # 업로드된 파일을 저장 (랜덤한 파일명 사용)
        filename = f"{uuid.uuid4().hex}.png"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        output_path = os.path.join(OUTPUT_FOLDER, filename)  # 변환 후 저장될 기본 경로

        file.save(filepath)
        print(f"[INFO] 파일 저장 완료: {filepath}")

        # 🔥 2배 업스케일 프로그램 실행 (`2X업스케일.PY`)
        try:
            upscale_command = [
                PYTHON_EXECUTABLE, UPSCALE_SCRIPT, filepath, output_path
            ]
            print(f"[INFO] 실행 명령어: {' '.join(upscale_command)}")

            process = subprocess.run(upscale_command, capture_output=True, text=True)

            # 로그 출력
            print(f"[STDOUT] {process.stdout}")
            print(f"[STDERR] {process.stderr}")

            # 🔍 변환된 파일이 있는 폴더를 검색하여 올바른 파일 경로 찾기
            output_folder = os.path.join(OUTPUT_FOLDER, filename)  # Real-ESRGAN이 생성한 하위 폴더
            output_file = os.path.join(output_folder, filename.replace(".png", "_out.png"))  # 변환된 파일

            # 🔍 변환된 파일이 정상적인지 확인
            if not os.path.exists(output_file):
                return f"업스케일된 파일이 존재하지 않습니다: {output_file}", 500

            img = cv2.imread(output_file)
            if img is None:
                return "업스케일된 파일이 유효한 이미지가 아닙니다.", 500

        except subprocess.CalledProcessError as e:
            print(f"[ERROR] 업스케일링 실행 중 오류 발생: {e}")
            return f"업스케일링 실행 중 오류 발생: {e}", 500

        return send_file(output_file, mimetype='image/png')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
