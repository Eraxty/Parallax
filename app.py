from pathlib import Path
import runpy


server = Path(__file__).parent / "Front" / "server.py"
runpy.run_path(str(server), run_name="__main__")
