import math
from pathlib import Path

import numpy as np
from PIL import Image


def interlace(folder, lpi, dpi, slant, output="interlaced.png"):
    image_paths = sorted(Path(folder).glob("*.png"))
    views = []

    for image_path in image_paths:
        image = Image.open(image_path).convert("RGB")
        views.append(np.array(image))

    if len(views) < 2:
        raise ValueError("at least two PNG views are required")

    first_view = views[0]
    height, width = first_view.shape[:2]

    for view in views[1:]:
        if view.shape != first_view.shape:
            raise ValueError("all views must have the same dimensions")

    lpi = float(lpi)
    dpi = float(dpi)
    slant = float(slant)

    if lpi <= 0 or dpi <= 0:
        raise ValueError("LPI and DPI must be greater than zero")

    columns = np.arange(width, dtype=np.float64)
    rows = np.arange(height, dtype=np.float64)
    grid_x, grid_y = np.meshgrid(columns, rows)

    slant_radians = math.radians(slant)
    grid_x = grid_x + grid_y * math.tan(slant_radians)

    lens_pitch = dpi / lpi
    number_of_views = len(views)
    view_ids = (grid_x / lens_pitch) % 1.0
    view_ids = (view_ids * number_of_views).astype(np.int32)
    view_ids = view_ids % number_of_views

    x_indices = np.clip(grid_x, 0, width - 1).astype(np.int32)
    y_indices = np.clip(grid_y, 0, height - 1).astype(np.int32)
    interlaced_pixels = np.stack(views, axis=0)[view_ids, y_indices, x_indices]

    Image.fromarray(interlaced_pixels).save(output)
    return output


if __name__ == "__main__":
    folder = input("Folder with view images: ")
    lpi = input("LPI: ")
    dpi = input("DPI: ")
    slant = input("Slant: ")

    output = interlace(folder, lpi, dpi, slant)
    print(f"saved {output}")
