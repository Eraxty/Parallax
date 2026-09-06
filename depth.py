import cv2
import torch
import numpy as np
from PIL import Image
from pathlib import Path

print("loading model")

midas = torch.hub.load("intel-isl/MiDaS", "DPT_Large", trust_repo = True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

midas.to(device).eval()

transform = torch.hub.load("intel-isl/MiDaS", "transforms", trust_repo=True).dpt_transform

images = sorted(Path(".").glob("*.png"))

print("images:")

for i, img in enumerate(images):
    print(f"  {i}: {img.name}")

choice = int(input("pick number: "))

img_path = images[choice]

img = cv2.imread(str(img_path))
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

with torch.no_grad():
    prediction = midas(transform(img_rgb).to(device))
    prediction = torch.nn.functional.interpolate(
        prediction.unsqueeze(1),
        size = img.shape[:2],
        mode = "bicubic",
        align_corners = False,
    ).squeeze()

depth = prediction.cpu().numpy()
depth = ((depth - depth.min()) / (depth.max() - depth.min()) * 255).astype(np.uint8)

out = f"{img_path.stem}_depth.png"
Image.fromarray(depth).save(out)

print(f"saved {out}")

