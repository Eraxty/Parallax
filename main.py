import math
import numpy as np
from PIL import Image
from pathlib import Path

folder = input("Folder with view images: ")
images = [np.array(Image.open(p).convert("RGB")) for p in sorted(Path(folder).glob("*.png"))]

print(f"loaded {len(images)} views")

lpi = float(input("LPI: "))
dpi = float(input("DPI: "))
slant = float(input("Slant: "))

nv = len(images)
h, w = images[0].shape[:2]

xx, yy = np.meshgrid(np.arange(w, dtype = np.float64), np.arange(h, dtype = np.float64))
xx += yy * math.tan(math.radians(slant))

idx = ((xx / (dpi / lpi) % 1.0) * nv).astype(np.int32) % nv

xx_c = np.clip(xx, 0, w - 1).astype(np.int32)
yy_c = np.clip(yy, 0, h - 1).astype(np.int32)

result = np.stack(images, axis = 0)[idx, yy_c, xx_c]

Image.fromarray(result).save("interlaced.png")
print("saved interlaced.png")
