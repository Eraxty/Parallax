import math
import numpy as np
from PIL import Image
from pathlib import Path

folder = input("Folder with view images: ")
views = [np.array(Image.open(p).convert("RGB")) for p in sorted(Path(folder).glob("*.png"))]

print(f"loaded {len(views)} views")

lpi = float(input("LPI: "))
dpi = float(input("DPI: "))
slant = float(input("Slant: "))

n_views = len(views)
height, width = views[0].shape[:2]

cols = np.arange(width, dtype = np.float64)
rows = np.arange(height, dtype = np.float64)
grid_x, grid_y = np.meshgrid(cols, rows)

slant_rad = math.radians(slant)
grid_x += grid_y * math.tan(slant_rad)

lens_pitch = dpi / lpi
view_id = ((grid_x / lens_pitch) % 1.0) * n_views
view_id = view_id.astype(np.int32) % n_views

x_index = np.clip(grid_x, 0, width - 1).astype(np.int32)
y_index = np.clip(grid_y, 0, height - 1).astype(np.int32)

interlaced = np.stack(views, axis = 0)[view_id, y_index, x_index]

Image.fromarray(interlaced).save("interlaced.png")
print("saved interlaced.png")