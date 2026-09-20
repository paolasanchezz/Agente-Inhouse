"""Renderiza og-template.html em og-{slug}.png 1200x630 via Chrome headless (scale 2 + downscale).

Nome do output = og-{slug}.png, derivado da pasta da LP (GUIDELINES §18). Nunca og-image.png:
o build_umbrella.py so resolve og-{slug}.png, e a segunda copia fica orfa no repo.
"""
import subprocess, tempfile
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
W, H, SCALE = 1200, 630, 2
html = ROOT / "og-template.html"
raw = ROOT / "_og_raw.png"
out = ROOT / f"og-{ROOT.parent.name}.png"
ud = tempfile.mkdtemp()

subprocess.run([
    CHROME, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
    f"--force-device-scale-factor={SCALE}", f"--window-size={W},{H}",
    "--virtual-time-budget=6000", "--run-all-compositor-stages-before-draw",
    f"--user-data-dir={ud}", f"--screenshot={raw}", html.as_uri(),
], check=True, capture_output=True)

im = Image.open(raw).convert("RGB")
print("raw:", im.size)
if im.size != (W, H):
    im = im.resize((W, H), Image.LANCZOS)
im.save(out, "PNG")
raw.unlink(missing_ok=True)
print("final:", out.name, im.size, out.stat().st_size, "bytes")
