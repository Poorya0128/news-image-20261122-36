# data.py — pure data for "The World in One Day", Sunday 22 November 2026.
# One-page newspaper, 35 stories, 1024x1024. Transcribed word-for-word from
# the build spec (agent_spec_news-image-20261122.md, v8, plus v9 change list).
# Standard library only; no Pillow, no imports at all. Every count is
# computed from STORIES.

# ---------------------------------------------------------------- colours
PAPER = (247, 244, 236)
INK = (20, 22, 28)
GREY = (96, 98, 106)
RULE = (205, 199, 186)
RED = (176, 22, 30)
NAVY = (16, 34, 64)
WHITE = (255, 255, 255)
GOLD = (250, 206, 102)
BAR = (16, 22, 34)        # place bars on picture panels
SRC = (196, 204, 220)     # card source text in the place bar
OCEAN = (222, 232, 241)
LAND = (206, 197, 178)

REG = {
    "EUROPE": (34, 88, 166),
    "MIDDLE EAST": (190, 92, 14),
    "ASIA-PACIFIC": (18, 122, 132),
    "AFRICA": (40, 122, 72),
    "AMERICAS": (112, 60, 156),
    "WORLD": (88, 88, 96),
}

CERT = {
    "CONFIRMED": (24, 122, 64),
    "STATED": (176, 112, 8),
    "UNVERIFIED": (192, 54, 30),
}

REGIONS = ["EUROPE", "MIDDLE EAST", "ASIA-PACIFIC", "AFRICA", "AMERICAS", "WORLD"]

REGION_NAMES = {
    "EUROPE": "Europe",
    "MIDDLE EAST": "Middle East",
    "ASIA-PACIFIC": "Asia & Pacific",
    "AFRICA": "Africa",
    "AMERICAS": "Americas",
    "WORLD": "World",
}

# ------------------------------------------------------- field -> topic (5.6)
FIELD_TOPICS = {
    "ACCIDENT": "DISASTER",
    "CLIMATE": "POLITICS",
    "COALITION": "POLITICS",
    "CRICKET": "SPORT",
    "CRYPTO": "ECONOMY",
    "DEFENCE": "CONFLICT",
    "DIPLOMACY": "POLITICS",
    "EARTHQUAKE": "DISASTER",
    "EDUCATION": "SOCIETY",
    "ELECTIONS": "POLITICS",
    "ENERGY": "ECONOMY",
    "EPIDEMIC": "SOCIETY",
    "FOOTBALL": "SPORT",
    "GAZA": "CONFLICT",
    "HEALTH POLICY": "POLITICS",
    "INDUSTRIAL FIRE": "DISASTER",
    "MARKETS": "ECONOMY",
    "MOTORSPORT": "SPORT",
    "NAVAL WAR": "CONFLICT",
    "PRESS FREEDOM": "POLITICS",
    "PROTEST": "POLITICS",
    "SHIPPING": "CONFLICT",
    "SUDAN WAR": "CONFLICT",
    "TECH & SPEECH": "POLITICS",
    "TENNIS": "SPORT",
    "UKRAINE WAR": "CONFLICT",
    "US POLITICS": "POLITICS",
    "WEATHER": "DISASTER",
    "WEST BANK": "CONFLICT",
}

# ---------------------------------------------------------------- stories
# Keys: n, region, field, topic, place, place_bar, headline, body, what,
# sources, tag, tag_extra, lon, lat, picture, label.
# - headline: leads 1-3 and cards 4-13 use the spec headline; briefs 14-35
#   use the "what happened" text as the headline too.
# - body: leads 1-3 only (exact wording from spec 5.3); "" otherwise.
# - what: briefs 14-35 (the "what happened" text); "" for leads/cards.
# - place_bar: the place name shown in the picture bar (leads/cards); for
#   briefs it is the same as place (no picture panel).
# - lon/lat: leads/cards from spec 5.7; briefs from the Lon,Lat column in
#   5.5; story 35 has none -> None, None.
STORIES = [
    # ---- leads (1-3) ----
    {
        "n": 1, "region": "WORLD", "field": "CLIMATE",
        "topic": FIELD_TOPICS["CLIMATE"],
        "place": "ANTALYA, TÜRKİYE", "place_bar": "ANTALYA, TÜRKİYE",
        "headline": "COP31 ends with no deal on fossil fuels",
        "body": "Longest UN climate summit on record ends with no final "
                "text; the EU and others reject a draft silent on fossil fuels.",
        "why": "Nearly 200 nations leave with no agreed step away from "
               "fossil fuels.",
        "what": "",
        "sources": "UN News · Reuters · NPR",
        "tag": "CONFIRMED", "tag_extra": "",
        "lon": 30.7, "lat": 36.9,
        "picture": "cop", "label": "NO DEAL",
    },
    {
        "n": 2, "region": "EUROPE", "field": "UKRAINE WAR",
        "topic": FIELD_TOPICS["UKRAINE WAR"],
        "place": "DYMER, NORTH OF KYIV", "place_bar": "DYMER, NORTH OF KYIV",
        "headline": "Russia fires 186 drones at Ukraine; 11 dead near Kyiv",
        "body": "A five-storey block in Dymer collapsed; a woman of 79 was "
                "pulled out alive. 161 drones were downed or jammed.",
        "why": "25 of 186 got through; one brought down a block of flats near the capital.",
        "what": "",
        "sources": "Ukraine Air Force · Ukrainska Pravda · AP",
        "tag": "CONFIRMED", "tag_extra": "",
        "lon": 30.3, "lat": 50.9,
        "picture": "dymer", "label": "11 DEAD",
    },
    {
        "n": 3, "region": "AFRICA", "field": "NAVAL WAR",
        "topic": FIELD_TOPICS["NAVAL WAR"],
        "place": "BENGHAZI, LIBYA", "place_bar": "BENGHAZI, LIBYA",
        "headline": "Russian warship capsizes in a Libyan port",
        "body": "Blasts around 01:00 UTC; by morning the Russian corvette "
                "Merkury lies capsized, bow up. No one has claimed it.",
        "why": "A Russian Navy warship hit in a foreign port, far from Ukraine.",
        "what": "",
        "sources": "AP · BBC Verify · The Guardian",
        "tag": "UNVERIFIED", "tag_extra": "WHO STRUCK",
        "lon": 20.1, "lat": 32.1,
        "picture": "benghazi", "label": "CAPSIZED",
    },
    # ---- picture cards (4-13) ----
    {
        "n": 4, "region": "MIDDLE EAST", "field": "ENERGY",
        "topic": FIELD_TOPICS["ENERGY"],
        "place": "IRAN", "place_bar": "IRAN",
        "headline": "Fuel shortage and war damage force rolling power cuts across Iran",
        "body": "", "what": "",
        "sources": "Tavanir, Rudaw",
        "tag": "CONFIRMED", "tag_extra": "",
        "lon": 51.4, "lat": 35.7,
        "picture": "power", "label": "2 HRS",
    },
    {
        "n": 5, "region": "MIDDLE EAST", "field": "SHIPPING",
        "topic": FIELD_TOPICS["SHIPPING"],
        "place": "GULF OF OMAN", "place_bar": "GULF OF OMAN",
        "headline": "UKMTO: tanker in incident with unnamed military forces off Iran",
        "body": "", "what": "",
        "sources": "UKMTO, Euronews",
        "tag": "STATED", "tag_extra": "",
        "lon": 60.6, "lat": 25.3,
        "picture": "tanker", "label": "UKMTO ALERT",
    },
    {
        "n": 6, "region": "MIDDLE EAST", "field": "WEST BANK",
        "topic": FIELD_TOPICS["WEST BANK"],
        "place": "WEST BANK", "place_bar": "WEST BANK",
        "headline": "Settlers torch Palestinian homes; Israel’s Eisenkot calls it “Jewish terror”",
        "body": "", "what": "",
        "sources": "Guardian, ToI",
        "tag": "CONFIRMED", "tag_extra": "",
        "lon": 35.2, "lat": 32.0,
        "picture": "westbank", "label": "ARSON",
    },
    {
        "n": 7, "region": "AFRICA", "field": "EPIDEMIC",
        "topic": FIELD_TOPICS["EPIDEMIC"],
        "place": "ITURI, DR CONGO", "place_bar": "ITURI, DR CONGO",
        "headline": "Fighting in Congo stalls Ebola response; WHO pleads for peace",
        "body": "", "what": "",
        "sources": "Reuters, WHO",
        "tag": "CONFIRMED", "tag_extra": "",
        "lon": 30.2, "lat": 1.6,
        "picture": "ebola", "label": "11,613 IN DRC",
    },
    {
        "n": 8, "region": "AFRICA", "field": "SUDAN WAR",
        "topic": FIELD_TOPICS["SUDAN WAR"],
        "place": "KHARTOUM", "place_bar": "KHARTOUM",
        "headline": "Overnight drone strikes on Khartoum kill at least 4 and hit a UN site",
        "body": "", "what": "",
        "sources": "AFP, Xinhua",
        "tag": "CONFIRMED", "tag_extra": "",
        "lon": 32.5, "lat": 15.6,
        "picture": "khartoum", "label": "UN SITE HIT",
    },
    {
        "n": 9, "region": "EUROPE", "field": "PRESS FREEDOM",
        "topic": FIELD_TOPICS["PRESS FREEDOM"],
        "place": "ISTANBUL", "place_bar": "ISTANBUL",
        "headline": "Istanbul march for press freedom after police seize Sözcü TV",
        "body": "", "what": "",
        "sources": "DW, AP",
        "tag": "CONFIRMED", "tag_extra": "",
        "lon": 28.9, "lat": 41.0,
        "picture": "istanbul", "label": "THOUSANDS",
    },
    {
        "n": 10, "region": "ASIA-PACIFIC", "field": "ELECTIONS",
        "topic": FIELD_TOPICS["ELECTIONS"],
        "place": "HONG KONG", "place_bar": "HONG KONG",
        "headline": "Record turnout in Hong Kong vote for body that picks city leader",
        "body": "", "what": "",
        "sources": "HK Govt, RTHK",
        "tag": "CONFIRMED", "tag_extra": "",
        "lon": 114.2, "lat": 22.3,
        "picture": "hk", "label": "98.79%",
    },
    {
        "n": 11, "region": "ASIA-PACIFIC", "field": "EDUCATION",
        "topic": FIELD_TOPICS["EDUCATION"],
        "place": "SEOUL", "place_bar": "SEOUL",
        "headline": "South Korea’s education minister quits over AI cheating chaos at exams",
        "body": "", "what": "",
        "sources": "Chosun, Guardian",
        "tag": "CONFIRMED", "tag_extra": "",
        "lon": 127.0, "lat": 37.6,
        "picture": "seoul", "label": "RESIGNS",
    },
    {
        "n": 12, "region": "AMERICAS", "field": "US POLITICS",
        "topic": FIELD_TOPICS["US POLITICS"],
        "place": "WASHINGTON", "place_bar": "WASHINGTON",
        "headline": "Foxx concedes; Democrats hit 258 House seats, most since 1992",
        "body": "", "what": "",
        "sources": "AP, CBS",
        "tag": "CONFIRMED", "tag_extra": "",
        "lon": -77.0, "lat": 38.9,
        "picture": "house", "label": "258 SEATS",
    },
    {
        "n": 13, "region": "EUROPE", "field": "TENNIS",
        "topic": FIELD_TOPICS["TENNIS"],
        "place": "TURIN", "place_bar": "TURIN",
        "headline": "Alcaraz beats world No 1 Zverev to win his first ATP Finals title",
        "body": "", "what": "",
        "sources": "ATP, ESPN",
        "tag": "CONFIRMED", "tag_extra": "",
        "lon": 7.7, "lat": 45.1,
        "picture": "tennis", "label": "6-2 7-6",
    },
    # ---- list briefs (14-35) ----
    {
        "n": 14, "region": "EUROPE", "field": "UKRAINE WAR",
        "topic": FIELD_TOPICS["UKRAINE WAR"],
        "place": "Vyshneve", "place_bar": "Vyshneve",
        "headline": "supermarket hit, 3 killed",
        "body": "", "what": "supermarket hit, 3 killed",
        "sources": "Kyiv Indep.",
        "tag": "STATED", "tag_extra": "",
        "lon": 30.36, "lat": 50.39,
        "picture": None, "label": None,
    },
    {
        "n": 15, "region": "EUROPE", "field": "UKRAINE WAR",
        "topic": FIELD_TOPICS["UKRAINE WAR"],
        "place": "Kyiv", "place_bar": "Kyiv",
        "headline": "Zelensky: 165 missiles in 7 days",
        "body": "", "what": "Zelensky: 165 missiles in 7 days",
        "sources": "Al Jazeera",
        "tag": "STATED", "tag_extra": "",
        "lon": 30.52, "lat": 50.45,
        "picture": None, "label": None,
    },
    {
        "n": 16, "region": "EUROPE", "field": "UKRAINE WAR",
        "topic": FIELD_TOPICS["UKRAINE WAR"],
        "place": "Krasnodar", "place_bar": "Krasnodar",
        "headline": "drones hit security HQ",
        "body": "", "what": "drones hit security HQ",
        "sources": "Kyiv Post",
        "tag": "UNVERIFIED", "tag_extra": "",
        "lon": 38.98, "lat": 45.04,
        "picture": None, "label": None,
    },
    {
        "n": 17, "region": "EUROPE", "field": "UKRAINE WAR",
        "topic": FIELD_TOPICS["UKRAINE WAR"],
        "place": "Finland", "place_bar": "Finland",
        "headline": "drone-hit ship towed away",
        "body": "", "what": "drone-hit ship towed away",
        "sources": "Coastguard",
        "tag": "CONFIRMED", "tag_extra": "",
        "lon": 25.00, "lat": 60.00,
        "picture": None, "label": None,
    },
    {
        "n": 18, "region": "EUROPE", "field": "FOOTBALL",
        "topic": FIELD_TOPICS["FOOTBALL"],
        "place": "Anfield", "place_bar": "Anfield",
        "headline": "Liverpool 4–0 Man United",
        "body": "", "what": "Liverpool 4–0 Man United",
        "sources": "LFC, Sky",
        "tag": "CONFIRMED", "tag_extra": "",
        "lon": -2.96, "lat": 53.43,
        "picture": None, "label": None,
    },
    {
        "n": 19, "region": "MIDDLE EAST", "field": "COALITION",
        "topic": FIELD_TOPICS["COALITION"],
        "place": "Israel", "place_bar": "Israel",
        "headline": "unity-government talks: no deal",
        "body": "", "what": "unity-government talks: no deal",
        "sources": "AJ, Ynet",
        "tag": "CONFIRMED", "tag_extra": "",
        "lon": 34.85, "lat": 32.08,
        "picture": None, "label": None,
    },
    {
        "n": 20, "region": "MIDDLE EAST", "field": "GAZA",
        "topic": FIELD_TOPICS["GAZA"],
        "place": "Gaza", "place_bar": "Gaza",
        "headline": "4 killed despite truce",
        "body": "", "what": "4 killed despite truce",
        "sources": "Health Min.",
        "tag": "STATED", "tag_extra": "",
        "lon": 34.45, "lat": 31.50,
        "picture": None, "label": None,
    },
    {
        "n": 21, "region": "MIDDLE EAST", "field": "DIPLOMACY",
        "topic": FIELD_TOPICS["DIPLOMACY"],
        "place": "Doha", "place_bar": "Doha",
        "headline": "no imminent US–Iran deal",
        "body": "", "what": "no imminent US–Iran deal",
        "sources": "Jiji",
        "tag": "STATED", "tag_extra": "",
        "lon": 51.53, "lat": 25.29,
        "picture": None, "label": None,
    },
    {
        "n": 22, "region": "AFRICA", "field": "ACCIDENT",
        "topic": FIELD_TOPICS["ACCIDENT"],
        "place": "Nigeria", "place_bar": "Nigeria",
        "headline": "funeral-boat toll rises to 24",
        "body": "", "what": "funeral-boat toll rises to 24",
        "sources": "NEMA",
        "tag": "CONFIRMED", "tag_extra": "",
        "lon": 8.00, "lat": 10.00,
        "picture": None, "label": None,
    },
    {
        "n": 23, "region": "AFRICA", "field": "SUDAN WAR",
        "topic": FIELD_TOPICS["SUDAN WAR"],
        "place": "Sudan", "place_bar": "Sudan",
        "headline": "RSF commander defects",
        "body": "", "what": "RSF commander defects",
        "sources": "Ahram",
        "tag": "UNVERIFIED", "tag_extra": "",
        "lon": 30.00, "lat": 15.00,
        "picture": None, "label": None,
    },
    {
        "n": 24, "region": "AFRICA", "field": "ELECTIONS",
        "topic": FIELD_TOPICS["ELECTIONS"],
        "place": "Kenya", "place_bar": "Kenya",
        "headline": "govt: tally 2027 vote in Nairobi",
        "body": "", "what": "govt: tally 2027 vote in Nairobi",
        "sources": "Dawan",
        "tag": "STATED", "tag_extra": "",
        "lon": 36.82, "lat": -1.29,
        "picture": None, "label": None,
    },
    {
        "n": 25, "region": "ASIA-PACIFIC", "field": "INDUSTRIAL FIRE",
        "topic": FIELD_TOPICS["INDUSTRIAL FIRE"],
        "place": "Serang", "place_bar": "Serang",
        "headline": "plant fire: 3 dead, 36 missing",
        "body": "", "what": "plant fire: 3 dead, 36 missing",
        "sources": "Basarnas",
        "tag": "CONFIRMED", "tag_extra": "",
        "lon": 106.15, "lat": -6.12,
        "picture": None, "label": None,
    },
    {
        "n": 26, "region": "ASIA-PACIFIC", "field": "CRICKET",
        "topic": FIELD_TOPICS["CRICKET"],
        "place": "Wellington", "place_bar": "Wellington",
        "headline": "India 720/9, record in NZ",
        "body": "", "what": "India 720/9, record in NZ",
        "sources": "ESPN, TOI",
        "tag": "CONFIRMED", "tag_extra": "",
        "lon": 174.78, "lat": -41.29,
        "picture": None, "label": None,
    },
    {
        "n": 27, "region": "ASIA-PACIFIC", "field": "PROTEST",
        "topic": FIELD_TOPICS["PROTEST"],
        "place": "Bangladesh", "place_bar": "Bangladesh",
        "headline": "~30 homes torched in unrest",
        "body": "", "what": "~30 homes torched in unrest",
        "sources": "PTI",
        "tag": "STATED", "tag_extra": "",
        "lon": 90.41, "lat": 23.81,
        "picture": None, "label": None,
    },
    {
        "n": 28, "region": "ASIA-PACIFIC", "field": "DEFENCE",
        "topic": FIELD_TOPICS["DEFENCE"],
        "place": "Canberra", "place_bar": "Canberra",
        "headline": "Marles hits back on AUKUS",
        "body": "", "what": "Marles hits back on AUKUS",
        "sources": "Reuters",
        "tag": "STATED", "tag_extra": "",
        "lon": 149.13, "lat": -35.28,
        "picture": None, "label": None,
    },
    {
        "n": 29, "region": "ASIA-PACIFIC", "field": "MARKETS",
        "topic": FIELD_TOPICS["MARKETS"],
        "place": "China", "place_bar": "China",
        "headline": "stock margin cut to 80%",
        "body": "", "what": "stock margin cut to 80%",
        "sources": "3 exchanges",
        "tag": "CONFIRMED", "tag_extra": "",
        "lon": 121.47, "lat": 31.23,
        "picture": None, "label": None,
    },
    {
        "n": 30, "region": "AMERICAS", "field": "MOTORSPORT",
        "topic": FIELD_TOPICS["MOTORSPORT"],
        "place": "Las Vegas", "place_bar": "Las Vegas",
        "headline": "Verstappen wins the GP",
        "body": "", "what": "Verstappen wins the GP",
        "sources": "F1",
        "tag": "CONFIRMED", "tag_extra": "",
        "lon": -115.14, "lat": 36.17,
        "picture": None, "label": None,
    },
    {
        "n": 31, "region": "AMERICAS", "field": "TECH & SPEECH",
        "topic": FIELD_TOPICS["TECH & SPEECH"],
        "place": "Bogotá", "place_bar": "Bogotá",
        "headline": "govt asks X to suspend Petro",
        "body": "", "what": "govt asks X to suspend Petro",
        "sources": "MinTIC",
        "tag": "CONFIRMED", "tag_extra": "",
        "lon": -74.07, "lat": 4.71,
        "picture": None, "label": None,
    },
    {
        "n": 32, "region": "AMERICAS", "field": "WEATHER",
        "topic": FIELD_TOPICS["WEATHER"],
        "place": "Brazil", "place_bar": "Brazil",
        "headline": "storm death toll rises to 5",
        "body": "", "what": "storm death toll rises to 5",
        "sources": "Civil Def.",
        "tag": "CONFIRMED", "tag_extra": "",
        "lon": -47.90, "lat": -15.80,
        "picture": None, "label": None,
    },
    {
        "n": 33, "region": "AMERICAS", "field": "EARTHQUAKE",
        "topic": FIELD_TOPICS["EARTHQUAKE"],
        "place": "Peru", "place_bar": "Peru",
        "headline": "M5.1 quake near Cerro de Pasco",
        "body": "", "what": "M5.1 quake near Cerro de Pasco",
        "sources": "IGP",
        "tag": "CONFIRMED", "tag_extra": "",
        "lon": -76.26, "lat": -10.68,
        "picture": None, "label": None,
    },
    {
        "n": 34, "region": "AMERICAS", "field": "HEALTH POLICY",
        "topic": FIELD_TOPICS["HEALTH POLICY"],
        "place": "US", "place_bar": "US",
        "headline": "senator-elect pitches ‘TrumpCare’",
        "body": "", "what": "senator-elect pitches ‘TrumpCare’",
        "sources": "NBC",
        "tag": "STATED", "tag_extra": "",
        "lon": -77.04, "lat": 38.90,
        "picture": None, "label": None,
    },
    {
        "n": 35, "region": "WORLD", "field": "CRYPTO",
        "topic": FIELD_TOPICS["CRYPTO"],
        "place": "Markets", "place_bar": "Markets",
        "headline": "Bitcoin back above $60k",
        "body": "", "what": "Bitcoin back above $60k",
        "sources": "FXStreet, Fool",
        "tag": "CONFIRMED", "tag_extra": "",
        "lon": None, "lat": None,
        "picture": None, "label": None,
    },
]

LEADS = STORIES[0:3]
CARDS = STORIES[3:13]
BRIEFS = STORIES[13:35]

N = len(STORIES)

# ------------------------------------------------------------- top of page
DECK = ("COP31 ends with no deal  ·  Russia fires 186 drones at Ukraine, "
        "11 dead near Kyiv  ·  Russian warship capsized at Benghazi")

BACKGROUND = ("US–Israel war with Iran since Feb 2026  ·  Russia’s war on "
              "Ukraine since 2022  ·  Gaza truce since Oct 2025  ·  "
              "Netanyahu: caretaker PM  ·  US midterms: 3 Nov")

# ------------------------------------------------------------ timeline (5.2)
# (time, qualifier, event) — qualifier "" when none.
TIMELINE = [
    ("00:00", "", "Khartoum drones"),
    ("~01:00", "", "Benghazi blasts"),
    ("04:00", "start", "Las Vegas GP"),
    ("05:47", "", "Merkury ablaze"),
    ("06:00", "", "COP31 plenary"),
    ("10:00", "", "HK polls close"),
    ("16:30", "kick-off", "Liverpool 4–0 Utd"),
    ("17:00", "start", "ATP Finals final"),
]

# ----------------------------------------------------------- date check (5.8)
# (lead, rest) pairs. Non-breaking spaces (\u00a0) keep "Sat 21" and
# "Mon 23" from splitting across lines. {N} is filled by date_check_lines.
DATE_CHECK = [
    ("", "All {N} stories happened, or were first reported, on Sun 22 Nov (UTC); "
         "leads chosen by lives lost and reach."),
    ("Left out, Sat 21:", " Peru M6.7 quake and its toll, ‘El Chapo Isidro’ arrest, Bahrain strike."),
    ("Mon 23:", " 49ers–Vikings (kick-off 01:20 UTC)."),
]


def date_check_lines(n=None):
    """Return DATE_CHECK with {N} filled in (default: the computed total)."""
    if n is None:
        n = N
    return [(lead, rest.format(N=n)) for lead, rest in DATE_CHECK]


# -------------------------------------------------------- footer legend (5.9)
CERTAINTY_DEFS = [
    ("CONFIRMED", "official source or 2+ outlets named"),
    ("STATED", "one party’s claim, not checked"),
    ("UNVERIFIED", "unconfirmed, or attacker unknown"),
]

# ----------------------------------------------------------------- helpers
def region_totals():
    """dict region -> count, in REGIONS order, computed from STORIES."""
    totals = {region: 0 for region in REGIONS}
    for story in STORIES:
        totals[story["region"]] += 1
    return totals


def topic_totals():
    """dict topic -> count, computed from STORIES (not shown on the page)."""
    totals = {}
    for story in STORIES:
        totals[story["topic"]] = totals.get(story["topic"], 0) + 1
    return totals


def story_by_number(n):
    """Return the story dict with number n (1-35), or None."""
    for story in STORIES:
        if story["n"] == n:
            return story
    return None
