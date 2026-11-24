#!/usr/bin/env python3
"""news-image-20261123 front-page-dense entry: draws the whole 1024x1024 page."""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
MUTE = (90, 86, 76)
RED = (176, 30, 30)
DARKRED = (140, 20, 20)
BLUE = (29, 78, 137)
GREEN = (46, 107, 52)
GOLD = (138, 90, 0)
PURPLE = (122, 59, 143)
GREY = (85, 85, 85)
LINE = (200, 192, 175)
CARD_BG = (255, 255, 255)
SEA = (203, 224, 238)
LAND = (232, 222, 196)
LAND_EDGE = (170, 158, 130)

FB = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
FS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FSB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, f, max_w, fill=INK, lh=None, max_lines=None):
    lines = wrap(d, text, f, max_w)
    if max_lines:
        lines = lines[:max_lines]
    if lh is None:
        lh = int(f.size * 1.22)
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


def center(d, cx, y, text, f, fill=INK):
    w = d.textlength(text, font=f)
    d.text((cx - w / 2, y), text, font=f, fill=fill)


# ---------------------------------------------------------------- scenes
def scene_rout(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 24, 30))
    # grid
    for gy in range(y + 14, y + h - 8, 16):
        d.line([x + 8, gy, x + w - 8, gy], fill=(52, 52, 64))
    pts = []
    n = 9
    vals = [0.18, 0.24, 0.22, 0.38, 0.34, 0.52, 0.48, 0.66, 0.82]
    for i, v in enumerate(vals):
        px = x + 14 + i * (w - 28) / (n - 1)
        py = y + 10 + v * (h - 26)
        pts.append((px, py))
    d.line(pts, fill=(230, 60, 60), width=4)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 90, 90))
    # big red arrow head at end
    ex, ey = pts[-1]
    d.polygon([(ex + 2, ey - 12), (ex + 16, ey + 2), (ex - 2, ey + 4)], fill=(230, 60, 60))
    f = font(FSB, 30)
    d.text((x + w - 96, y + 6), "-3.3%", font=f, fill=(255, 120, 110))
    f2 = font(FSB, 13)
    d.text((x + 12, y + h - 22), "KOSPI 4,708.54", font=f2, fill=(255, 255, 255))
    d.text((x + w - 118, y + h - 22), "SEOUL", font=f2, fill=(150, 150, 165))


def scene_guterres(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 58, 110))
    cx, cy, r = x + w // 2, y + h // 2 - 6, 44
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 180, 235))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=2)
    d.line([cx - 38, cy - 20, cx + 38, cy - 20], fill=(255, 255, 255), width=2)
    d.line([cx - 38, cy + 20, cx + 38, cy + 20], fill=(255, 255, 255), width=2)
    d.ellipse([cx - r + 12, cy - r + 14, cx + r - 12, cy + r - 14],
              outline=(255, 255, 255), width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=2)
    # podium
    d.polygon([(cx - 52, y + h), (cx - 40, y + h - 26), (cx + 40, y + h - 26),
               (cx + 52, y + h)], fill=(240, 240, 235))
    d.rectangle([cx - 40, y + h - 30, cx + 40, y + h - 26], fill=(176, 30, 30))
    # flags
    for fx, col in ((x + 16, (220, 60, 60)), (x + w - 22, (60, 180, 90))):
        d.line([fx, y + 12, fx, y + 44], fill=(255, 255, 255), width=2)
        d.polygon([(fx, y + 12), (fx + 14, y + 17), (fx, y + 22)], fill=col)
    f = font(FSB, 12)
    d.text((x + 10, y + h - 20), "BRIDGETOWN", font=f, fill=(190, 215, 245))


def scene_power(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(245, 240, 225))
    bx, bw = x + 16, 74
    by = y + h - 30
    h_us = int((h - 52) * 0.95)
    h_cn = int((h - 52) * 0.80)
    d.rectangle([bx, by - h_us, bx + bw, by], fill=BLUE)
    d.rectangle([bx + bw + 34, by - h_cn, bx + bw + 34 + bw, by], fill=RED)
    f = font(FSB, 20)
    d.text((bx + 12, by - h_us + 6), "78.9", font=f, fill=(255, 255, 255))
    d.text((bx + bw + 46, by - h_cn + 6), "73.6", font=f, fill=(255, 255, 255))
    f2 = font(FSB, 12)
    d.text((bx + 18, by + 6), "US", font=f2, fill=INK)
    d.text((bx + bw + 48, by + 6), "CHINA", font=f2, fill=INK)
    # gap arrow
    gx = bx + bw + 17
    d.line([gx, by - h_us + 8, gx, by - h_cn - 4], fill=GOLD, width=3)
    d.polygon([(gx - 5, by - h_cn - 4), (gx + 5, by - h_cn - 4), (gx, by - h_cn - 14)],
              fill=GOLD)
    f3 = font(FSB, 15)
    d.text((x + w - 74, y + 8), "GAP 5.3", font=f3, fill=GOLD)


# ------------------------------------------------------------- card icons
def icon(d, kind, x, y, s, col):
    if kind == "chart":
        pts = [(x, y + s * 0.8), (x + s * 0.3, y + s * 0.5), (x + s * 0.55, y + s * 0.65),
               (x + s, y + s * 0.15)]
        d.line(pts, fill=(255, 255, 255), width=3)
        d.polygon([(x + s - 6, y + s * 0.15 - 8), (x + s + 4, y + s * 0.15 + 2),
                   (x + s - 8, y + s * 0.15 + 6)], fill=(255, 255, 255))
    elif kind == "shield":
        d.polygon([(x + s / 2, y), (x + s, y + s * 0.25), (x + s, y + s * 0.6),
                   (x + s / 2, y + s), (x, y + s * 0.6), (x, y + s * 0.25)],
                  outline=(255, 255, 255), width=3)
        d.line([x + s * 0.3, y + s * 0.5, x + s * 0.45, y + s * 0.65, x + s * 0.75, y + s * 0.3],
               fill=(255, 255, 255), width=3)
    elif kind == "flag":
        d.line([x + s * 0.2, y + 2, x + s * 0.2, y + s], fill=(255, 255, 255), width=3)
        d.polygon([(x + s * 0.2, y + 2), (x + s, y + s * 0.2), (x + s * 0.2, y + s * 0.38)],
                  fill=(255, 255, 255))
    elif kind == "ball":
        d.ellipse([x, y, x + s, y + s], outline=(255, 255, 255), width=3)
        d.line([x + s / 2, y, x + s / 2, y + s], fill=(255, 255, 255), width=2)
        d.arc([x - s * 0.4, y + s * 0.2, x + s * 0.4, y + s * 0.8], 300, 60,
              fill=(255, 255, 255), width=2)
        d.arc([x + s * 0.6, y + s * 0.2, x + s * 1.4, y + s * 0.8], 120, 240,
              fill=(255, 255, 255), width=2)
    elif kind == "star":
        cx, cy = x + s / 2, y + s / 2
        pts = []
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            r = s / 2 if i % 2 == 0 else s / 5
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
        d.polygon(pts, fill=(255, 255, 255))
    elif kind == "scale":
        d.line([x + s / 2, y + 2, x + s / 2, y + s - 4], fill=(255, 255, 255), width=3)
        d.line([x + 2, y + 6, x + s - 2, y + 6], fill=(255, 255, 255), width=3)
        d.polygon([(x, y + 6), (x + s * 0.28, y + 6), (x + s * 0.14, y + s * 0.55)],
                  outline=(255, 255, 255))
        d.polygon([(x + s * 0.72, y + 6), (x + s, y + 6), (x + s * 0.86, y + s * 0.55)],
                  outline=(255, 255, 255))
        d.rectangle([x + s * 0.3, y + s - 4, x + s * 0.7, y + s], fill=(255, 255, 255))
    elif kind == "chip":
        d.rectangle([x + 2, y + s * 0.25, x + s - 2, y + s * 0.75], outline=(255, 255, 255), width=3)
        for dx in (x + s * 0.2, x + s * 0.45, x + s * 0.7):
            d.line([dx, y + s * 0.25, dx, y + s * 0.1], fill=(255, 255, 255), width=2)
            d.line([dx, y + s * 0.75, dx, y + s * 0.9], fill=(255, 255, 255), width=2)
    elif kind == "rocket":
        d.polygon([(x + s * 0.5, y), (x + s * 0.8, y + s * 0.45), (x + s * 0.5, y + s * 0.7),
                   (x + s * 0.2, y + s * 0.45)], fill=(255, 255, 255))
        d.ellipse([x + s * 0.38, y + s * 0.3, x + s * 0.62, y + s * 0.52], fill=col)
        d.polygon([(x + s * 0.35, y + s * 0.7), (x + s * 0.5, y + s), (x + s * 0.65, y + s * 0.7)],
                  fill=(255, 200, 60))
    elif kind == "flame":
        d.polygon([(x + s * 0.5, y), (x + s * 0.85, y + s * 0.4), (x + s * 0.7, y + s * 0.7),
                   (x + s * 0.5, y + s), (x + s * 0.3, y + s * 0.7), (x + s * 0.15, y + s * 0.4)],
                  fill=(255, 255, 255))
    else:  # globe
        d.ellipse([x, y, x + s, y + s], outline=(255, 255, 255), width=3)
        d.ellipse([x + s * 0.25, y, x + s * 0.75, y + s], outline=(255, 255, 255), width=2)
        d.line([x, y + s / 2, x + s, y + s / 2], fill=(255, 255, 255), width=2)


# ------------------------------------------------------------------- map
NA = [(-168, 66), (-150, 70), (-135, 69), (-125, 71), (-115, 68), (-105, 68),
      (-95, 69), (-85, 66), (-80, 70), (-75, 62), (-65, 60), (-55, 52),
      (-60, 47), (-65, 44), (-70, 42), (-74, 39), (-76, 35), (-80, 32),
      (-81, 26), (-84, 30), (-90, 21), (-95, 19), (-97, 16), (-92, 15),
      (-86, 13), (-83, 9), (-80, 8), (-85, 11), (-90, 14), (-95, 16),
      (-100, 18), (-105, 20), (-110, 23), (-114, 28), (-117, 33), (-122, 37),
      (-124, 42), (-124, 48), (-130, 55), (-140, 60), (-150, 59), (-158, 58),
      (-162, 55), (-166, 60)]
GL = [(-55, 60), (-45, 60), (-40, 65), (-32, 68), (-25, 70), (-22, 73),
      (-30, 76), (-45, 76), (-55, 74), (-58, 70), (-60, 65)]
SA = [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
      (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-71, -50), (-66, -55),
      (-68, -52), (-65, -45), (-62, -40), (-57, -38), (-52, -33), (-48, -28),
      (-41, -23), (-39, -17), (-35, -9), (-35, -6), (-40, -3), (-44, -2),
      (-50, 0), (-52, 4), (-55, 6), (-60, 8), (-65, 10), (-70, 11), (-75, 10)]
AF = [(-6, 35), (0, 36), (10, 37), (11, 34), (15, 32), (20, 32), (25, 32),
      (30, 31), (32, 31), (34, 28), (37, 22), (39, 20), (41, 18), (43, 12),
      (46, 11), (51, 11), (48, 5), (44, 0), (41, -3), (40, -10), (38, -15),
      (35, -20), (33, -25), (29, -30), (26, -33), (20, -35), (17, -32),
      (15, -27), (13, -20), (12, -15), (13, -10), (12, -5), (9, -1), (9, 4),
      (4, 6), (-3, 5), (-8, 4), (-12, 8), (-15, 11), (-17, 15), (-17, 20),
      (-16, 25), (-13, 28), (-10, 31)]
EUAS = [(-10, 36), (-9, 43), (-2, 48), (-4, 49), (0, 50), (2, 52), (5, 53),
        (8, 57), (10, 58), (6, 58), (5, 60), (6, 62), (10, 64), (14, 67),
        (18, 69), (22, 70), (28, 71), (32, 70), (38, 68), (44, 68), (50, 69),
        (56, 69), (62, 69), (68, 72), (74, 72), (80, 73), (88, 74), (95, 76),
        (103, 77), (110, 74), (118, 73), (126, 72), (134, 72), (142, 72),
        (150, 70), (158, 69), (166, 68), (173, 66), (178, 65), (173, 62),
        (169, 60), (163, 60), (160, 56), (158, 52), (156, 51), (150, 59),
        (144, 59), (142, 54), (141, 50), (140, 45), (138, 43), (135, 43),
        (131, 42), (128, 39), (126, 38), (122, 38), (121, 35), (120, 32),
        (122, 28), (119, 25), (115, 23), (110, 21), (109, 18), (107, 15),
        (105, 10), (103, 7), (101, 6), (99, 8), (98, 10), (97, 14), (94, 17),
        (92, 21), (90, 22), (88, 22), (86, 20), (83, 18), (80, 15), (78, 10),
        (76, 9), (75, 12), (73, 17), (71, 21), (69, 22), (67, 24), (65, 25),
        (62, 25), (59, 25), (57, 26), (55, 27), (52, 26), (51, 28), (50, 29),
        (49, 30), (48, 30), (50, 27), (52, 26), (54, 24), (57, 22), (59, 22),
        (56, 26), (54, 26), (52, 28), (50, 29), (48, 29), (47, 30), (44, 29),
        (42, 29), (40, 31), (38, 31), (36, 36), (33, 36), (30, 36), (27, 37),
        (26, 38), (23, 36), (22, 37), (20, 39), (19, 42), (15, 44), (12, 44),
        (10, 44), (8, 44), (6, 43), (3, 42), (0, 40), (-2, 37), (-6, 36),
        (-9, 37)]
AU = [(113, -22), (114, -28), (115, -33), (118, -35), (124, -33), (129, -32),
      (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
      (153, -32), (153, -27), (150, -23), (147, -19), (144, -15), (142, -11),
      (140, -17), (137, -12), (135, -15), (132, -12), (130, -13), (127, -14),
      (124, -16), (121, -19), (117, -20)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51), (-2, 50)]
JP = [(130, 31), (132, 33), (134, 34), (137, 35), (139, 37), (140, 39),
      (141, 41), (142, 44), (144, 44), (141, 42), (140, 38), (139, 36),
      (136, 34), (133, 34), (131, 32)]


def draw_map(d, x0, y0, w, h, pins):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=SEA)
    lon0, lon1, lat0, lat1 = -168, 192, 75, -56

    def proj(lon, lat):
        px = x0 + (lon - lon0) / (lon1 - lon0) * w
        py = y0 + (lat0 - lat) / (lat0 - lat1) * h
        return (px, py)

    for poly in (NA, GL, SA, AF, EUAS, AU, UK, JP):
        d.polygon([proj(lo, la) for lo, la in poly], fill=LAND, outline=LAND_EDGE)
    for lo, la in ((95, 5), (105, -2), (112, -7), (120, -9), (130, -3), (138, -5)):
        px, py = proj(lo, la)
        d.ellipse([px - 3, py - 2, px + 3, py + 2], fill=LAND, outline=LAND_EDGE)
    for num, lon, lat in pins:
        px, py = proj(lon, lat)
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(255, 255, 255), width=1)
        f = font(FSB, 9)
        tw = d.textlength(str(num), font=f)
        d.text((px - tw / 2, py - 6), str(num), font=f, fill=(255, 255, 255))

# ------------------------------------------------------------- page data
NUMBERS = [
    ("-3.3%", "KOSPI rout, Seoul"),
    ("5.3", "US-China power gap"),
    ("11,762", "Ebola cases, DRC"),
    ("10T won", "Seoul rescue fund"),
    ("2%", "billionaire tax plan"),
    ("$450M", "Skubal Mets deal"),
    ("165", "Russian missiles / week"),
    ("12,000", "cleared, Manchester"),
    ("264 kg", "explosives, Lebanon"),
    ("$107.3B", "Anthropic IPO"),
]

REGIONS = [
    ("AMERICAS", 8, BLUE), ("ASIA-PACIFIC", 7, RED), ("MIDDLE EAST", 6, GOLD),
    ("EUROPE", 5, GREEN), ("AFRICA", 3, PURPLE), ("WORLD", 2, GREY),
]

UTC = [
    ("~06:30", "Kospi closes -3.3%"),
    ("~13:00", "Guterres urges AI rules"),
    ("~14:30", "Asia Power Index out"),
    ("~15:00", "Zelenskyy: 165 missiles"),
    ("~19:00", "COP31 fallout: fury"),
    ("21:00", "Anthropic debut $97.17"),
]

HEROES = [
    ("ASIA-PACIFIC · MARKETS", "AI ROUT HITS ASIA",
     "Kospi -3.3% to 4,708.54, shedding 161 pts; intraday -5.8%. Samsung "
     "-3.1%, SK Hynix -2.5% as the AI sell-off spreads from Wall Street.",
     "KRX, wires · REPORTED", scene_rout),
    ("WORLD · UNITED NATIONS", "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 "
     "delegates back a risk framework — a blueprint, not a treaty.",
     "UN, wires · REPORTED", scene_guterres),
    ("ASIA-PACIFIC · POWER", "US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 — gap 5.3, narrowest since "
     "2018. US diplomatic influence -6 to 76.7; India 3rd at 40.5.",
     "Lowy Institute · REPORTED", scene_power),
]

CARDS = [
    ("US · TRADE", "Bessent demands Nvidia answers",
     "Treasury chief wants to know of violations; China in focus.",
     "Treasury · REPORTED", "scale", BLUE),
    ("US · CYBER", "FBI probes hack of police database",
     "NCIC system used by police nationwide under investigation.",
     "FBI, wires · REPORTED", "shield", BLUE),
    ("US · IRAN", "Trump: Iran strikes may resume in New Year",
     "President says US strikes on Iran could resume in January.",
     "White House · REPORTED", "flag", RED),
    ("US · SPORT", "Skubal signs $450M Mets deal",
     "Two-time Cy Young winner; largest ever for a pitcher.",
     "MLB, wires · REPORTED", "ball", GREEN),
    ("US · SPORT", "Tom Jackson dies at 75",
     "Broncos linebacker turned ESPN voice; tributes pour in.",
     "ESPN · REPORTED", "star", GREEN),
    ("US · TECH", "10 states sue SpaceX over AI safety claims",
     "States challenge the firm's AI safety claims in court.",
     "State AGs · REPORTED", "scale", PURPLE),
    ("US · TECH", "Anthropic IPO: $107.3B, largest ever",
     "Claude maker raised at $83 a share on 19 Nov; debut close $97.17.",
     "NYSE, wires · REPORTED", "chip", PURPLE),
    ("EUROPE · SECURITY", "Poland: 3 Russian missiles crossed airspace",
     "Kyiv says three Kh-101 cruise missiles entered Poland on Friday.",
     "Kyiv, Warsaw · CLAIM", "rocket", RED),
    ("EUROPE · WAR", "Zelenskyy: 165 Russian missiles in a week",
     "Kyiv says Moscow fired 165 missiles in seven days as US delays Patriots.",
     "Kyiv · REPORTED", "flame", RED),
    ("WORLD · CLIMATE", "COP31: the day after",
     "Sunday's collapse — 194 nations reject the Antalya Pact — draws fury.",
     "UNFCCC, wires · REPORTED", "globe", GREEN),
]

ALSO = [
    (14, "US futures jump 3% in holiday week"),
    (15, "Intel: Russian nuclear satellite may launch next month · CLAIM"),
    (16, "Paris: 100+ back 2% billionaire tax"),
    (17, "Manchester: 12,000 cleared after substance scare"),
    (18, "Benghazi: UN demands probe of port attacks · CLAIM"),
    (19, "Israel unity talks resume after Sunday stall"),
    (20, "Gaza: two killed in Israeli strike"),
    (21, "West Bank settler attacks hit villages"),
    (22, "Iran war: no deal in sight"),
    (23, "Lebanon seizes 264 kg of explosives"),
    (24, "Bahrain: Iranian strike hits plant, 2 hurt"),
    (25, "Sudan air defences down drones over Khartoum · CLAIM"),
    (26, "DRC: fighting traps Ebola teams"),
    (27, "Bangladesh: Hasina jailed if she returns"),
    (28, "Seoul minister quits over AI exam chaos"),
    (29, "SK Telecom -7.3% as Anthropic hype cools"),
    (30, "China eases margin rules to calm rout"),
    (31, "Seoul readies 10T-won stabilisation fund"),
]

PINS = [
    (1, 127, 37.5), (2, -59.6, 13.1), (3, 116.4, 39.9), (4, -82, 36.5),
    (10, -74, 40.7), (11, 21, 52.2), (12, 33, 49), (16, 2.35, 48.85),
    (13, 28, 38), (20, 36, 30), (26, 15.3, -4.3),
]

EXCLUDED = [
    ("Democrats reach 258 seats", "22 Nov"),
    ("Sparta II fire", "22 Nov"),
    ("El Chapo Isidro captured", "22 Nov"),
    ("EU-Indonesia pact signed", "21 Nov"),
    ("Nigeria boat disaster", "21 Nov"),
    ("ICJ Myanmar ruling", "19 Nov"),
]

NOT_YET = [
    "Dymer search: 14 missing",
    "4 House races uncalled",
    "COP32 venue not set",
    "WHO evacuating trapped Ebola staff",
]


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 14
    cw = W - 2 * mx

    # masthead
    d.rectangle([0, 0, W, 74], fill=(17, 17, 17))
    center(d, W // 2, 8, "THE WORLD TODAY", font(FB, 44), fill=(247, 243, 234))
    center(d, W // 2, 56, "MONDAY, 23 NOVEMBER 2026  ·  THE DAY IN ONE IMAGE",
           font(FSB, 13), fill=(210, 200, 175))
    # kicker
    center(d, W // 2, 80, "AI rout sinks Seoul  ·  Guterres calls for AI rules  ·  "
           "America's lead over China at a record low",
           font(FSB, 13), fill=INK)
    d.line([mx, 98, W - mx, 98], fill=INK, width=2)

    # number strip
    y = 104
    d.text((mx, y), "THE DAY IN NUMBERS", font=font(FSB, 11), fill=RED)
    y += 16
    bw = cw / 10
    for i, (num, lab) in enumerate(NUMBERS):
        x = mx + i * bw
        d.rectangle([x + 1, y, x + bw - 1, y + 40], fill=CARD_BG, outline=LINE)
        f = font(FSB, 17 if len(num) <= 7 else 15)
        center(d, x + bw / 2, y + 3, num, f, fill=RED if i in (0, 1, 5, 9) else INK)
        text_block(d, x + 4, y + 24, lab, font(FS, 8), bw - 8, fill=MUTE,
                   lh=9, max_lines=2)
    y += 46

    # region bar
    d.text((mx, y + 2), "REGIONS", font=font(FSB, 11), fill=RED)
    x = mx + 78
    for name, n, col in REGIONS:
        label = "%s %d" % (name, n)
        f = font(FSB, 11)
        tw = d.textlength(label, font=f) + 16
        d.rounded_rectangle([x, y, x + tw, y + 18], radius=9, fill=col)
        d.text((x + 8, y + 3), label, font=f, fill=(255, 255, 255))
        x += tw + 6
    d.text((x + 4, y + 3), "31 stories", font=font(FSB, 11), fill=INK)
    y += 26

    # UTC strip
    d.text((mx, y + 2), "THE DAY IN UTC", font=font(FSB, 11), fill=RED)
    x = mx + 108
    uw = (W - mx - x) / 6
    for t, txt in UTC:
        d.text((x, y), t, font=font(FSB, 10), fill=BLUE)
        text_block(d, x, y + 12, txt, font(FS, 9), uw - 8, fill=INK, lh=10,
                   max_lines=2)
        x += uw
    y += 34
    d.line([mx, y, W - mx, y], fill=INK, width=2)

    # heroes
    y += 8
    hw = (cw - 16) / 3
    for i, (kick, head, body, src, scene) in enumerate(HEROES):
        x = mx + i * (hw + 8)
        scene(d, x, y, hw, 112)
        yy = y + 118
        d.text((x, yy), kick, font=font(FSB, 10), fill=RED)
        yy += 13
        yy = text_block(d, x, yy, head, font(FB, 17), hw, fill=INK, lh=19,
                        max_lines=2)
        yy = text_block(d, x, yy + 2, body, font(FS, 11), hw, fill=INK, lh=13,
                        max_lines=3)
        d.text((x, yy + 3), src, font=font(FSB, 8), fill=MUTE)
    y += 236

    # cards, 2 rows x 5
    cw5 = (cw - 4 * 8) / 5
    for r in range(2):
        for c in range(5):
            i = r * 5 + c
            kick, head, body, src, ic, col = CARDS[i]
            x = mx + c * (cw5 + 8)
            yy = y + r * 116
            d.rectangle([x, yy, x + cw5, yy + 110], fill=CARD_BG, outline=LINE)
            d.rectangle([x, yy, x + cw5, yy + 30], fill=col)
            icon(d, ic, x + 8, yy + 5, 20, col)
            d.text((x + 34, yy + 9), "%d" % (i + 4), font=font(FSB, 13),
                   fill=(255, 255, 255))
            d.text((x + 6, yy + 34), kick, font=font(FSB, 8), fill=RED)
            ty = text_block(d, x + 6, yy + 46, head, font(FSB, 11), cw5 - 12,
                            fill=INK, lh=12, max_lines=2)
            ty = text_block(d, x + 6, ty + 1, body, font(FS, 9), cw5 - 12,
                            fill=INK, lh=11, max_lines=2)
            d.text((x + 6, yy + 97), src, font=font(FSB, 7), fill=MUTE)
    y += 236

    # map + ALSO
    d.line([mx, y, W - mx, y], fill=INK, width=2)
    y += 6
    d.text((mx, y), "WHERE IT HAPPENED", font=font(FSB, 11), fill=RED)
    d.text((mx + 490, y), "ALSO ON MONDAY", font=font(FSB, 11), fill=RED)
    y += 16
    draw_map(d, mx, y, 470, 168, PINS)
    d.text((mx, y + 172), "Pins match story numbers. 1 Seoul · 2 Bridgetown · "
           "3 Beijing · 10 New York · 13 Antalya · 26 Kinshasa",
           font=font(FS, 8), fill=MUTE)
    ax = mx + 490
    aw = W - mx - ax
    colw = aw / 2
    for j, (num, txt) in enumerate(ALSO):
        col = j // 9
        row = j % 9
        x = ax + col * colw
        yy = y + row * 19
        d.text((x, yy), "%d." % num, font=font(FSB, 9), fill=RED)
        lines = wrap(d, txt, font(FS, 9), colw - 24)
        d.text((x + 20, yy), lines[0], font=font(FS, 9), fill=INK)
        if len(lines) > 1:
            d.text((x + 20, yy + 10), lines[1], font=font(FS, 9), fill=INK)
    y += 196

    # DATE CHECK
    d.rectangle([mx, y, W - mx, y + 66], outline=RED, width=2)
    d.text((mx + 8, y + 5), "DATE CHECK — LEFT OUT: NOT 23 NOVEMBER",
           font=font(FSB, 11), fill=RED)
    d.text((mx + 500, y + 5), "NOT YET", font=font(FSB, 11), fill=RED)
    yy = y + 22
    for r in range(3):
        for c in range(2):
            i = r * 2 + c
            txt, dt = EXCLUDED[i]
            x = mx + 8 + c * 245
            d.text((x, yy + r * 13), "x %s — %s" % (txt, dt), font=font(FS, 10),
                   fill=INK)
    for r in range(2):
        for c in range(2):
            i = r * 2 + c
            x = mx + 500 + c * 245
            d.text((x, yy + r * 13), "… %s" % NOT_YET[i], font=font(FS, 10),
                   fill=INK)
    y += 72

    # footer
    d.line([mx, y, W - mx, y], fill=LINE, width=1)
    y += 5
    d.text((mx, y), "Sources: KRX · Lowy Institute · UN · NYSE · MLB · ESPN · "
           "FBI · Treasury · Kyiv · Warsaw · UNFCCC · wires (AP, Reuters, AFP).",
           font=font(FS, 9), fill=MUTE)
    y += 12
    d.text((mx, y), "Chips: REPORTED = confirmed by a named source · CLAIM = one "
           "side alleges, not verified · ONGOING = still developing.",
           font=font(FS, 9), fill=MUTE)
    y += 12
    d.text((mx, y), "Scenes are drawn illustrations, not photographs. "
           "Compiled from wires read 23 Nov 2026. ~ = approximate time.",
           font=font(FS, 9), fill=MUTE)
    return img


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    im = build()
    im.save(out, optimize=True)
    print(out, im.size)
