# draw_helpers.py — Pillow drawing helpers, text registry, reusable
# components for "The World in One Day", Sunday 22 November 2026.
# All coordinates / sizes are in FINAL 1024-px page units; every drawing
# call multiplies by S = 2 internally (the page is drawn at 2048x2048
# and downscaled once with LANCZOS by the builder).
# Geometry is from icon_guide_news-image-20261122.md (sections 0, 1, 2,
# 3, 5, 6) and agent_spec_news-image-20261122.md sections 2-3.
# Colours are imported from data.py — never redefined here.

import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import data

S = 2

# ---------------------------------------------------------------- fonts
_LIB_DIR = os.environ.get("FONT_LIB_DIR", "/usr/share/fonts/truetype/liberation")
_COND_DIR = os.environ.get(
    "FONT_COND_DIR", "/home/hatch/workspace/fonts-dejavu-condensed"
)

_FONT_PATHS = {
    "serif_b": os.path.join(_LIB_DIR, "LiberationSerif-Bold.ttf"),
    "serif": os.path.join(_LIB_DIR, "LiberationSerif-Regular.ttf"),
    "serif_i": os.path.join(_LIB_DIR, "LiberationSerif-Italic.ttf"),
    "dserif_b": os.path.join(_COND_DIR, "DejaVuSerifCondensed-Bold.ttf"),
    "cond": os.path.join(_COND_DIR, "DejaVuSansCondensed.ttf"),
    "cond_b": os.path.join(_COND_DIR, "DejaVuSansCondensed-Bold.ttf"),
    "sans_b": os.path.join(_LIB_DIR, "LiberationSans-Bold.ttf"),
}

_FONT_CACHE = {}


def font(key, size):
    """Cached ImageFont.truetype at int(round(size * S)) for font key."""
    px = int(round(size * S))
    cache_key = (key, px)
    f = _FONT_CACHE.get(cache_key)
    if f is None:
        f = ImageFont.truetype(_FONT_PATHS[key], px)
        _FONT_CACHE[cache_key] = f
    return f


# ------------------------------------------------------- low-level wrappers
# Page units in, *S inside. Outline/stroke widths: max(1, round(width*S)).


def _w(width):
    return max(1, int(round(width * S)))


def _box(x0, y0, x1, y1):
    return [x0 * S, y0 * S, x1 * S, y1 * S]


def _pts(pts):
    return [(x * S, y * S) for (x, y) in pts]


def rect(d, x0, y0, x1, y1, fill=None, outline=None, width=1):
    d.rectangle(_box(x0, y0, x1, y1), fill=fill, outline=outline,
                width=_w(width))


def rrect(d, x0, y0, x1, y1, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(_box(x0, y0, x1, y1), radius=r * S, fill=fill,
                        outline=outline, width=_w(width))


def ellipse(d, x0, y0, x1, y1, fill=None, outline=None, width=1):
    d.ellipse(_box(x0, y0, x1, y1), fill=fill, outline=outline,
              width=_w(width))


def line(d, pts, fill, width=1, joint=None):
    d.line(_pts(pts), fill=fill, width=_w(width), joint=joint)


def poly(d, pts, fill=None, outline=None):
    d.polygon(_pts(pts), fill=fill, outline=outline)


# ------------------------------------------------------------- text registry
REGISTRY = []


def record(name, bbox):
    REGISTRY.append((name, bbox))


def reset_registry():
    del REGISTRY[:]


def text(d, name, x, y, s, key, size, fill, anchor="la"):
    """Draw text with font(key, size); record its bbox (page units) under
    name in REGISTRY; return the bbox."""
    f = font(key, size)
    d.text((x * S, y * S), s, font=f, fill=fill, anchor=anchor)
    bb = d.textbbox((x * S, y * S), s, font=f, anchor=anchor)
    bbox = (bb[0] / S, bb[1] / S, bb[2] / S, bb[3] / S)
    record(name, bbox)
    return bbox


def text_w(key, size, s):
    """Width of s in page units (textlength / S)."""
    return font(key, size).getlength(s) / S


def check_problems():
    """Return a list of problem strings: two boxes with DIFFERENT names
    overlapping by > 0.6 px in BOTH axes, or any box outside
    [0, 1024] x [0, 1024]. Same-name boxes are one element and are
    never flagged against each other."""
    problems = []
    for name, (x0, y0, x1, y1) in REGISTRY:
        if x0 < 0 or y0 < 0 or x1 > 1024 or y1 > 1024:
            problems.append(
                "%s out of bounds: (%.2f, %.2f, %.2f, %.2f)"
                % (name, x0, y0, x1, y1)
            )
    for i in range(len(REGISTRY)):
        name_i, (ax0, ay0, ax1, ay1) = REGISTRY[i]
        for j in range(i + 1, len(REGISTRY)):
            name_j, (bx0, by0, bx1, by1) = REGISTRY[j]
            if name_i == name_j:
                continue
            ox = min(ax1, bx1) - max(ax0, bx0)
            oy = min(ay1, by1) - max(ay0, by0)
            if ox > 0.6 and oy > 0.6:
                problems.append(
                    "%s overlaps %s by %.2f x %.2f px"
                    % (name_i, name_j, ox, oy)
                )
    return problems


# ------------------------------------------------------------ rich text wrap
def wrap(runs, width, lh):
    """Wrap runs [(text, key, size, colour), ...] on spaces to `width`
    (page units, measured with text_w). Returns (lines, total_h) where
    each line is a list of (text, font_obj, colour, x_off) and
    total_h = len(lines) * lh."""
    # Flatten runs into word tokens, keeping each word's font/colour.
    tokens = []
    for text_s, key, size, colour in runs:
        f = font(key, size)
        space_w = text_w(key, size, " ")
        for word in text_s.split(" "):
            if word == "":
                continue
            tokens.append((word, f, colour, text_w(key, size, word), space_w))
    lines = []
    cur = []
    cur_w = 0.0
    for word, f, colour, word_w, space_w in tokens:
        if not cur:
            cur.append((word, f, colour, 0.0))
            cur_w = word_w
        elif cur_w + space_w + word_w <= width:
            cur.append((word, f, colour, cur_w + space_w))
            cur_w += space_w + word_w
        else:
            lines.append(cur)
            cur = [(word, f, colour, 0.0)]
            cur_w = word_w
    if cur:
        lines.append(cur)
    return lines, len(lines) * lh


def draw_wrapped(d, name, lines, x, y, lh):
    """Draw wrapped lines; record ONE bbox per line as name_i.
    Returns total_h = len(lines) * lh."""
    for i, line_runs in enumerate(lines):
        ly = y + i * lh
        x0 = y0 = None
        x1 = y1 = None
        for text_s, f, colour, x_off in line_runs:
            px, py = (x + x_off) * S, ly * S
            d.text((px, py), text_s, font=f, fill=colour, anchor="la")
            bb = d.textbbox((px, py), text_s, font=f, anchor="la")
            bx0, by0, bx1, by1 = (bb[0] / S, bb[1] / S, bb[2] / S, bb[3] / S)
            x0 = bx0 if x0 is None else min(x0, bx0)
            y0 = by0 if y0 is None else min(y0, by0)
            x1 = bx1 if x1 is None else max(x1, bx1)
            y1 = by1 if y1 is None else max(y1, by1)
        if x0 is not None:
            record("%s_%d" % (name, i), (x0, y0, x1, y1))
    return len(lines) * lh


# ------------------------------------------------------------- badges & icons
def badge(d, cx, cy, number, colour, r, size):
    """Numbered circle badge: region-coloured circle, 1.2 px white
    outline, white cond_b number centred (anchor mm, cy + 0.4)."""
    ellipse(d, cx - r, cy - r, cx + r, cy + r, fill=colour,
            outline=data.WHITE, width=1.2)
    d.text((cx * S, (cy + 0.4) * S), str(number), font=font("cond_b", size),
           fill=data.WHITE, anchor="mm")


def square_badge(d, cx, cy, number, colour):
    """Square badge for list stories (side 16, sharp corners)."""
    rect(d, cx - 8, cy - 8, cx + 8, cy + 8, fill=colour,
         outline=data.WHITE, width=1.2)
    d.text((cx * S, (cy + 0.4) * S), str(number),
           font=font("cond_b", 10.2), fill=data.WHITE, anchor="mm")


def certainty_icon(d, kind, cx, cy, r):
    """One of the three certainty icons, centred at (cx, cy), radius r.
    Filled circle in the kind colour, then check / quote marks / "?"."""
    colour = data.CERT[kind]
    ellipse(d, cx - r, cy - r, cx + r, cy + r, fill=colour)
    if kind == "CONFIRMED":
        line(d, [(cx - 0.50 * r, cy + 0.02 * r),
                 (cx - 0.12 * r, cy + 0.42 * r),
                 (cx + 0.55 * r, cy - 0.40 * r)],
             fill=data.WHITE, width=0.30 * r, joint="curve")
    elif kind == "STATED":
        for dd in (-0.30 * r, 0.30 * r):
            ellipse(d, cx + dd - 0.22 * r, cy - 0.38 * r,
                    cx + dd + 0.22 * r, cy + 0.06 * r, fill=data.WHITE)
            poly(d, [(cx + dd + 0.05 * r, cy - 0.05 * r),
                     (cx + dd + 0.22 * r, cy - 0.10 * r),
                     (cx + dd - 0.12 * r, cy + 0.42 * r)],
                 fill=data.WHITE)
    elif kind == "UNVERIFIED":
        d.text((cx * S, (cy + 0.06 * r) * S), "?",
               font=font("sans_b", 1.45 * r), fill=data.WHITE, anchor="mm")
    else:
        raise ValueError("unknown certainty kind: %r" % (kind,))


def tag_chip(d, kind, extra, right, top):
    """Lead tag chip, right edge `right`, top `top`. White pill, 1.1 px
    outline in the kind colour, certainty icon at the left end, then
    the kind word (plus ' · ' + extra) in cond_b 10 in the kind colour.
    The text is registered under name 'tagchip'."""
    colour = data.CERT[kind]
    s = kind + (" · " + extra if extra else "")
    h = 16
    w = text_w("cond_b", 10, s) + h + 8
    rrect(d, right - w, top, right, top + 16, 8, fill=data.WHITE,
          outline=colour, width=1.1)
    certainty_icon(d, kind, right - w + 8, top + 8, 7)
    text(d, "tagchip", right - w + 16 + 3, top + 2.6, s, "cond_b", 10,
         colour, anchor="la")


# ------------------------------------------------------------ picture panels
def panel(d, img, picture_fn, x0, y0, x1, y1, place, label, label_size,
          place_size, sources=None):
    """Picture panel (icon guide section 5). The picture is drawn on a
    copy of img and pasted back clipped to the panel rect; the picture
    function receives the drawing area (x0, y0, x1, y0 + h). Then the
    dark place bar, the red label (top right) and the frame are drawn
    on the real canvas."""
    full_h = y1 - y0
    bar_h = place_size + 7
    h = full_h - bar_h
    # (1) Clip: draw the picture on a copy, paste back only the panel.
    tmp = img.copy()
    d_tmp = ImageDraw.Draw(tmp)
    picture_fn(d_tmp, x0, y0, x1, y0 + h)
    box = (int(round(x0 * S)), int(round(y0 * S)),
           int(round(x1 * S)), int(round(y1 * S)))
    img.paste(tmp.crop(box), box[:2])
    # (3) Place bar.
    rect(d, x0, y0 + h, x1, y1, fill=data.BAR)
    d.text(((x0 + 6) * S, (y0 + h + 2.5) * S), place,
           font=font("cond_b", place_size), fill=data.WHITE, anchor="la")
    if sources:
        d.text(((x1 - 6) * S, (y0 + h + 2.5) * S), sources,
               font=font("cond", place_size), fill=data.SRC, anchor="ra")
    # (4) Red label, top right.
    lw = text_w("sans_b", label_size, label) + 10
    lh = label_size + 6
    box_left = (x1 - 6) - lw
    box_top = y0 + 6
    rect(d, box_left, box_top, box_left + lw, box_top + lh, fill=data.RED)
    d.text(((box_left + 5) * S, (box_top + 2.4) * S), label,
           font=font("sans_b", label_size), fill=data.WHITE, anchor="la")
    # (5) Frame.
    rect(d, x0, y0, x1, y1, outline=(40, 44, 56), width=0.8)


# --------------------------------------------------------- shared pictures
def sky(d, x0, y0, x1, y1, top, bottom):
    """24-band vertical gradient from `top` to `bottom`."""
    h = y1 - y0
    for i in range(24):
        colour = tuple(
            int(top[c] + (bottom[c] - top[c]) * i / 23) for c in range(3)
        )
        rect(d, x0, y0 + h * i / 24, x1, y0 + h * (i + 1) / 24 + 0.6,
             fill=colour)


def flame(d, x, y, s):
    """Flame, (x, y) = centre of its base, s = scale."""
    poly(d, [(x - 9 * s, y), (x - 4 * s, y - 16 * s), (x, y - 8 * s),
             (x + 4 * s, y - 22 * s), (x + 9 * s, y)], fill=(232, 96, 28))
    poly(d, [(x - 5 * s, y), (x - s, y - 9 * s), (x + 3 * s, y - 13 * s),
             (x + 5 * s, y)], fill=(250, 196, 60))


def smoke(d, x, y, s, colour):
    """Four filled circles rising up and to the right."""
    for (cx, cy, r) in ((x, y, 8 * s), (x + 6 * s, y - 10 * s, 10 * s),
                        (x + 14 * s, y - 22 * s, 12 * s),
                        (x + 24 * s, y - 34 * s, 13 * s)):
        ellipse(d, cx - r, cy - r, cx + r, cy + r, fill=colour)


def drone(d, x, y, s, colour=(30, 30, 36)):
    """Nose-left aircraft seen from above: body + wing triangles."""
    poly(d, [(x - 6 * s, y), (x + 6 * s, y - 1.5 * s),
             (x + 6 * s, y + 1.5 * s)], fill=colour)
    poly(d, [(x - s, y - 5 * s), (x + 2 * s, y), (x - s, y + 5 * s)],
         fill=colour)
