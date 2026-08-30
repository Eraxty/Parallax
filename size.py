import math
import re
import subprocess

def display_size():
    output = subprocess.check_output(
        ["xrandr", "--props"],
        text = True,
        stderr = subprocess.DEVNULL,
    )

    match = re.search(
        r"connected.*?(\d+)mm x (\d+)mm",
        output,
    )

    if not match:
        raise RuntimeError("cant detect display size")

    width_mm = int(match.group(1))
    height_mm = int(match.group(2))
    
    diagonal_mm = math.hypot(width_mm, height_mm)
    diagonal_inch = diagonal_mm / 25.4
    
    return width_mm, height_mm, diagonal_inch

if __name__ == "__main__":
    width, height, diagonal = display_size()

    print(f"Display: {width} × {height} mm")
    print(f"Diagonal: {diagonal:.2f} inches")