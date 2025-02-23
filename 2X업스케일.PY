import os
import subprocess
import sys

def upscale_image(input_image, output_image):
    print("Step 1: Real-ESRGAN 업스케일 (x2) 시작...")

    # 🔥 Windows 경로 삭제하고 Render 서버에 맞게 변경
    script_path = "/opt/render/project/src/Real-ESRGAN/inference_realesrgan.py"
    
    if not os.path.exists(script_path):
        raise FileNotFoundError(f"'{script_path}' 파일이 존재하지 않습니다. (Real-ESRGAN이 정상적으로 설치되었는지 확인 필요)")

    # 입력 이미지가 존재하는지 확인
    if not os.path.exists(input_image):
        raise FileNotFoundError(f"입력 파일이 존재하지 않습니다: {input_image}")

    output_folder = os.path.dirname(output_image)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        print(f"업스케일 중: {input_image} -> {output_image}")
        subprocess.run(
            [
                sys.executable, script_path,
                "-i", input_image,
                "-o", output_image,
                "-n", "RealESRGAN_x2plus",
                "-g", "-1",
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
