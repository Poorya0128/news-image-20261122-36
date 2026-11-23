# map_draw.py — the world map for "The World in One Day", 22 Nov 2026.
# One-page newspaper, 35 stories, 1024x1024. Draws the map box, the
# numbered pins for stories 1-13, the list dots for stories 14-36, the
# map key and the region key (spec section 8, icon guide section 4).
# All coordinates / sizes are in final 1024-px page units. H.* helpers
# take page units and scale by S internally; the raw Pillow work here
# (land mask, outline overlay, equator dashes) multiplies by S by hand.
# Deterministic: no randomness, fixed placement order and candidate list.

import json
import math
import os
import sys

from PIL import Image, ImageChops, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import data
import draw_helpers as H

from data import GREY, INK, LAND, OCEAN, REG, REGION_NAMES, WHITE

S = H.S

# Map drawing constants (spec 8 / icon guide 4), page units.
_EQUATOR_COLOUR = (160, 176, 192)
_OUTLINE_COLOUR = (150, 160, 172)
_BADGE_R = 7.2
_BADGE_SIZE = 9.2
_DOT_R = 2.8
_TRUE_DOT_R = 1.6
_LON_MIN, _LON_MAX = -126.0, 180.0
_LAT_TOP, _LAT_BOTTOM = 62.0, -42.0


def load_land(path):
    """Load world_land.json; return the list of rings ([[lon, lat], ...]).

    Two rings in the file are antimeridian-seam artefacts of the
    TopoJSON join, not land: they run the whole width of the map at a
    nearly constant latitude (ring 8 at lat ~-16.5, ring 64 at
    lat ~71). A real ring that spans >300 degrees of longitude (the
    big northern landmass) spans >100 degrees of latitude, so rings
    spanning >300 degrees of longitude but <2 degrees of latitude
    are dropped here.
    """
    with open(path, "r", encoding="utf-8") as fh:
        rings = json.load(fh)
    kept = []
    for ring in rings:
        if not ring:
            continue
        lons = [pt[0] for pt in ring]
        lats = [pt[1] for pt in ring]
        if max(lons) - min(lons) > 300.0 and max(lats) - min(lats) < 2.0:
            continue
        kept.append(ring)
    return kept


def lonlat_to_xy(lon, lat, box):
    """Equirectangular projection into box=(x0, y0, x1, y1), page units.

    lon -126..180 maps to x0..x1, lat 62 (top)..-42 (bottom) maps to
    y0..y1. Scale is (x1 - x0) / 306 px per degree on both axes.
    """
    x0, y0, x1, y1 = box
    scale = (x1 - x0) / (_LON_MAX - _LON_MIN)
    x = x0 + (lon - _LON_MIN) * scale
    y = y0 + (_LAT_TOP - lat) * scale
    return (x, y)


def _canvas_box(box):
    """Page-unit box -> canvas-pixel box (ints)."""
    x0, y0, x1, y1 = box
    return (int(round(x0 * S)), int(round(y0 * S)),
            int(round(x1 * S)), int(round(y1 * S)))


def _ring_canvas_points(ring, box):
    """A land ring projected to canvas-pixel (x, y) points."""
    return [(lonlat_to_xy(lon, lat, box)[0] * S,
             lonlat_to_xy(lon, lat, box)[1] * S) for lon, lat in ring]


def _box_mask(img_size, box):
    """'L' mask, white exactly inside the box (canvas pixels)."""
    mask = Image.new("L", img_size, 0)
    md = ImageDraw.Draw(mask)
    md.rectangle(_canvas_box(box), fill=255)
    return mask


def draw_map(img, box, land, stories):
    """Draw the map into PIL image `img` (2048x2048, drawn at 2x).

    `box` is the map box in page units, `land` the rings from
    load_land(), `stories` the STORIES list from data.py.
    Returns {story_number: (cx, cy)} of numbered-badge centres,
    in page units.
    """
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(img)

    # (1) Ocean.
    H.rect(d, x0, y0, x1, y1, fill=OCEAN)

    # (2) Land, filled through a mask clipped to the box. Rings can run
    # past the box edges (high latitudes, lon < -126), so the land mask
    # is ANDed with a box mask before compositing.
    land_mask = Image.new("L", img.size, 0)
    md = ImageDraw.Draw(land_mask)
    for ring in land:
        if len(ring) >= 3:
            md.polygon(_ring_canvas_points(ring, box), fill=255)
    land_mask = ImageChops.multiply(land_mask, _box_mask(img.size, box))
    land_layer = Image.new("RGB", img.size, LAND)
    img.paste(land_layer, (0, 0), land_mask)

    # (3) Dashed equator (lat 0): 3-px dashes every 6 px, page units.
    eq_y = lonlat_to_xy(0.0, 0.0, box)[1]
    eq_y_px = eq_y * S
    dash_px = int(round(3 * S))
    period_px = int(round(6 * S))
    eq_w = max(1, int(round(0.6 * S)))
    xx = int(round(x0 * S))
    x_end = int(round(x1 * S))
    while xx < x_end:
        d.line([(xx, eq_y_px), (min(xx + dash_px, x_end), eq_y_px)],
               fill=_EQUATOR_COLOUR, width=eq_w)
        xx += period_px

    # (4) Land outline, drawn on an overlay and pasted back clipped to
    # the box, so no outline spills onto the page outside the map.
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    ol_w = max(1, int(round(0.8 * S)))
    for ring in land:
        pts = _ring_canvas_points(ring, box)
        if len(pts) >= 2:
            od.line(pts + [pts[0]], fill=_OUTLINE_COLOUR + (255,),
                    width=ol_w)
    clip = ImageChops.multiply(overlay.split()[3], _box_mask(img.size, box))
    img.paste(overlay, (0, 0), clip)

    # True points of the numbered pins (stories 1-13) and the list dots.
    true_pt = {}
    for story in stories:
        if story["n"] <= 13 and story["lon"] is not None:
            true_pt[story["n"]] = lonlat_to_xy(story["lon"], story["lat"],
                                               box)

    # (5) List dots: stories 14-35 with coordinates, region colour,
    # white 0.7-px outline.
    for story in stories:
        if story["n"] >= 14 and story["lon"] is not None \
                and story["lat"] is not None:
            px, py = lonlat_to_xy(story["lon"], story["lat"], box)
            colour = REG[story["region"]]
            H.ellipse(d, px - _DOT_R, py - _DOT_R, px + _DOT_R, py + _DOT_R,
                      fill=colour, outline=WHITE, width=0.7)

    # (6) Numbered badges 1-13, most crowded pins first. Crowding =
    # number of other true points within 30 px; ties by story number.
    pins = [story for story in stories
            if story["n"] <= 13 and story["n"] in true_pt]

    def _crowding(story):
        tx, ty = true_pt[story["n"]]
        count = 0
        for other in pins:
            if other["n"] == story["n"]:
                continue
            ox, oy = true_pt[other["n"]]
            if math.hypot(tx - ox, ty - oy) <= 30.0:
                count += 1
        return count

    order = sorted(pins, key=lambda s: (-_crowding(s), s["n"]))

    # Candidate offsets: the true point, then rings of radius 10, 14,
    # 18, 22 px in 8 directions (0 deg = east, y grows downwards).
    candidates = [(0.0, 0.0)]
    for radius in (10, 14, 18, 22):
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            candidates.append((radius * math.cos(rad),
                               radius * math.sin(rad)))

    placed = {}          # story number -> (cx, cy)
    leaders = []         # (true point, badge centre, region colour)

    def _ok(cx, cy, unplaced_true):
        if not (x0 + 8 <= cx <= x1 - 8 and y0 + 8 <= cy <= y1 - 8):
            return False
        for (_, (bx, by)) in placed.items():
            if math.hypot(cx - bx, cy - by) < 15.0:
                return False
        for (ux, uy) in unplaced_true:
            if math.hypot(cx - ux, cy - uy) < 9.0:
                return False
        return True

    def _score(cx, cy, unplaced_true):
        """Best-effort score: smallest clearance to anything to avoid."""
        dists = [math.hypot(cx - bx, cy - by)
                 for (_, (bx, by)) in placed.items()]
        dists += [math.hypot(cx - ux, cy - uy)
                  for (ux, uy) in unplaced_true]
        return min(dists) if dists else 1e9

    for idx, story in enumerate(order):
        tx, ty = true_pt[story["n"]]
        unplaced_true = [true_pt[s["n"]] for s in order[idx + 1:]]
        chosen = None
        for (dx, dy) in candidates:
            cx, cy = tx + dx, ty + dy
            if _ok(cx, cy, unplaced_true):
                chosen = (cx, cy)
                break
        if chosen is None:
            # No spot passed every rule: take the candidate with the
            # largest clearance (deterministic, earliest wins ties).
            best_score = -1.0
            for (dx, dy) in candidates:
                cx, cy = tx + dx, ty + dy
                if not (x0 + 8 <= cx <= x1 - 8
                        and y0 + 8 <= cy <= y1 - 8):
                    continue
                sc = _score(cx, cy, unplaced_true)
                if sc > best_score:
                    best_score = sc
                    chosen = (cx, cy)
            if chosen is None:
                chosen = (tx, ty)
        placed[story["n"]] = chosen
        if math.hypot(chosen[0] - tx, chosen[1] - ty) > 0.01:
            leaders.append((tx, ty, chosen, REG[story["region"]]))

    # Leader lines + true-point dots first, so no line crosses a badge.
    for (tx, ty, (cx, cy), colour) in leaders:
        H.line(d, [(tx, ty), (cx, cy)], fill=colour, width=0.9)
        H.ellipse(d, tx - _TRUE_DOT_R, ty - _TRUE_DOT_R,
                  tx + _TRUE_DOT_R, ty + _TRUE_DOT_R, fill=colour)

    # All badges last.
    for story in pins:
        cx, cy = placed[story["n"]]
        H.badge(d, cx, cy, story["n"], REG[story["region"]],
                _BADGE_R, _BADGE_SIZE)

    return placed


def _no_pin_numbers(stories):
    """Numbers of stories with no coordinates, in story order."""
    return [story["n"] for story in stories
            if story["lon"] is None or story["lat"] is None]


def map_key_lines(stories):
    """Return (key1_text, key2_text), the two strings of the map key."""
    n = len(stories)
    key1 = "= stories 1–13"
    key2 = "= 14–%d (list)" % n
    no_pin = _no_pin_numbers(stories)
    if no_pin:
        key2 += "  ·  no pin: %s" % ", ".join(str(num) for num in no_pin)
    return key1, key2


def draw_map_key(d, x, y, stories):
    """Draw the map key at (x, y) (icon guide section 4).

    Grey badge "7", then key1 text starting at x+16; 12 px after that
    text a grey list dot, then the key2 text. Returns the y just below
    the key (y + 14).
    """
    key1, key2 = map_key_lines(stories)
    H.badge(d, x + 7, y + 7, 7, GREY, 6.6, 8.6)
    H.text(d, "map_key1", x + 16, y, key1, "cond", 10.8, INK, "la")
    w1 = H.text_w("cond", 10.8, key1)
    dot_cx = x + 16 + w1 + 12 + _DOT_R
    H.ellipse(d, dot_cx - _DOT_R, y + 7 - _DOT_R,
              dot_cx + _DOT_R, y + 7 + _DOT_R,
              fill=GREY, outline=WHITE, width=0.7)
    H.text(d, "map_key2", dot_cx + _DOT_R + 5, y, key2, "cond", 10.8,
           INK, "la")
    return y + 14


def draw_region_key(d, x, y):
    """Draw the region key at (x, y) (icon guide section 4).

    2 columns x 3 rows, 15 px apart, columns 150 px apart. Column 1:
    EUROPE, MIDDLE EAST, AFRICA; column 2: ASIA-PACIFIC, AMERICAS,
    WORLD. Each row: filled 9-px circle in the region colour and
    "{Region name} {count}" in cond_b 11 INK. Returns the y just
    below the key.
    """
    totals = data.region_totals()
    columns = (("EUROPE", "MIDDLE EAST", "AFRICA"),
               ("ASIA-PACIFIC", "AMERICAS", "WORLD"))
    for col, regions in enumerate(columns):
        col_x = x + col * 150
        for row, region in enumerate(regions):
            ry = y + row * 15
            H.ellipse(d, col_x + 1, ry + 3, col_x + 10, ry + 12,
                      fill=REG[region])
            H.text(d, "region_key_" + region, col_x + 14, ry,
                   "%s %d" % (REGION_NAMES[region], totals[region]),
                   "cond_b", 11, INK, "la")
    return y + 3 * 15
