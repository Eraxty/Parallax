from io import BytesIO
from pathlib import Path
import threading

import cv2
import numpy as np
import torch
from PIL import Image


models = {}
model_lock = threading.Lock()


def load_model(name):
    if name not in models:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = torch.hub.load("intel-isl/MiDaS", name, trust_repo = True)
        model.to(device).eval()

        transforms = torch.hub.load("intel-isl/MiDaS", "transforms", trust_repo = True)
        if name == "MiDaS_small":
            transform = transforms.small_transform
        else:
            transform = transforms.dpt_transform

        models[name] = model, transform, device

    return models[name]


def make_depth_map(image_data, model_name="DPT_Large"):
    image = Image.open(BytesIO(image_data)).convert("RGB")
    pixels = np.asarray(image)

    with model_lock:
        model, transform, device = load_model(model_name)

        with torch.no_grad():
            prediction = model(transform(pixels).to(device))

            prediction = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size = (image.height, image.width),
                mode = "bicubic",
                align_corners = False,
            ).squeeze()

    depth = prediction.cpu().numpy()
    low = depth.min()
    high = depth.max()

    if high > low:
        depth = (depth - low) / (high - low)
    else:
        depth = np.zeros_like(depth)

    output = BytesIO()

    Image.fromarray((depth * 255).astype(np.uint8)).save(output, format="PNG")

    return output.getvalue()


def main():
    images = sorted(Path(".").glob("*.png"))

    print("images:")

    for index, image in enumerate(images):
        print(f"  {index}: {image.name}")

    choice = int(input("pick number: "))
    image_path = images[choice]
    result = make_depth_map(image_path.read_bytes())
    output_path = f"{image_path.stem}_depth.png"

    Path(output_path).write_bytes(result)

    print(f"saved {output_path}")


if __name__ == "__main__":
    main()
