# build.py — assembles "The World in One Day", Sunday 22 November 2026.
# One-page newspaper, 35 stories, 1024x1024. Draws at 2x (2048x2048)
# with Pillow, downscales once with LANCZOS, quantizes to 256 colours,
# saves entry.png next to this file. Deterministic: no randomness,
# no clock, no network, fixed fonts/data. Layout from spec section 4;
# all drawing primitives / pictures / map come from the verified
# modules draw_helpers.py, pictures.py, map_draw.py and data.py.
# Run: python3 build.py

import hashlib
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import data
import draw_helpers as H
import map_draw
from pictures import PICTURES

HERE = os.path.dirname(os.path.abspath(__file__))
REG = data.REG


def shorten_to_lines(text, key, size, width, lh, max_lines):
    """Wrap text; while it needs more than max_lines, drop words from
    the end and add an ellipsis. Returns (lines, total_h, final_text)."""
    cur = text
    while True:
        lines, total_h = H.wrap([(cur, key, size, data.INK)], width, lh)
        if len(lines) <= max_lines:
            return lines, total_h, cur
        words = cur.rstrip("…").split(" ")
        if len(words) <= 1:
            return lines, total_h, cur
        cur = " ".join(words[:-1]) + "…"


def shorten_what(what, key, size, avail):
    """Shorten a list-row 'what' by dropping words + '…' until it fits
    the available width. Returns the (possibly shortened) text."""
    cur = what
    while H.text_w(key, size, cur) > avail and " " in cur.rstrip("…"):
        cur = " ".join(cur.rstrip("…").split(" ")[:-1]) + "…"
    return cur


def main():
    H.reset_registry()
    img = Image.new("RGB", (2048, 2048), data.PAPER)
    d = ImageDraw.Draw(img)

    # ---------------------------------------------------------- kicker (y=4)
    H.text(d, "kicker_l", 12, 4,
           "THE WORLD IN ONE DAY · CLOSING EDITION",
           "cond_b", 12.5, data.RED, anchor="la")
    H.text(d, "kicker_r", 1012, 4,
           "%d STORIES · 6 REGIONS · 6 TOPICS · TIMES IN UTC" % data.N,
           "cond_b", 12.5, data.INK, anchor="ra")

    # -------------------------------------------------------- masthead (y=17)
    H.text(d, "masthead", 512, 17, "Sunday 22 November 2026",
           "serif_b", 74, data.INK, anchor="ma")

    # ------------------------------------------------------- double rule
    H.rect(d, 12, 98, 1012, 98 + 2.2, fill=data.INK)
    H.rect(d, 12, 101, 1012, 101 + 0.7, fill=data.INK)

    # ------------------------------------------------------------ deck (y=104)
    H.text(d, "deck", 512, 104, data.DECK, "serif_i", 17, data.RED,
           anchor="ma")

    # ---------------------------------------------- coverage strip (y=124)
    H.rect(d, 12, 124, 1012, 143, fill=data.WHITE, outline=data.NAVY,
           width=1)
    cov_x = 18
    H.text(d, "cov_label", cov_x, 126.8, "COVERAGE", "cond_b", 11.6,
           data.NAVY, anchor="la")
    cov_x += H.text_w("cond_b", 11.6, "COVERAGE") + 10
    region_totals = data.region_totals()
    for region in data.REGIONS:
        H.ellipse(d, cov_x, 129, cov_x + 9, 138,
                  fill=data.REG[region])
        label = "%s %d" % (data.REGION_NAMES[region],
                           region_totals[region])
        H.text(d, "cov_region_" + region, cov_x + 12, 126.8, label,
               "cond_b", 11.6, data.INK, anchor="la")
        cov_x += 12 + H.text_w("cond_b", 11.6, label) + 10
    rule_x = cov_x - 3
    H.line(d, [(rule_x, 128), (rule_x, 139)], fill=data.RULE, width=1)
    cov_x = rule_x + 6
    topic_totals = data.topic_totals()
    topic_order = ["CONFLICT", "POLITICS", "ECONOMY", "DISASTER",
                   "SOCIETY", "SPORT"]
    topic_parts = ["%s %d" % (t.capitalize(), topic_totals.get(t, 0))
                   for t in topic_order if topic_totals.get(t, 0)]
    topic_text = "  ·  ".join(topic_parts)
    H.text(d, "cov_topics", cov_x, 126.8, topic_text, "cond", 11.6,
           data.INK, anchor="la")
    cov_end = cov_x + H.text_w("cond", 11.6, topic_text)
    print("coverage strip ends at x=%.1f (must be <= 1006)" % cov_end)
    assert cov_end <= 1006, "coverage strip too wide: %.1f" % cov_end

    # ---------------------------------------------------- background bar (y=146)
    H.rect(d, 12, 146, 1012, 163, fill=(234, 230, 220))
    H.text(d, "bg_label", 18, 146 + 3, "BACKGROUND", "cond_b", 11.5,
           data.NAVY, anchor="la")
    bg_x = 18 + H.text_w("cond_b", 11.5, "BACKGROUND") + 6
    H.text(d, "bg_text", bg_x, 146 + 3, data.BACKGROUND, "cond", 11.5,
           data.INK, anchor="la")

    # --------------------------------------------------------- timeline (y=168)
    H.rect(d, 12, 168, 76, 204, fill=data.RED)
    H.text(d, "tl_box_day", 44, 168 + 5, "THE DAY", "cond_b", 11.5,
           data.WHITE, anchor="ma")
    H.text(d, "tl_box_utc", 44, 168 + 19, "IN UTC", "cond_b", 11.5,
           data.WHITE, anchor="ma")
    for i, (time_s, qual, event) in enumerate(data.TIMELINE):
        col_x = 84 + 116 * i
        if i > 0:
            sep_x = col_x - 5
            H.line(d, [(sep_x, 168), (sep_x, 168 + 40)], fill=data.RULE,
                   width=1)
        H.text(d, "tl_time_%d" % i, col_x, 168 + 1, time_s, "serif_b", 17,
               data.RED, anchor="la")
        if qual:
            qx = col_x + H.text_w("serif_b", 17, time_s) + 4
            H.text(d, "tl_qual_%d" % i, qx, 168 + 6, qual, "cond", 10.6,
                   data.GREY, anchor="la")
        ev_w = H.text_w("cond_b", 11.2, event)
        assert ev_w <= 108, "timeline event too wide: %r %.1f" % (event, ev_w)
        H.text(d, "tl_event_%d" % i, col_x, 168 + 21, event, "cond_b",
               11.2, data.INK, anchor="la")
    H.rect(d, 12, 168 + 40, 1012, 168 + 40 + 0.9, fill=data.INK)

    # ------------------------------------------------------------ leads (y=213)
    leads_y = 213
    lead_pic_h = 96
    lead_xs = [12, 350, 688]
    col_bottoms = []
    for story, x in zip(data.LEADS, lead_xs):
        n = story["n"]
        H.panel(d, img, PICTURES[story["picture"]], x, leads_y, x + 324,
                leads_y + lead_pic_h, story["place_bar"], story["label"],
                17, 10.5, sources=None)
        kicker_y = leads_y + lead_pic_h + 5
        H.badge(d, x + 9, kicker_y + 8, n, REG[story["region"]], 9, 11)
        kicker = "%s · %s" % (story["region"], story["field"])
        H.text(d, "lead_kicker_%d" % n, x + 22, kicker_y, kicker,
               "cond_b", 11, REG[story["region"]], anchor="la")
        H.tag_chip(d, story["tag"], story["tag_extra"], x + 324, kicker_y)
        y = kicker_y + 21
        lines, hh = H.wrap([(story["headline"], "serif_b", 24, data.INK)],
                           324, 25.4)
        y += H.draw_wrapped(d, "lead_head_%d" % n, lines, x, y, 25.4) + 4
        lines, hh = H.wrap([(story["body"], "serif", 13.4, data.INK)],
                           324, 15.2)
        assert len(lines) == 2, \
            "lead %d body not 2 lines: %d" % (n, len(lines))
        y += H.draw_wrapped(d, "lead_body_%d" % n, lines, x, y, 15.2)
        # "Why it matters" line, 3 px below the body's last line.
        why_y = y + 3
        H.rect(d, x, why_y - 1, x + 3, why_y + 13,
               fill=REG[story["region"]])
        why_runs = [("Why it matters:", "cond_b", 12,
                     REG[story["region"]]),
                    (story["why"], "cond_b", 12, data.INK)]
        why_lines, why_h = H.wrap(why_runs, 324 - 8, 14)
        assert len(why_lines) <= 2, \
            "lead %d why over 2 lines: %d" % (n, len(why_lines))
        H.draw_wrapped(d, "lead_why_%d" % n, why_lines, x + 8, why_y, 14)
        y = why_y + why_h + 2
        bb = H.text(d, "lead_src_%d" % n, x, y, story["sources"],
                    "cond_b", 10.6, data.GREY, anchor="la")
        col_bottoms.append(bb[3] + 2)
    leads_rule_y = max(col_bottoms) + 2
    H.rect(d, 12, leads_rule_y, 1012, leads_rule_y + 1.4, fill=data.INK)

    # ------------------------------------------------------------- cards
    cards_y = leads_rule_y + 6
    card_w = 190.4
    for idx, story in enumerate(data.CARDS):
        r, c = idx // 5, idx % 5
        x = 12 + c * (card_w + 12)
        y = cards_y + r * 138.8
        n = story["n"]
        H.panel(d, img, PICTURES[story["picture"]], x, y, x + card_w,
                y + 64, story["place_bar"], story["label"], 13, 9.6,
                sources=story["sources"])
        H.badge(d, x + 8, y + 67 + 7.5, n, REG[story["region"]], 8, 10)
        kicker = "%s · %s" % (data.FIELD_TOPICS[story["field"]],
                              story["field"])
        H.text(d, "card_kicker_%d" % n, x + 19, y + 67, kicker, "cond_b",
               10.4, REG[story["region"]], anchor="la")
        H.certainty_icon(d, story["tag"], x + card_w - 8, y + 67 + 7.5, 7)
        lines, hh, final_head = shorten_to_lines(
            story["headline"], "dserif_b", 14.6, card_w, 15.6, 3)
        if final_head != story["headline"]:
            print("card %d headline shortened to: %s" % (n, final_head))
        H.draw_wrapped(d, "card_head_%d" % n, lines, x, y + 83, 15.6)
    cards_rule_y = cards_y + 138.8 + 138.8
    H.rect(d, 12, cards_rule_y, 1012, cards_rule_y + 1.4, fill=data.INK)

    # ------------------------------------------------------- map + list row
    row_y = cards_rule_y + 6
    H.text(d, "map_title", 12, row_y,
           "WHERE ALL %d STORIES HAPPENED" % data.N, "cond_b", 11.4,
           data.NAVY, anchor="la")
    map_box = (12, row_y + 16, 312, row_y + 16 + 102)
    land = map_draw.load_land(os.path.join(HERE, "world_land.json"))
    map_draw.draw_map(img, map_box, land, data.STORIES)
    map_key_bottom = map_draw.draw_map_key(
        d, 12, row_y + 16 + 102 + 4, data.STORIES)

    # "What we don't know yet" box, left column under the map key.
    dk_top = map_key_bottom + 2
    dk_bottom = 967 - 5
    H.rect(d, 12, dk_top, 312, dk_bottom, fill=(246, 243, 234),
           outline=(176, 112, 8), width=1)
    H.text(d, "dk_title", 18, dk_top + 2.5, "WHAT WE DON’T KNOW YET",
           "cond_b", 11.4, (150, 92, 6), anchor="la")
    dk_items = [
        ("Merkury:", "who struck it; no one has claimed it"),
        ("Chabahar:", "which forces; UKMTO did not say"),
        ("Dymer:", "the final toll; people were still trapped"),
        ("Ebola:", "WHO’s latest count is from 17 Nov"),
    ]
    dk_spacing = (dk_bottom - 3 - (dk_top + 16) - 11.4) / 3.0
    for i, (lead, rest) in enumerate(dk_items):
        ly = dk_top + 16 + i * dk_spacing
        lead_w = H.text_w("cond_b", 11.4, lead)
        H.text(d, "dk_lead_%d" % i, 18, ly, lead, "cond_b", 11.4,
               data.INK, anchor="la")
        H.text(d, "dk_text_%d" % i, 18 + lead_w + 4, ly, rest, "cond",
               11.4, data.INK, anchor="la")

    # List (right).
    H.text(d, "list_head", 326, row_y,
           "ALSO ON SUNDAY 22 NOVEMBER — %d MORE STORIES"
           % len(data.BRIEFS), "cond_b", 11.4, data.NAVY, anchor="la")
    H.text(d, "list_sub", 1012, row_y,
           "place · what happened · source · how sure", "cond", 10.6,
           data.GREY, anchor="ra")
    H.line(d, [(669, row_y + 16), (669, 967 - 4)], fill=data.RULE, width=1)
    available = (967 - 4) - (row_y + 16)
    row_h = available / 11.0
    cols = [(326, 337), (675, 337)]
    for bi, story in enumerate(data.BRIEFS):
        col_idx = 0 if bi < 11 else 1
        row_i = bi if bi < 11 else bi - 11
        col_x, col_w = cols[col_idx]
        row_top = row_y + 16 + row_i * row_h
        n = story["n"]
        H.square_badge(d, col_x + 9, row_top + 8.5, n,
                       REG[story["region"]])
        # Source first (right-aligned) so the "what" can be measured
        # against where the source text actually starts.
        src_w = H.text_w("cond", 11.4, story["sources"])
        src_left = col_x + col_w - 17 - src_w
        H.text(d, "list_src_%d" % n, col_x + col_w - 17, row_top,
               story["sources"], "cond", 11.4, data.GREY, anchor="ra")
        place_bb = H.text(d, "list_place_%d" % n, col_x + 21, row_top,
                          story["place"], "cond_b", 13.8,
                          REG[story["region"]], anchor="la")
        what_x = place_bb[2] + 5
        what = shorten_what(story["what"], "cond", 13.8,
                            (src_left - 5) - what_x)
        if what != story["what"]:
            print("brief %d what shortened to: %s" % (n, what))
        H.text(d, "list_what_%d" % n, what_x, row_top, what, "cond",
               13.8, data.INK, anchor="la")
        H.certainty_icon(d, story["tag"], col_x + col_w - 7,
                         row_top + 8.5, 6.8)

    # ------------------------------------------------- date check strip (y=967)
    H.rect(d, 12, 967, 1012, 1001, fill=(251, 240, 236),
           outline=data.RED, width=1.1)
    label_w = H.text_w("sans_b", 11.4, "DATE CHECK") + 10
    label_h = 11.4 + 6
    H.rect(d, 18, 975, 18 + label_w, 975 + label_h, fill=data.RED)
    H.text(d, "datecheck_label", 18 + 5, 975 + 2.4, "DATE CHECK",
           "sans_b", 11.4, data.WHITE, anchor="la")
    runs = []
    for lead, rest in data.date_check_lines():
        if lead:
            runs.append((lead, "cond_b", 11.8, data.RED))
        runs.append((rest, "cond", 11.8, data.INK))
    dc_w = 1012 - (18 + label_w + 18) - 12
    dc_lines, dc_h = H.wrap(runs, dc_w, 13.6)
    print("date check lines: %d (width %.1f)" % (len(dc_lines), dc_w))
    H.draw_wrapped(d, "datecheck", dc_lines, 18 + label_w + 18, 971, 13.6)

    # ------------------------------------------------------------ footer (y=1006)
    H.text(d, "footer_howsure", 12, 1006, "HOW SURE", "cond_b", 11.8,
           data.INK, anchor="la")
    fx = 12 + H.text_w("cond_b", 11.8, "HOW SURE") + 12
    for kind, definition in data.CERTAINTY_DEFS:
        H.certainty_icon(d, kind, fx + 7.5, 1013, 7.5)
        kind_label = kind + ":"
        H.text(d, "footer_kind_" + kind, fx + 18, 1006, kind_label,
               "cond_b", 10, data.INK, anchor="la")
        def_x = (fx + 18 + H.text_w("cond_b", 10, kind_label)
                 + H.text_w("cond", 11.8, " "))
        H.text(d, "footer_def_" + kind, def_x, 1006, definition,
               "cond", 11.8, data.INK, anchor="la")
        fx = def_x + H.text_w("cond", 11.8, definition) + 8
    H.text(d, "footer_drawings", 1012, 1006, "Drawings, not photos",
           "cond", 11.8, data.GREY, anchor="ra")
    print("footer legend ends at x=%.1f; drawings starts at %.1f"
          % (fx, 1012 - H.text_w("cond", 11.8, "Drawings, not photos")))

    # ------------------------------------------------------- registry check
    problems = H.check_problems()
    print("text registry problems (%d):" % len(problems))
    for p in problems:
        print("  " + p)
    print("leads rule y=%.1f cards_y=%.1f cards rule y=%.1f "
          "map/list row y=%.1f row_h=%.2f"
          % (leads_rule_y, cards_y, cards_rule_y, row_y, row_h))
    if problems:
        sys.exit("registry problems remain: %d" % len(problems))

    # ------------------------------------------------------- downscale + save
    out = img.resize((1024, 1024), Image.LANCZOS)
    out = out.quantize(colors=256, method=Image.MEDIANCUT,
                       dither=Image.NONE)
    path = os.path.join(HERE, "entry.png")
    out.save(path, optimize=True)
    raw = open(path, "rb").read()
    print("wrote %s: 1024x1024, %d bytes, sha256 %s"
          % (path, len(raw), hashlib.sha256(raw).hexdigest()))


if __name__ == "__main__":
    main()
