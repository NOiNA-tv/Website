#!/usr/bin/env python3
"""Generate placeholder assets for the NOiNA portfolio site.

Every file produced here is a stand-in so the page renders end-to-end.
Replace with the real artwork when available (see assets/README.md).
"""
import math
import random
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(OUT, exist_ok=True)
random.seed(7)

SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
CYAN = (78, 200, 224)
INK = (13, 24, 30)
SS = 4  # supersampling factor for the vector-ish marks


def font(path, size):
    return ImageFont.truetype(path, size)


def centered(draw, box, text, f, fill):
    x0, y0, x1, y1 = box
    l, t, r, b = draw.textbbox((0, 0), text, font=f)
    draw.text((x0 + (x1 - x0 - (r - l)) / 2 - l,
               y0 + (y1 - y0 - (b - t)) / 2 - t), text, font=f, fill=fill)


# ---------------------------------------------------------------- terrazzo
def terrazzo(size=270):
    """Tileable terrazzo: grey base with green/purple/blue/magenta chips."""
    img = Image.new("RGB", (size, size), (150, 158, 160))
    d = ImageDraw.Draw(img)
    chips = [(20, 130, 100), (110, 85, 180), (55, 110, 190), (165, 60, 130)]
    for _ in range(700):
        cx, cy = random.uniform(0, size), random.uniform(0, size)
        r = random.uniform(1.6, 6.0)
        col = random.choice(chips)
        n = random.randint(5, 8)
        a0 = random.uniform(0, math.tau)
        radii = [r * random.uniform(0.6, 1.4) for _ in range(n)]
        # draw at every wrap offset so the tile seams are invisible
        for dx in (-size, 0, size):
            for dy in (-size, 0, size):
                x, y = cx + dx, cy + dy
                if not (-12 < x < size + 12 and -12 < y < size + 12):
                    continue
                d.polygon([(x + radii[i] * math.cos(a0 + math.tau * i / n),
                            y + radii[i] * math.sin(a0 + math.tau * i / n))
                           for i in range(n)], fill=col)
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
    d.text(((w - (r - l)) / 2 - l + jitter, (h - (b - t)) / 2 - t),
           text, font=f, fill=(17, 17, 17, 255))
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
    img = Image.new("RGB", (w, h), (126, 214, 232))
    d = ImageDraw.Draw(img)
    d.ellipse([w * 0.26, h * 0.16, w * 0.74, h * 0.52], fill=(18, 74, 88))
    d.ellipse([w * 0.08, h * 0.56, w * 0.92, h * 1.20], fill=(18, 74, 88))
    # coarse dither, echoing the halftone treatment of the real portrait
    px = img.load()
    for y in range(0, h, 3):
        for x in range(0, w, 3):
            if random.random() >= 0.35:
                continue
            for dy in range(3):
                for dx in range(3):
                    if x + dx < w and y + dy < h:
                        r, g, b = px[x + dx, y + dy]
                        px[x + dx, y + dy] = (min(255, r + 26), min(255, g + 26), min(255, b + 26))
    centered(d, (0, int(h * 0.86), w, h), "PHOTO", font(SANS_BOLD, 28), (18, 74, 88))
    img.save(f"{OUT}/profile-photo.png")


# ------------------------------------------------------------- og / social
def og_share():
    w, h = 1200, 630
    img = Image.new("RGB", (w, h), (13, 20, 24))
    d = ImageDraw.Draw(img)
    for y in range(h):
        k = y / h
        d.line([(0, y), (w, y)], fill=(int(13 + 18 * k), int(20 + 26 * k), int(24 + 30 * k)))
    d.rounded_rectangle([190, 105, 1010, 525], radius=46, fill=(38, 46, 50))
    d.rounded_rectangle([232, 147, 968, 455], radius=30, fill=(22, 130, 150))
    for y in range(147, 455, 3):  # scanlines
        d.line([(232, y), (968, y)], fill=(10, 60, 72))
    centered(d, (232, 147, 968, 440), "NOiNA", font(SANS_BOLD, 132), (236, 252, 254))
    centered(d, (232, 440, 968, 520), "BINGE WORTHY MOTION DESIGN",
             font(SANS_BOLD, 26), (210, 244, 250))
    img.save(f"{OUT}/og-share.png")


# -------------------------------------------------------------- ghost mark
def ghost(px):
    """The NOiNA mark: a cyan arch with two eyes, a smile and a chin dome."""
    s = px * SS
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    u = s / 512.0          # design units -> pixels
    sw = max(1, int(30 * u))

    def U(*v):
        return [x * u for x in v]

    d.rounded_rectangle(U(0, 0, 511, 511), radius=int(96 * u), fill=INK)
    # arch: an open-bottomed dome — a thick stroked arc closed by two legs
    d.arc(U(58, 42, 454, 560), start=180, end=360, fill=CYAN, width=sw)
    d.line(U(58 + sw / 2, 300, 58 + sw / 2, 500), fill=CYAN, width=sw)
    d.line(U(454 - sw / 2, 300, 454 - sw / 2, 500), fill=CYAN, width=sw)
    # eyes
    for x0 in (206, 286):
        d.rounded_rectangle(U(x0, 170, x0 + 30, 276), radius=int(15 * u), fill=CYAN)
    # smile: a lens built from two arcs
    d.chord(U(146, 268, 366, 380), start=0, end=180, fill=CYAN)
    d.chord(U(146, 292, 366, 356), start=0, end=180, fill=INK)
    # chin dome
    d.ellipse(U(150, 424, 362, 620), fill=CYAN)
    return img.resize((px, px), Image.LANCZOS)


def favicons():
    for n in (16, 32, 48):
        ghost(n).save(f"{OUT}/favicon-{n}.png")
    ghost(180).convert("RGB").save(f"{OUT}/apple-touch-icon.png")

    with open(f"{OUT}/favicon-small.svg", "w") as fh:
        fh.write(
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">'
            '<rect width="512" height="512" rx="96" fill="#0d181e"/>'
            '<path d="M73 500V301a183 244 0 0 1 366 0v199" fill="none"'
            ' stroke="#4ec8e0" stroke-width="30" stroke-linecap="round"/>'
            '<g fill="#4ec8e0">'
            '<rect x="206" y="170" width="30" height="106" rx="15"/>'
            '<rect x="286" y="170" width="30" height="106" rx="15"/>'
            '<path d="M146 324q110 84 220 0-110 32-220 0Z"/>'
            '<ellipse cx="256" cy="522" rx="106" ry="98"/></g></svg>\n'
        )


terrazzo()
noise_tile()
logos()
profile()
og_share()
favicons()
print("generated:", sorted(os.listdir(OUT)))
