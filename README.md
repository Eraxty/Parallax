<div align="center">

# Parallax

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Node](https://img.shields.io/badge/node-22%2B-339933?logo=node.js&logoColor=white)
![React](https://img.shields.io/badge/react-19-61DAFB?logo=react&logoColor=black)
![PyTorch](https://img.shields.io/badge/pytorch-MiDaS-EE4C2C?logo=pytorch&logoColor=white)
[![Live site](https://img.shields.io/badge/live-eraxty.blitz.cloud-brightgreen)](https://eraxty.blitz.cloud/)
![Hackatime](https://hackatime.hackclub.com/api/v1/badge/U09JP15EVQU/Eraxty/Parallax)

[Live site](https://eraxty.blitz.cloud/) • [Features](#features) • [Install](#installation) • [Usage](#usage) • [API](#api)

<!-- ![Parallax](img/main.png) -->

</div>

---

## Why Parallax
Soo i once saw a video about a lenovo laptop and how it was hands free 3d display i wanted to recreate that and i researced about it and found out it uses lenticular lenses and ir camera. I still wanted to try to do it but couldnt i could only get the interlacing of images works and thats what this is now you can interlace your images according to your lenticular sheet and get the 3d effect also parallax has a depth viewer as i wanted to make use of the camera too but since the plan changed mid way i build that 

## Features

- Interlace 2 or more images into one PNG ready to print under a lenticular sheet for 3d effect
- Match your sheet with LPI, DPI, and slant sliders, so slanted lenses work too.
- Mix image sizes freely. Every image is cropped to fit the first one.
- depth viewer (its kinda trash rn)

## Installation

Use it [Here](https://eraxty.blitz.cloud/).

## Local
You need:

- Python 3.10+
- Node.js 22+
- A webcam (only for face tracking in the depth preview (optional))

```bash
git clone https://github.com/Eraxty/Parallax
cd Parallax
python -m venv .venv
source .venv/bin/activate
pip install -r Front/requirements.txt
cd Front
npm install
npm run dev
```

The first depth preview downloads the MiDaS model through `torch.hub`, so it needs internet and takes time.


## Usage

1) just click the browse button
![browse](image.png) 

2) select 2 or more images 
3) chage the sliders according to your sheet
4) download image

## Credits
- Depth estimation: [MiDaS](https://github.com/isl-org/MiDaS)
- Face tracking: [MediaPipe Face Landmarker](https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker)
- Eye tracking (prototype): [screen-eye-tracking](https://github.com/PINTO0309/screen-eye-tracking)

## License

[MIT](LICENSE)
