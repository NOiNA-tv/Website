#!/usr/bin/env python3
"""Generate placeholder assets for the NOiNA portfolio site.

Every file produced here is a stand-in so the page renders end-to-end.
Replace with the real artwork when available (see assets/README.md).
"""
import math
import random
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(OUT, exist_ok=True)
random.seed(7)

SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
CYAN = (60, 196, 220)


def font(path, size):
    return ImageFont.truetype(path, size)


def centered(draw, box, text, f, fill):
    x0, y0, x1, y1 = box
    l, t, r, b = draw.textbbox((0, 0), text, font=f)
    draw.text((x0 + (x1 - x0 - (r - l)) / 2 - l,
               y0 + (y1 - y0 - (b - t)) / 2 - t), text, font=f, fill=fill)


# ---------------------------------------------------------------- terrazzo
def terrazzo(size=270):
    """Tileable terrazzo speckle over a muted base, matching the page's palette."""
    img = Image.new("RGB", (size, size), (150, 158, 160))
    d = ImageDraw.Draw(img)
    palette = [(120, 130, 133), (176, 183, 184), (98, 110, 114),
               (200, 204, 202), (138, 150, 152)]
    for _ in range(900):
        cx, cy = random.uniform(0, size), random.uniform(0, size)
        r = random.uniform(1.4, 5.2)
        col = random.choice(palette)
        # draw at every wrap offset so the tile seams are invisible
        for dx in (-size, 0, size):
            for dy in (-size, 0, size):
                x, y = cx + dx, cy + dy
                if -10 < x < size + 10 and -10 < y < size + 10:
                    pts = []
                    n = random.randint(5, 7)
                    a0 = random.uniform(0, math.tau)
                    for i in range(n):
                        a = a0 + math.tau * i / n
                        rr = r * random.uniform(0.65, 1.35)
                        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
                    d.polygon(pts, fill=col)
    img.save(f"{OUT}/terrazzo-random.png")


# -------------------------------------------------------------- noise tile
def noise_tile(size=180):
    """Greyscale static; screen-blended over the CRT screen at low opacity."""
    img = Image.new("L", (size, size))
    img.putdata([random.randint(0, 255) for _ in range(size * size)])
    img.convert("RGB").save(f"{OUT}/static-noise-tile.png")


# ------------------------------------------------------------------ logos
def logo_frame(w, h, jitter=0):
    """Dark wordmark on transparent — the page applies brightness(0) invert()."""
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = font(SANS_BOLD, int(h * 0.62))
    text = "NOiNA"
    l, t, r, b = d.textbbox((0, 0), text, font=f)
    x = (w - (r - l)) / 2 - l + jitter
    y = (h - (b - t)) / 2 - t
    d.text((x, y), text, font=f, fill=(17, 17, 17, 255))
    return img


def logos():
    logo_frame(520, 150).save(f"{OUT}/noina-logo-static.png")
    frames = [logo_frame(520, 150, jitter=j) for j in (0, 3, -2, 1, -3, 0)]
    frames[0].save(f"{OUT}/noina-logo.gif", save_all=True,
                   append_images=frames[1:], duration=110, loop=0,
                   disposal=2, transparency=0)


# ---------------------------------------------------------- profile photo
def profile():
    w, h = 408, 592
    img = Image.new("RGB", (w, h), (14, 26, 30))
    d = ImageDraw.Draw(img)
    for y in range(h):  # vertical wash
        k = y / h
        d.line([(0, y), (w, y)], fill=(int(14 + 26 * k), int(30 + 40 * k), int(36 + 44 * k)))
    d.ellipse([w * 0.28, h * 0.16, w * 0.72, h * 0.46], fill=(58, 92, 100))       # head
    d.ellipse([w * 0.12, h * 0.50, w * 0.88, h * 1.18], fill=(58, 92, 100))       # shoulders
    centered(d, (0, int(h * 0.80), w, h), "PHOTO", font(SANS_BOLD, 30), CYAN)
    img.save(f"{OUT}/profile-photo.png")


# ------------------------------------------------------------- og / social
def og_share():
    w, h = 1200, 630
    img = Image.new("RGB", (w, h), (13, 20, 24))
    d = ImageDraw.Draw(img)
    for y in range(h):
        k = y / h
        d.line([(0, y), (w, y)], fill=(int(13 + 18 * k), int(20 + 26 * k), int(24 + 30 * k)))
    # CRT body + screen
    d.rounded_rectangle([190, 105, 1010, 525], radius=46, fill=(38, 46, 50))
    d.rounded_rectangle([232, 147, 968, 455], radius=30, fill=(5, 5, 5))
    for y in range(147, 455, 3):  # scanlines
        d.line([(232, y), (968, y)], fill=(0, 0, 0))
    centered(d, (232, 147, 968, 455), "NOiNA", font(SANS_BOLD, 132), (233, 250, 252))
    centered(d, (232, 455, 968, 520), "BINGE-WORTHY MOTION DESIGN",
             font(SANS_BOLD, 26), CYAN)
    img.save(f"{OUT}/og-share.png")


# -------------------------------------------------------------- favicons
def favicons():
    base = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    d = ImageDraw.Draw(base)
    d.rounded_rectangle([16, 76, 496, 436], radius=64, fill=(13, 20, 24))
    d.rounded_rectangle([52, 112, 460, 400], radius=40, fill=(5, 5, 5))
    centered(d, (52, 112, 460, 400), "N", font(SANS_BOLD, 232), CYAN)
    for s in (16, 32, 48):
        base.resize((s, s), Image.LANCZOS).save(f"{OUT}/favicon-{s}.png")
    base.resize((180, 180), Image.LANCZOS).convert("RGB").save(f"{OUT}/apple-touch-icon.png")

    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">'
        '<rect x="16" y="76" width="480" height="360" rx="64" fill="#0d1418"/>'
        '<rect x="52" y="112" width="408" height="288" rx="40" fill="#050505"/>'
        '<text x="256" y="256" font-family="Helvetica,Arial,sans-serif" font-weight="700"'
        ' font-size="232" fill="#3CC4DC" text-anchor="middle"'
        ' dominant-baseline="central">N</text></svg>\n'
    )
    with open(f"{OUT}/favicon-small.svg", "w") as fh:
        fh.write(svg)


terrazzo()
noise_tile()
logos()
profile()
og_share()
favicons()
print("generated:", sorted(os.listdir(OUT)))
