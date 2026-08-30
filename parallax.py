import json
import subprocess
import sys

from size import display_size

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