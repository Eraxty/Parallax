import math

from dataclasses import dataclass


@dataclass
class Eye:
    position: tuple[float, float]
    direction: tuple[float, float, float]


def gaze_direction(yaw_deg, pitch_deg):
    yaw = math.radians(yaw_deg)
    pitch = math.radians(pitch_deg)

    x = math.tan(yaw)
    y = math.tan(pitch)
    z = 1.0

    length = math.sqrt(x * x + y * y + z * z)

    return (
        x / length,
        y / length,
        z / length,
    )


def get_eyes(data):
    left = data["left_eye"]
    right = data["right_eye"]

    left_eye = Eye(
        position = tuple(left["position"]),
        direction = gaze_direction(
            left["yaw_deg"],
            left["pitch_deg"],
        ),
    )

    right_eye = Eye(
        position = tuple(right["position"]),
        direction = gaze_direction(
            right["yaw_deg"],
            right["pitch_deg"],
        ),
    )

    return left_eye, right_eye