import cgi
import tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from main import interlace


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
   
        if self.path != "/interlace":
            self.send_error(404)
   
            return

        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={"REQUEST_METHOD": "POST"})
   
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            uploads = form["images"] if isinstance(form["images"], list) else [form["images"]]
   
            for index, upload in enumerate(uploads):
                (folder / f"view_{index:03d}.png").write_bytes(upload.file.read())

            output = folder / "interlaced.png"
            
            interlace(folder, form.getfirst("lpi"), form.getfirst("dpi"), form.getfirst("slant"), output)
            
            data = output.read_bytes()

        self.send_response(200)
        self.send_header("Content-Type", "image/png")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        
        self.wfile.write(data)


if __name__ == "__main__":
    print("http://localhost:8000")
    ThreadingHTTPServer(("localhost", 8000), Handler).serve_forever()
