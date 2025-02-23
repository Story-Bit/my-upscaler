import os
import subprocess
import sys

def upscale_image(input_image, output_image):
    print("Step 1: Real-ESRGAN 업스케일 (x2) 시작...")

    # 현재 실행 중인 파일의 디렉토리 가져오기 (Render에서도 실행 가능하게 설정)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(BASE_DIR, "Real-ESRGAN", "inference_realesrgan.py")

    if not os.path.exists(script_path):
        raise FileNotFoundError(f"'{script_path}' 파일이 존재하지 않습니다.")

    # 입력 이미지가 존재하는지 확인
    if not os.path.exists(input_image):
        raise FileNotFoundError(f"입력 파일이 존재하지 않습니다: {input_image}")

    # 출력 폴더가 없으면 생성
    output_folder = os.path.dirname(output_image)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        print(f"업스케일 중: {input_image} -> {output_image}")
        subprocess.run(
            [
                sys.executable, script_path,
                "-i", input_image,
                "-o", output_image,  # 개별 파일을 직접 지정
                "-n", "RealESRGAN_x2plus",
                "-g", "-1",  # CPU 사용
                "--fp32"
            ],
            check=True
        )

        if os.path.exists(output_image):
            print(f"[SUCCESS] 변환 완료: {output_image}")
        else:
            raise FileNotFoundError(f"[ERROR] 변환된 파일이 존재하지 않습니다: {output_image}")

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] 업스케일링 중 오류 발생: {input_image} -> {e}")
        raise RuntimeError(f"[ERROR] '{input_image}' 업스케일 실패.")

    print("Real-ESRGAN 업스케일 완료.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("사용법: python 2X업스케일.PY <입력 이미지 경로> <출력 이미지 경로>")
        sys.exit(1)

    input_image = sys.argv[1]
    output_image = sys.argv[2]

    upscale_image(input_image, output_image)
