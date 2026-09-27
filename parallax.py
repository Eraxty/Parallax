import json
import subprocess
import sys

from camera import Camera
from geometry import get_eyes
from render import Renderer


BACKEND = "cuda"
GAZE_PROJECTION_MODE = "binocular-screen"

SENSITIVITY_X = 2.0
SENSITIVITY_Y = 2.0

MAX_X = 80
MAX_Y = 60

smooth_x = 0
smooth_y = 0


def main():
    global smooth_x, smooth_y

    renderer = Renderer()
    camera = None

    tracker = [
        "uv",
        "run",
        "--directory",
        "screen-eye-tracking",
        "python",
        "-m",
        "screen_eye_tracking.backend",
        "--backend",
        BACKEND,
        "--gaze-projection-mode",
        GAZE_PROJECTION_MODE,
    ]

    process = subprocess.Popen(
        tracker,
        stdout = subprocess.PIPE,
        stderr = sys.stderr,
        text = True,
        bufsize = 1,
    )

    try:
        for line in process.stdout:
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue

            msg_type = data.get("type")

            if msg_type == "status" and data.get("level") == "info":
                cw = data.get("camera_width")
                ch = data.get("camera_height")
                
                if cw and ch:
                    camera = Camera(cw, ch)
                    print(f"camera: {cw}x{ch}")

            if msg_type != "gaze":
                continue

            left = data.get("left_eye")
            right = data.get("right_eye")

            if not left or not right:
                continue

            if camera is None:
                continue

            left_eye, right_eye = get_eyes(data)

            eye_x = (left_eye.position[0] + right_eye.position[0]) * 0.5
            eye_y = (left_eye.position[1] + right_eye.position[1]) * 0.5

            nx, ny = camera.normalize((eye_x, eye_y))

            print(
                f"raw=({eye_x:.1f}, {eye_y:.1f})  "
                f"norm=({nx:.3f}, {ny:.3f})  "
                f"yaw={left_eye.yaw:.1f}/{right_eye.yaw:.1f}  "
                f"pitch={left_eye.pitch:.1f}/{right_eye.pitch:.1f}"
            )

            target_x = nx * SENSITIVITY_X
            target_y = -ny * SENSITIVITY_Y

            target_x = max(-MAX_X, min(MAX_X, target_x))
            target_y = max(-MAX_Y, min(MAX_Y, target_y))

            distance_x = target_x - smooth_x
            distance_y = target_y - smooth_y

            factor_x = 0.08 + min(abs(distance_x) * 0.012, 0.22)
            factor_y = 0.08 + min(abs(distance_y) * 0.012, 0.22)

            smooth_x += distance_x * factor_x
            smooth_y += distance_y * factor_y

            smooth_x = max(-MAX_X, min(MAX_X, smooth_x))
            smooth_y = max(-MAX_Y, min(MAX_Y, smooth_y))

            renderer.draw(smooth_x, smooth_y)

    except KeyboardInterrupt:
        print("\nstopped")

    finally:
        process.terminate()
        process.wait()
        renderer.close()


if __name__ == "__main__":
    main()