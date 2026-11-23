#!/usr/bin/env python3
"""Prep step for the "World in One Day" newspaper map.

Downloads Natural Earth 1:110m land (public domain) as TopoJSON from
jsDelivr and converts it into a simple JSON list of [lon, lat] rings for
the map in the entry. Falls back to a local copy if the download fails.

Decode rules (TopoJSON spec):
- arcs are delta-encoded integer coordinates; undo the deltas to get
  absolute integers, then apply transform.scale and transform.translate
  to get real longitude/latitude.
- a negative arc index i refers to arc ~i (= -i - 1) traversed in reverse.
- joining arcs into a ring: concatenate the points, skipping the first
  point of each joined arc (it duplicates the previous arc's last point).
- keep every ring of the `land` object except Antarctica: drop rings
  whose highest latitude is below -55 degrees.
- round coordinates to 0.2 degrees, drop consecutive duplicates, and
  drop rings whose area is under 0.8 square degrees (shoelace formula).
- output rings with one decimal place.
"""

import json
import math
import os
import sys
import urllib.request

URL = "https://cdn.jsdelivr.net/npm/world-atlas@2/land-110m.json"
FALLBACK = "/tmp/land-110m.json"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "world_land.json")

ROUND_STEP = 0.2
MIN_AREA_SQ_DEG = 0.8
ANTARCTICA_MAX_LAT = -55.0


def load_topology():
    """Try the CDN first, fall back to the local copy. Returns (data, source)."""
    try:
        with urllib.request.urlopen(URL, timeout=30) as resp:
            raw = resp.read()
        print(f"downloaded {URL} ({len(raw)} bytes)")
        return json.loads(raw.decode("utf-8")), "download"
    except Exception as exc:  # network or decode failure -> local copy
        print(f"download failed ({exc}); using local fallback {FALLBACK}")
        with open(FALLBACK, "r", encoding="utf-8") as fh:
            return json.load(fh), "fallback"


def decode_arcs(topology):
    """Return the arcs as lists of [lon, lat] float points."""
    transform = topology["transform"]
    sx, sy = transform["scale"]
    tx, ty = transform["translate"]
    arcs = []
    for arc in topology["arcs"]:
        x = 0
        y = 0
        points = []
        for dx, dy in arc:
            x += dx
            y += dy
            points.append([x * sx + tx, y * sy + ty])
        arcs.append(points)
    return arcs


def arc_points(arcs, index):
    """Points of arc `index`; a negative index means the arc reversed."""
    if index >= 0:
        return arcs[index]
    return list(reversed(arcs[~index]))


def join_ring(arcs, arc_indices):
    """Join arcs into one ring, skipping each joined arc's first point."""
    ring = []
    for idx in arc_indices:
        pts = arc_points(arcs, idx)
        if not ring:
            ring.extend(pts)
        else:
            ring.extend(pts[1:])
    return ring


def collect_rings(topology, arcs):
    """All rings of the `land` object (Polygon and MultiPolygon)."""
    land = topology["objects"]["land"]
    rings = []
    for geom in land["geometries"]:
        if geom["type"] == "Polygon":
            polygons = [geom["arcs"]]
        elif geom["type"] == "MultiPolygon":
            polygons = geom["arcs"]
        else:
            continue
        for polygon in polygons:
            for arc_indices in polygon:
                rings.append(join_ring(arcs, arc_indices))
    return rings


def polygon_area_sq_deg(ring):
    """Absolute shoelace area of a ring, in square degrees."""
    total = 0.0
    n = len(ring)
    for i in range(n):
        x1, y1 = ring[i]
        x2, y2 = ring[(i + 1) % n]
        total += x1 * y2 - x2 * y1
    return abs(total) / 2.0


def simplify_ring(ring):
    """Round to 0.2 degrees and drop consecutive duplicates."""
    out = []
    for lon, lat in ring:
        lon = round(round(lon / ROUND_STEP) * ROUND_STEP, 1)
        lat = round(round(lat / ROUND_STEP) * ROUND_STEP, 1)
        if not out or out[-1] != [lon, lat]:
            out.append([lon, lat])
    # The ring closes on itself; drop a trailing duplicate of the first point.
    if len(out) > 1 and out[-1] == out[0]:
        out.pop()
    return out


def main():
    topology, source = load_topology()
    arcs = decode_arcs(topology)
    raw_rings = collect_rings(topology, arcs)

    kept = []
    dropped_antarctica = 0
    dropped_small = 0
    for ring in raw_rings:
        if not ring:
            continue
        max_lat = max(lat for _, lat in ring)
        if max_lat < ANTARCTICA_MAX_LAT:
            dropped_antarctica += 1
            continue
        simple = simplify_ring(ring)
        if len(simple) < 3 or polygon_area_sq_deg(simple) < MIN_AREA_SQ_DEG:
            dropped_small += 1
            continue
        kept.append(simple)

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(kept, fh)

    total_points = sum(len(r) for r in kept)
    print(f"source: {source}")
    print(f"raw rings: {len(raw_rings)}")
    print(f"dropped Antarctica: {dropped_antarctica}, dropped tiny: {dropped_small}")
    print(f"kept rings: {len(kept)}, total points: {total_points}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
