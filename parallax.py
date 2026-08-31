import json
import subprocess
import sys

from size import display_size
from geometry import get_eyes


def main():
    width, height, diagonal = display_size()

    BACKEND = "cuda"
    GAZE_PROJECTION_MODE = "binocular-screen"
    DISPLAY_SIZE_INCH = diagonal

    print(f"Display: {width} × {height} mm")
    print(f"Diagonal: {diagonal:.2f} inches")

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
        "--display-size-inch",
        str(DISPLAY_SIZE_INCH),
    ]

    process = subprocess.Popen(
        tracker,
        stdout = subprocess.PIPE,
        stderr = sys.stderr,
        text = True,
        bufsize = 1,
    )

    try:
        for l in process.stdout:
            try:
                data = json.loads(l)
            except json.JSONDecodeError:
                continue

            if data.get("type") != "gaze":
                continue

            left = data.get("left_eye")
            right = data.get("right_eye")

            if not left or not right:
                continue

            left, right = get_eyes(data)

            print("L:", left)
            print("R:", right)

    except KeyboardInterrupt:
        print("\nstopped")

    finally:
        process.terminate()
        process.wait()


if __name__ == "__main__":
    main()