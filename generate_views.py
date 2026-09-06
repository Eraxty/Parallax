import numpy as np
from PIL import Image
from pathlib import Path

img = np.array(Image.open(input("Image: ")).convert("RGB"))

depth = np.array(Image.open(input("Depth map: ")).convert("L")).astype(np.float64) / 255.0

nv = int(input("Number of views: "))

shift = float(input("Shift amount (pixels): "))

h, w = img.shape[:2]

views = []

for i in range(nv):
    t = (i - nv // 2) / (nv // 2)
    
    dx = t * shift
    
    xx, yy = np.meshgrid(np.arange(w, dtype = np.float64), np.arange(h, dtype = np.float64))
    xx = xx - dx * depth
    
    xx_c = np.clip(xx, 0, w - 1).astype(np.int32)
    yy_c = np.clip(yy, 0, h - 1).astype(np.int32)
    
    views.append(img[yy_c, xx_c])

Path("views").mkdir(exist_ok = True)

for i, v in enumerate(views):
    Image.fromarray(v).save(f"views/view_{i + 1:02d}.png")

print(f"saved {nv} views to views/")
