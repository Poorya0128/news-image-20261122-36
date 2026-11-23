# pictures.py — the 13 picture functions for "The World in One Day",
# Sunday 22 November 2026 (make.fun news-image-20261122).
#
# Written from icon_guide_news-image-20261122.md section 7 (exact geometry)
# and ref_pictures.png. No randomness: every "random-looking" pattern is a
# fixed formula from the guide. Each function draws inside its drawing area
# (x0, y0, x1, y1) where y1 is the TOP of the place bar, not the panel bottom.
# All coordinates are final-page units; draw_helpers multiplies by S=2.
#
# Helpers used (from draw_helpers, imported as H):
#   H.sky(d, x0, y0, x1, y1, top, bottom)
#   H.flame(d, x, y, s)  H.smoke(d, x, y, s, colour)
#   H.drone(d, x, y, s, colour)
#   H.rect(d, x0, y0, x1, y1, fill, outline, width)
#   H.rrect(d, x0, y0, x1, y1, radius, fill, outline, width)
#   H.ellipse(d, x0, y0, x1, y1, fill, outline, width)
#   H.line(d, pts, fill, width, joint)  H.poly(d, pts, fill, outline)
#   H.text(d, name, x, y, s, key, size, fill, anchor)

import math

import draw_helpers as H
from data import GOLD, GREY, NAVY, RED, WHITE

# Colours named in the guide but not in data.py.
FLAME_OUT = (232, 96, 28)   # (draw_helpers.flame uses these internally)
DARK = (30, 30, 36)         # default drone colour


def _txt(d, name, s, x, y, key, size, fill, anchor="la"):
    """Thin wrapper so the H.text call site is a single line to adapt.
    H.text signature: text(d, name, x, y, s, key, size, fill, anchor)
    where `name` is the registry name for the overlap checker."""
    H.text(d, name, x, y, s, key, size, fill, anchor)


def _line(d, pts, fill, width):
    H.line(d, pts, fill, width)


def _dome(d, cx, y_top, y_bot, rx, fill):
    """Upper half of an ellipse (pie slice 180..360 deg) as a polygon.

    The guide specifies domes as pie slices, but draw_helpers has no pie
    primitive, so the arc is approximated with 24 segments — deterministic.
    Box: cx-rx..cx+rx horizontally, y_top..y_bot vertically.
    """
    cy = (y_top + y_bot) / 2.0
    ry = (y_bot - y_top) / 2.0
    pts = []
    for i in range(25):
        a = math.pi + i * math.pi / 24.0  # 180 deg -> 360 deg
        pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
    H.poly(d, pts, fill, None)


# ---------------------------------------------------------------- lead 1
def pic_cop(d, x0, y0, x1, y1):
    W = x1 - x0
    h = y1 - y0
    H.sky(d, x0, y0, x1, y1, (206, 230, 236), (238, 244, 240))
    # Globe
    cx = x0 + 70
    cy = y0 + h / 2 + 4
    H.ellipse(d, cx - 40, cy - 40, cx + 40, cy + 40, (70, 140, 200), None, 1)
    # Land: four circles
    for dx, dy, r in ((-14, -10, 16), (12, 6, 14), (-4, 20, 10), (18, -18, 9)):
        H.ellipse(d, cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r,
                  (96, 176, 96), None, 1)
    # Thermometer
    tx = cx + 54
    H.rrect(d, tx - 5, cy - 38, tx + 5, cy + 22, 5, WHITE, (150, 150, 150), 1)
    H.rect(d, tx - 2.5, cy - 20, tx + 2.5, cy + 20, RED, None, 1)
    H.ellipse(d, tx - 9, cy + 16, tx + 9, cy + 34, RED, None, 1)
    # Torn document (shadow first, then white, per half)
    px0 = x0 + 150
    py0 = y0 + 6
    px1 = x1 - 16
    py1 = y1 - 18
    mid = (px0 + px1) / 2
    left = [(px0, py0), (mid - 4, py0), (mid + 4, py0 + 18),
            (mid - 6, py0 + 38), (mid + 2, py0 + 60), (mid - 8, py1),
            (px0, py1)]
    right = [(mid + 6, py0 + 4), (px1, py0 + 8), (px1 - 4, py1 + 2),
             (mid - 2, py1 - 4), (mid + 8, py0 + 62), (mid, py0 + 40),
             (mid + 10, py0 + 20)]
    for poly in (left, right):
        shadow = [(x + 2, y + 3) for (x, y) in poly]
        H.poly(d, shadow, (190, 186, 176), None)
        H.poly(d, poly, WHITE, None)
    # Text
    _txt(d, "cop31", "COP31", px0 + 8, py0 + 8, "sans_b", 12, NAVY)
    _txt(d, "finaltext", "FINAL TEXT", px0 + 8, py0 + 23, "cond_b", 8.5, GREY)
    # Grey text lines
    for k in range(2):
        _line(d, [(px0 + 8, py0 + 40 + 10 * k), (mid - 14, py0 + 40 + 10 * k)],
              (200, 200, 200), 2)
        _line(d, [(mid + 16, py0 + 26 + 10 * k), (px1 - 10, py0 + 30 + 10 * k)],
              (200, 200, 200), 2)


# ---------------------------------------------------------------- lead 2
def pic_dymer(d, x0, y0, x1, y1):
    W = x1 - x0
    h = y1 - y0
    H.sky(d, x0, y0, x1, y1, (14, 22, 46), (44, 52, 86))
    # Stars (fixed formula)
    for i in range(12):
        sx = x0 + 14 + ((i * 53) % (W - 20))
        sy = y0 + 8 + ((i * 29) % 40)
        H.ellipse(d, sx - 0.8, sy - 0.8, sx + 0.8, sy + 0.8,
                  (220, 220, 240), None, 1)
    # Six drones with amber dashed trails
    for fx, fy in ((0.15, 0.22), (0.32, 0.12), (0.52, 0.18),
                   (0.72, 0.10), (0.86, 0.26), (0.62, 0.34)):
        x = x0 + fx * W
        y = y0 + fy * h
        for k in range(4):
            _line(d, [(x + 10 + 7 * k, y - 3 - 2 * k),
                      (x + 13 + 7 * k, y - 4 - 2 * k)], (230, 180, 80), 1)
        H.drone(d, x, y, 1, (210, 214, 226))
    # Block
    bx0 = x0 + 90
    bx1 = x1 - 90
    by0 = y0 + 0.38 * h
    H.rect(d, bx0, by0, bx1, y1, (150, 146, 140), None, 1)
    # Windows: exactly 5 floors x 9 columns
    fh = (y1 - by0 - 3) / 5
    for f in range(5):
        for c in range(9):
            wx = bx0 + 8 + c * (bx1 - bx0 - 16) / 9
            wy = by0 + 2 + f * fh
            lit = (7 * c + 3 * f) % 5 != 0
            H.rect(d, wx, wy, wx + 8, wy + 0.55 * fh,
                   (250, 214, 120) if lit else (60, 62, 72), None, 1)
    # Collapse gap
    g0 = bx0 + 0.40 * (bx1 - bx0)
    g1 = bx0 + 0.62 * (bx1 - bx0)
    H.poly(d, [(g0, by0 - 2), (g1, by0 - 2), (g1 - 4, by0 + 18),
               (g1 + 2, by0 + 34), (g1 - 8, y1), (g0 + 6, y1),
               (g0 - 2, by0 + 30), (g0 + 4, by0 + 12)], (30, 36, 60), None)
    # Rubble triangles
    for k in range(7):
        rx = g0 + 4 + k * (g1 - g0 - 8) / 7
        H.poly(d, [(rx, y1), (rx + 6, y1 - 10 - 5 * (k % 3)), (rx + 12, y1)],
               (110, 104, 98), None)
    # Flames
    H.flame(d, g0 + 18, y1 - 10, 1.0)
    H.flame(d, g1 - 16, y1 - 6, 0.8)


# ---------------------------------------------------------------- lead 3
def pic_benghazi(d, x0, y0, x1, y1):
    W = x1 - x0
    h = y1 - y0
    H.sky(d, x0, y0, x1, y1, (236, 150, 92), (250, 214, 168))
    sy = y0 + 0.66 * h
    H.rect(d, x0, sy, x1, y1, (36, 82, 120), None, 1)
    # Waves
    for k in range(6):
        wy = sy + 6 + 5 * (k % 2)
        _line(d, [(x0 + 10 + 52 * k, wy), (x0 + 34 + 52 * k, wy)],
              (90, 140, 176), 1.2)
    # Quay (right edge) + two cranes
    H.rect(d, x1 - 110, sy - 6, x1, sy + 3, (120, 106, 92), None, 1)
    for cx in (x1 - 96, x1 - 60):
        _line(d, [(cx, sy - 6), (cx, y0 + 4)], (70, 62, 56), 2.4)
        _line(d, [(cx - 10, y0 + 5), (cx + 16, y0 + 5)], (70, 62, 56), 2.4)
    # Main element: capsized hull
    bx = x0 + 0.40 * W
    H.poly(d, [(bx - 80, sy + 1), (bx + 34, sy + 1), (bx + 50, y0 + 4),
               (bx + 40, y0 + 2), (bx - 20, sy - 0.32 * h)],
           (98, 104, 112), None)
    # Dark bow face
    H.poly(d, [(bx + 34, sy + 1), (bx + 50, y0 + 4), (bx + 56, y0 + 7),
               (bx + 44, sy + 1)], (70, 76, 84), None)
    H.smoke(d, bx - 56, sy - 10, 0.75, (88, 84, 84))
    H.flame(d, bx - 60, sy + 1, 0.7)
    # Foam
    for k in range(5):
        _line(d, [(bx - 84 + 24 * k, sy + 3), (bx - 70 + 24 * k, sy + 3)],
              (200, 220, 236), 1.2)


# --------------------------------------------------------------- card 4
def pic_power(d, x0, y0, x1, y1):
    W = x1 - x0
    h = y1 - y0
    H.sky(d, x0, y0, x1, y1, (18, 24, 48), (40, 46, 74))
    # Skyline: 11 buildings, only the left half lit
    for k in range(11):
        X = x0 + 60 + 12 * k
        hk = h * (0.45 + 0.4 * ((37 * k) % 5) / 5)
        H.rect(d, X, y1 - hk, X + 10, y1, (34, 40, 62), None, 1)
        for j in range(int(hk // 6)):
            lit = k < 5 and (j + k) % 3 != 0
            H.rect(d, X + 3, y1 - hk + 3 + 6 * j, X + 7, y1 - hk + 6 + 6 * j,
                   (250, 214, 120) if lit else (52, 58, 80), None, 1)
    # Main element: dead bulb
    cx = x0 + 28
    cy = y0 + 0.42 * h
    r = 0.30 * h
    H.ellipse(d, cx - r, cy - r, cx + r, cy + r, (240, 236, 210), None, 1)
    H.rect(d, cx - 0.45 * r, cy + 0.85 * r, cx + 0.45 * r, cy + 1.45 * r,
           (160, 160, 168), None, 1)
    _line(d, [(cx - 1.25 * r, cy + 1.25 * r), (cx + 1.25 * r, cy - 1.25 * r)],
          RED, 3.2)


# --------------------------------------------------------------- card 5
def pic_tanker(d, x0, y0, x1, y1):
    W = x1 - x0
    h = y1 - y0
    H.sky(d, x0, y0, x1, y1, (176, 196, 214), (220, 228, 232))
    sy = y0 + 0.70 * h
    H.rect(d, x0, sy, x1, y1, (42, 92, 128), None, 1)
    # Main element: tanker
    t0 = x0 + 8
    t1 = x0 + 82
    H.poly(d, [(t0, sy - 7), (t1, sy - 7), (t1 - 8, sy + 5), (t0 + 6, sy + 5)],
           (150, 40, 36), None)
    H.rect(d, t0 + 4, sy - 10, t1 - 22, sy - 7, (80, 84, 92), None, 1)
    H.rect(d, t1 - 22, sy - 21, t1 - 8, sy - 7, (236, 236, 236), None, 1)
    H.smoke(d, t0 + 24, sy - 20, 0.55, (96, 92, 92))
    H.flame(d, t0 + 26, sy - 9, 0.65)


# --------------------------------------------------------------- card 6
def pic_westbank(d, x0, y0, x1, y1):
    W = x1 - x0
    h = y1 - y0
    H.sky(d, x0, y0, x1, y1, (40, 34, 58), (96, 62, 60))
    # Three houses
    for X, hh in ((x0 + 8, 0.55 * h), (x0 + 46, 0.62 * h), (x0 + 84, 0.50 * h)):
        H.rect(d, X, y1 - hh, X + 32, y1, (196, 170, 130), None, 1)
        H.poly(d, [(X - 2, y1 - hh), (X + 16, y1 - hh - 7), (X + 34, y1 - hh)],
               (150, 110, 80), None)
        H.rect(d, X + 12.8, y1 - 8, X + 19.2, y1, (90, 60, 40), None, 1)
    # Flames on the roofs, smoke above
    H.flame(d, x0 + 62, y1 - 0.62 * h, 0.8)
    H.flame(d, x0 + 24, y1 - 0.55 * h, 0.6)
    H.smoke(d, x0 + 60, y0 + 8, 0.45, (70, 64, 70))


# --------------------------------------------------------------- card 7
def pic_ebola(d, x0, y0, x1, y1):
    W = x1 - x0
    h = y1 - y0
    H.sky(d, x0, y0, x1, y1, (236, 244, 240), (250, 250, 246))
    # Main element: virus
    cx = x0 + 26
    cy = y0 + h / 2
    R = 0.30 * h
    for i in range(12):
        a = math.radians(30 * i)
        ca, sa = math.cos(a), math.sin(a)
        ox, oy = cx + 1.4 * R * ca, cy + 1.4 * R * sa
        _line(d, [(cx + R * ca, cy + R * sa), (ox, oy)], (176, 30, 40), 1.6)
        H.ellipse(d, ox - 1.8, oy - 1.8, ox + 1.8, oy + 1.8,
                  (176, 30, 40), None, 1)
    H.ellipse(d, cx - R, cy - R, cx + R, cy + R, (214, 70, 70), None, 1)
    # Clinic with red cross
    hx = x0 + 66
    H.rect(d, hx - 16, y1 - 0.70 * h, hx + 16, y1, WHITE, (160, 160, 160), 0.8)
    H.rect(d, hx - 2.5, y1 - 0.62 * h, hx + 2.5, y1 - 0.18 * h,
           (200, 30, 40), None, 1)
    H.rect(d, hx - 9, y1 - 0.43 * h, hx + 9, y1 - 0.33 * h,
           (200, 30, 40), None, 1)


# --------------------------------------------------------------- card 8
def pic_khartoum(d, x0, y0, x1, y1):
    W = x1 - x0
    h = y1 - y0
    H.sky(d, x0, y0, x1, y1, (238, 200, 150), (246, 226, 190))
    # Town: 8 buildings
    for k in range(8):
        X = x0 + 70 + 16 * k
        bh = h * (0.35 + 0.12 * (k % 3))
        H.rect(d, X, y1 - bh, X + 13, y1, (204, 160, 110), None, 1)
    # Main element: UN building
    u0 = x0 + 8
    u1 = x0 + 62
    H.rect(d, u0, y1 - 0.62 * h, u1, y1, WHITE, (150, 150, 150), 0.6)
    H.rect(d, u0, y1 - 0.62 * h, u1, y1 - 0.40 * h, (70, 140, 220), None, 1)
    _txt(d, "un", "UN", (u0 + u1) / 2, y1 - 0.20 * h, "sans_b", 9.5,
         (70, 140, 220), "mm")
    H.flame(d, u1 - 8, y1 - 0.60 * h, 0.6)
    # Two drones, left of the "UN SITE HIT" label
    H.drone(d, x0 + 0.36 * W, y0 + 0.22 * h + 3, 1, DARK)
    H.drone(d, x0 + 0.47 * W, y0 + 0.12 * h + 3, 1, DARK)


# --------------------------------------------------------------- card 9
def pic_istanbul(d, x0, y0, x1, y1):
    W = x1 - x0
    h = y1 - y0
    H.sky(d, x0, y0, x1, y1, (190, 206, 226), (232, 236, 240))
    # Mosque (background, right): dome + two minarets
    cx = x0 + 150
    _dome(d, cx, y1 - 0.75 * h, y1 + 6, 16, (140, 150, 166))
    for mx in (cx - 24, cx + 24):
        H.rect(d, mx - 1.5, y1 - 0.85 * h, mx + 1.5, y1, (140, 150, 166),
               None, 1)
    # Main element: FREE PRESS banner
    H.rect(d, x0 + 6, y0 + 3, x0 + 84, y0 + 14, WHITE, (176, 30, 40), 1)
    _txt(d, "freepress", "FREE PRESS", x0 + 45, y0 + 8.6, "sans_b", 8.6, (176, 30, 40),
         "mm")
    # Nine marchers
    colours = ((176, 30, 40), (40, 60, 110), (60, 60, 66))
    for k in range(9):
        px = x0 + 10 + 10 * k
        H.ellipse(d, px - 3, y0 + 15, px + 3, y0 + 21, (70, 56, 50), None, 1)
        H.rect(d, px - 3.6, y0 + 21, px + 3.6, y1, colours[k % 3], None, 1)


# -------------------------------------------------------------- card 10
def pic_hk(d, x0, y0, x1, y1):
    W = x1 - x0
    h = y1 - y0
    H.sky(d, x0, y0, x1, y1, (226, 232, 240), (244, 244, 244))
    # Towers
    for k, f in enumerate((0.50, 0.80, 0.45, 0.90, 0.60, 0.70, 0.40, 0.85)):
        X = x0 + 70 + 15 * k
        H.rect(d, X, y1 - f * h, X + 11, y1, (176, 190, 210), None, 1)
    # Main element: ballot box
    bx = x0 + 38
    H.rect(d, bx - 26, y1 - 0.45 * h, bx + 26, y1, (180, 28, 40), None, 1)
    H.rect(d, bx - 11, y1 - 0.45 * h - 1, bx + 11, y1 - 0.45 * h + 2,
           (60, 14, 20), None, 1)
    # Ballot sticking out of the slot
    H.poly(d, [(bx - 9, y0 + 2), (bx + 12, y0 + 4), (bx + 10, y1 - 0.42 * h),
               (bx - 10, y1 - 0.44 * h)], WHITE, None)
    # Green tick on the ballot
    _line(d, [(bx - 4, y0 + 0.30 * h), (bx, y0 + 0.42 * h),
              (bx + 6, y0 + 0.14 * h)], (30, 120, 70), 2.2)


# -------------------------------------------------------------- card 11
def pic_seoul(d, x0, y0, x1, y1):
    W = x1 - x0
    h = y1 - y0
    H.sky(d, x0, y0, x1, y1, (232, 236, 246), (246, 246, 246))
    # Exam sheet
    p0 = x0 + 8
    H.rect(d, p0 + 2, y0 + 4, p0 + 46, y1, (196, 196, 196), None, 1)
    H.rect(d, p0, y0 + 2, p0 + 44, y1 - 1, WHITE, None, 1)
    _txt(d, "exam", "EXAM", p0 + 5, y0 + 4, "cond_b", 7.5, NAVY)
    for k in range(3):
        _line(d, [(p0 + 5, y0 + 15 + 5 * k), (p0 + 38, y0 + 15 + 5 * k)],
              (200, 200, 200), 1.2)
    # Main element: AI chip
    cx = x0 + 84
    cy = y0 + h / 2
    H.rrect(d, cx - 15, cy - 11, cx + 15, cy + 11, 3, (40, 50, 72), None, 1)
    for k in range(3):
        x = cx - 9 + 9 * k
        _line(d, [(x, cy - 15), (x, cy - 11)], (40, 50, 72), 1.6)
        _line(d, [(x, cy + 11), (x, cy + 15)], (40, 50, 72), 1.6)
    _txt(d, "ai", "AI", cx, cy, "sans_b", 11, (120, 200, 255), "mm")
    # Red slash across the chip
    _line(d, [(cx - 20, cy + 14), (cx + 20, cy - 14)], RED, 2.8)


# -------------------------------------------------------------- card 12
def pic_house(d, x0, y0, x1, y1):
    W = x1 - x0
    h = y1 - y0
    H.sky(d, x0, y0, x1, y1, (120, 160, 214), (176, 204, 236))
    CAP = (250, 250, 246)
    # Main element: Capitol
    cx = x0 + 60
    H.rect(d, cx - 52, y1 - 0.30 * h, cx + 52, y1, CAP, None, 1)
    for k in range(9):
        H.rect(d, cx - 47 + 12 * k, y1 - 0.27 * h, cx - 44 + 12 * k, y1 - 1,
               (170, 170, 164), None, 1)
    H.rect(d, cx - 18, y1 - 0.50 * h, cx + 18, y1 - 0.30 * h, CAP, None, 1)
    _dome(d, cx, y1 - 0.88 * h, y1 - 0.30 * h, 16, CAP)
    H.rect(d, cx - 1.5, y0 + 1, cx + 1.5, y1 - 0.80 * h, CAP, None, 1)
    # Seats: 3 blue, 2 red
    for k in range(5):
        X = x0 + 124 + 11 * k
        H.rect(d, X, y1 - 8, X + 8, y1,
               (40, 90, 190) if k < 3 else (196, 50, 50), None, 1)


# -------------------------------------------------------------- card 13
def pic_tennis(d, x0, y0, x1, y1):
    W = x1 - x0
    h = y1 - y0
    H.rect(d, x0, y0, x1, y1, (28, 70, 140), None, 1)
    # Court
    H.rect(d, x0 + 50, y0 + 4, x1 - 6, y1 - 2, (40, 110, 190), None, 1)
    midx = (x0 + 50 + x1 - 6) / 2
    for vx in (x0 + 50, midx, x1 - 6):
        _line(d, [(vx, y0 + 4), (vx, y1 - 2)], WHITE, 1.2)
    _line(d, [(x0 + 50, (y0 + y1) / 2), (x1 - 6, (y0 + y1) / 2)], WHITE, 1.2)
    # Main element: gold trophy
    tx = x0 + 24
    ty = y0 + 2
    H.poly(d, [(tx - 11, ty), (tx + 11, ty), (tx + 7, ty + 0.50 * h),
               (tx - 7, ty + 0.50 * h)], GOLD, None)
    H.rect(d, tx - 2.5, ty + 0.50 * h, tx + 2.5, ty + 0.72 * h, GOLD, None, 1)
    H.rect(d, tx - 10, ty + 0.72 * h, tx + 10, ty + 0.90 * h,
           (190, 150, 60), None, 1)
    # Ball
    bx, by = x0 + 100, y0 + 0.55 * h
    H.ellipse(d, bx - 5, by - 5, bx + 5, by + 5, (214, 236, 60), None, 1)


PICTURES = {
    "cop": pic_cop,
    "dymer": pic_dymer,
    "benghazi": pic_benghazi,
    "power": pic_power,
    "tanker": pic_tanker,
    "westbank": pic_westbank,
    "ebola": pic_ebola,
    "khartoum": pic_khartoum,
    "istanbul": pic_istanbul,
    "hk": pic_hk,
    "seoul": pic_seoul,
    "house": pic_house,
    "tennis": pic_tennis,
}
