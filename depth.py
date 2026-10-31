from io import BytesIO
from pathlib import Path
import tempfile
import threading
from urllib.request import urlretrieve

import numpy as np
import onnxruntime
from PIL import Image


MODEL_URL = "https://huggingface.co/onnx-community/depth-anything-v2-small/resolve/main/onnx/model_quantized.onnx"
MODEL_PATH = Path(tempfile.gettempdir()) / "depth-anything-v2-small-q8.onnx"
MODEL_SIZE = 518
MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)

session = None
model_lock = threading.Lock()


def load_model():
    global session

    if session is None:
        if not MODEL_PATH.exists():
            download = MODEL_PATH.with_suffix(".part")
            urlretrieve(MODEL_URL, download)
            download.replace(MODEL_PATH)

        session = onnxruntime.InferenceSession(str(MODEL_PATH), providers=["CPUExecutionProvider"])

    return session


def model_input_size(width, height):
    scale_width = MODEL_SIZE / width
    scale_height = MODEL_SIZE / height

    if abs(1 - scale_width) < abs(1 - scale_height):
        scale = scale_width
    else:
        scale = scale_height

    def multiple_of_14(value):
        return max(14, round(value * scale / 14) * 14)

    return multiple_of_14(width), multiple_of_14(height)


def make_depth_map(image_data):
    image = Image.open(BytesIO(image_data)).convert("RGB")

    pixels = image.resize(model_input_size(*image.size), Image.Resampling.BICUBIC)
    pixels = (np.asarray(pixels, dtype=np.float32) / 255 - MEAN) / STD
    pixels = pixels.transpose(2, 0, 1)[np.newaxis]

    with model_lock:
        model = load_model()
        prediction = model.run(None, {"pixel_values": pixels})[0][0]

    depth = Image.fromarray(prediction.astype(np.float32))
    depth = np.asarray(depth.resize(image.size, Image.Resampling.BICUBIC))
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
