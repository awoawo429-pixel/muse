#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news infographic (1024x1024).

Deterministic: fixed layout, fixed text, fixed colours, no randomness,
no network, no timestamps. Run: python3 draw_infographic.py
Writes entry.png to MAKEFUN_OUTPUT_DIR (or /output).
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (244, 241, 234)
NAVY = (15, 42, 74)
NAVY2 = (23, 58, 99)
RED = (178, 34, 34)
INK = (24, 24, 24)
GREY = (90, 90, 90)
CARD = (255, 255, 255)
LINE = (210, 205, 195)

FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def icon(draw, kind, cx, cy, r, colour):
    """Simple flat geometric icons, drawn with primitives only."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=colour)
    w = (255, 255, 255)
    if kind == "ship":
        draw.polygon([(cx - 28, cy + 8), (cx + 28, cy + 8), (cx + 18, cy + 26), (cx - 18, cy + 26)], fill=w)
        draw.rectangle([cx - 4, cy - 24, cx + 4, cy + 8], fill=w)
        draw.rectangle([cx + 4, cy - 18, cx + 22, cy - 6], fill=w)
        draw.arc([cx - 30, cy + 30, cx + 30, cy + 44], 0, 180, fill=w, width=3)
    elif kind == "flame":
        draw.polygon([(cx, cy - 30), (cx + 18, cy - 2), (cx + 8, cy + 12),
                      (cx + 22, cy + 26), (cx - 22, cy + 26), (cx - 8, cy + 12),
                      (cx - 18, cy - 2)], fill=w)
        draw.ellipse([cx - 7, cy + 6, cx + 7, cy + 24], fill=colour)
    elif kind == "chart":
        for i, h in enumerate((16, 28, 20, 36)):
            x0 = cx - 26 + i * 14
            draw.rectangle([x0, cy + 18 - h, x0 + 10, cy + 18], fill=w)
        draw.rectangle([cx - 30, cy + 18, cx + 30, cy + 22], fill=w)
    elif kind == "rocket":
        draw.polygon([(cx, cy - 32), (cx + 12, cy - 6), (cx + 12, cy + 16),
                      (cx - 12, cy + 16), (cx - 12, cy - 6)], fill=w)
        draw.ellipse([cx - 6, cy + 2, cx + 6, cy + 14], fill=colour)
        draw.polygon([(cx - 12, cy + 10), (cx - 22, cy + 26), (cx - 12, cy + 20)], fill=w)
        draw.polygon([(cx + 12, cy + 10), (cx + 22, cy + 26), (cx + 12, cy + 20)], fill=w)
        draw.polygon([(cx - 6, cy + 16), (cx + 6, cy + 16), (cx, cy + 32)], fill=w)
    elif kind == "flag":
        draw.rectangle([cx - 4, cy - 30, cx, cy + 30], fill=w)
        draw.polygon([(cx, cy - 30), (cx + 30, cy - 20), (cx, cy - 10)], fill=w)
        draw.rectangle([cx - 16, cy + 30, cx + 16, cy + 34], fill=w)
    elif kind == "drone":
        draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=w)
        for dx, dy in ((-24, -20), (24, -20), (-24, 20), (24, 20)):
            draw.ellipse([cx + dx - 7, cy + dy - 7, cx + dx + 7, cy + dy + 7], outline=w, width=3)
            draw.line([cx, cy, cx + dx, cy + dy], fill=w, width=3)


def panel(draw, x, y, w, h, tag, headline, body, accent, kind, head_size=27, body_size=17):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=CARD, outline=LINE, width=2)
    draw.rectangle([x, y, x + 10, y + h], fill=accent)
    tx = x + 26
    draw.text((tx, y + 16), tag, font=font(FONT_B, 17), fill=accent)
    icon(draw, kind, x + w - 52, y + 52, 34, accent)
    lines = wrap(draw, headline, font(FONT_B, head_size), w - 130)
    yy = draw_lines(draw, lines, tx, y + 44, font(FONT_B, head_size), INK, head_size + 6)
    blines = wrap(draw, body, font(FONT_R, body_size), w - 52)
    draw_lines(draw, blines, tx, yy + 10, font(FONT_R, body_size), GREY, body_size + 7)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Header
    d.rectangle([0, 0, W, 168], fill=NAVY)
    d.rectangle([0, 168, W, 176], fill=RED)
    d.text((32, 22), "THE WORLD IN ONE DAY", font=font(FONT_B, 24), fill=(255, 255, 255))
    d.text((32, 52), "25 NOVEMBER 2026", font=font(FONT_B, 68), fill=(255, 255, 255))
    d.text((32, 128), "WEDNESDAY  \u00b7  SIX STORIES THAT DEFINED THE DAY", font=font(FONT_B, 20), fill=(180, 200, 220))

    # Lead story
    panel(d, 24, 192, 976, 238, "LEAD  \u00b7  STRAIT OF HORMUZ",
          "Two oil tankers explode after hitting mines in Hormuz",
          "Iran's Revolutionary Guard Navy says the tankers struck naval "
          "mines early on Wednesday and caught fire on a route it calls "
          "unauthorised. The vessels are unnamed; the claims are unverified.",
          RED, "ship", head_size=36, body_size=21)

    # Grid of four
    gy, gh, gw = 446, 202, 482
    panel(d, 24, gy, gw, gh, "MIDDLE EAST",
          "Houthis claim strike on Ras Tanura refinery",
          "Yemen's Houthis say they hit Saudi Arabia's largest refinery. "
          "Riyadh says four drones were shot down.",
          (196, 90, 20), "flame")
    panel(d, 518, gy, gw, gh, "TRADE  \u00b7  UNITED STATES",
          "US proposes tariffs on 14 partners",
          "Washington targets excess factory capacity, with the highest "
          "rates for China.",
          (20, 110, 140), "chart")
    panel(d, 24, gy + gh + 16, gw, gh, "SPACE  \u00b7  CHINA",
          "Shenzhou-24 carries Pakistan's first astronaut",
          "China launches Shenzhou-24 with Tang Hongbo, Wu Yi and "
          "Muhammad Zeeshan Ali.",
          (30, 80, 140), "rocket")
    panel(d, 518, gy + gh + 16, gw, gh, "PACIFIC",
          "Australia, Solomons sign security treaty",
          "Canberra becomes primary security partner; no foreign "
          "base allowed.",
          (140, 60, 120), "flag")

    # Bottom strip: sixth story
    d.rounded_rectangle([24, 878, 1000, 1000], radius=14, fill=NAVY2)
    icon(d, "drone", 78, 922, 30, RED)
    d.text((126, 884), "ALSO ON 25 NOVEMBER  \u00b7  SUDAN",
           font=font(FONT_B, 17), fill=(255, 210, 90))
    d.text((126, 910), "Drone strikes kill 19 civilians in Sudan's Blue Nile state,",
           font=font(FONT_B, 24), fill=(255, 255, 255))
    d.text((126, 940), "rights group Emergency Lawyers reports.",
           font=font(FONT_B, 24), fill=(255, 255, 255))

    import os
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out, exist_ok=True)
    img.save(os.path.join(out, "entry.png"), format="PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
