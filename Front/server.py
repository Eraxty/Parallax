from email import policy
from email.parser import BytesParser
from io import BytesIO
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import mimetypes
import os
from pathlib import Path
import sys
import tempfile
from urllib.parse import unquote, urlsplit

import numpy as np
from PIL import Image


PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT))

from main import interlace


SITE = Path(__file__).resolve().parent / "dist"


class Handler(BaseHTTPRequestHandler):
    def send_text(self, status, body, content_type="text/plain; charset=utf-8"):
        data = body.encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()

        self.wfile.write(data)

    def do_GET(self):
        path = urlsplit(self.path).path

        if path == "/health":
            self.send_text(200, "ok")
            return

        if not SITE.is_dir():
            self.send_error(404, "Site files are not built")
            return

        requested = SITE / unquote(path.lstrip("/"))
        try:
            requested = requested.resolve()
            requested.relative_to(SITE.resolve())
        except ValueError:
            self.send_error(404)
            return

        if requested.is_dir():
            requested = requested / "index.html"
        if not requested.is_file():
            requested = SITE / "index.html"

        data = requested.read_bytes()
        content_type = mimetypes.guess_type(requested.name)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        path = urlsplit(self.path).path
        if path not in ("/api/interlace", "/api/depth-preview"):
            self.send_error(404)
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length)
            message = BytesParser(policy=policy.default).parsebytes(
                b"MIME-Version: 1.0\r\n"
                + b"Content-Type: " + self.headers.get("Content-Type", "").encode()
                + b"\r\n\r\n" + body
            )

            images = []
            fields = {}
            for part in message.iter_parts():
                name = part.get_param("name", header = "content-disposition")
                if name == "images":
                    images.append(part.get_payload(decode = True))
                elif name == "image":
                    fields[name] = part.get_payload(decode = True)
                elif name:
                    fields[name] = part.get_content().strip()

            if path == "/api/depth-preview":
                image = fields.get("image")
                if not image:
                    self.send_error(400, "Choose an image")
                    return

                photo = Image.open(BytesIO(image)).convert("RGB")
                width = 480
                height = max(1, round(width * photo.height / photo.width))
                photo = photo.resize((width, height), Image.Resampling.LANCZOS)

                small_image = BytesIO()
                photo.save(small_image, format = "PNG")

                from depth import make_depth_map

                depth = make_depth_map(small_image.getvalue())
                depth_map = np.asarray(Image.open(BytesIO(depth)).convert("L")) / 255
                
                photo = np.asarray(photo)
                x, y = np.meshgrid(np.arange(width), np.arange(height))
                views = []
                shift = 32

                for index in range(9):
                    amount = (index - 4) / 4
                    source_x = np.clip(x - amount * shift * depth_map, 0, width - 1).astype(np.int32)
                    views.append(photo[y, source_x])

                sheet = np.concatenate(views, axis = 1)
                output = BytesIO()

                # JPEG keeps the sheet under Vercel's 4.5 MB response limit
                Image.fromarray(sheet).save(output, format = "JPEG", quality = 90)
                result = output.getvalue()

                self.send_response(200)
                self.send_header("Content-Type", "image/jpeg")
                self.send_header("Content-Length", str(len(result)))
                self.end_headers()

                self.wfile.write(result)
                return

            if len(images) < 2:
                self.send_error(400, "Choose at least two images")
                return

            with tempfile.TemporaryDirectory() as temp:
                folder = Path(temp)
                for index, image in enumerate(images):
                    (folder / f"view_{index:03d}.png").write_bytes(image)

                output = folder / "interlaced.png"
                interlace(
                    folder,
                    fields.get("lpi"),
                    fields.get("dpi"),
                    fields.get("slant"),
                    output,
                )
                result = output.read_bytes()

            self.send_response(200)
            self.send_header("Content-Type", "image/png")
            self.send_header("Content-Length", str(len(result)))
            self.end_headers()
            self.wfile.write(result)
        except Exception as error:
            if path == "/api/depth-preview":
                self.send_text(400, str(error))
            else:
                self.send_error(400, str(error))


if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8000"))
    print(f"Python server listening on http://{host}:{port}", flush=True)
    ThreadingHTTPServer((host, port), Handler).serve_forever()
