#!/usr/bin/env python3
"""Generate a 1024x1024 newspaper front-page image summing up 17 Nov 2026 world news.
Deterministic: no randomness, no timestamps, no network."""
from PIL import Image, ImageDraw, ImageFont
import textwrap, os

W = H = 1024
BG = (250, 247, 238)
INK = (18, 18, 18)
RED = (178, 24, 24)
BLUE = (20, 55, 110)
GREY = (90, 90, 90)
LIGHT = (232, 226, 210)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def F(path, size): return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

def text(x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)
    return d.textbbox((x, y), s, font=font, anchor=anchor)[3]

def wrap(s, font, width):
    # pixel-width wrap
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w_
    if cur: lines.append(cur)
    return lines

def block(x, y, w_, headline, body, hsize=20, bsize=14, hcolor=INK, blines_max=4):
    yy = y
    for ln in wrap(headline, F(SANS_B, hsize), w_):
        text(x, yy, ln, F(SANS_B, hsize), hcolor); yy += hsize + 3
    for ln in wrap(body, F(SANS, bsize), w_)[:blines_max]:
        text(x, yy, ln, F(SANS, bsize), (40,40,40)); yy += bsize + 3
    return yy

def hline(x0, x1, y, color=INK, width=2):
    d.line([(x0, y), (x1, y)], fill=color, width=width)

# Masthead
d.rectangle([0, 0, W, 92], fill=INK)
text(W//2, 10, "THE  WORLD  TODAY", F(SERIF_B, 46), (255,255,255), "ma")
text(W//2, 62, "Tuesday 17 November 2026  •  15 stories  •  6 continents  •  One page", F(SANS_B, 16), (255, 210, 120), "ma")
hline(24, W-24, 104, RED, 4)

# Lead story
y = 114
text(24, y, "1  GULF WAR FLARES AGAIN", F(SANS_B, 15), RED); y += 22
y = block(24, y, 640, "US STRIKES IRAN'S QESHM ISLAND; TANKERS BURN IN HORMUZ",
          "US fighter jets hit a Revolutionary Guards missile site on Qeshm Island after Iranian drones struck a US radar at Bahrain's Sheikh Isa Air Base. In the strait, the LPG tanker Tara Gas was hit again off Oman — 24 crew evacuated, one missing — and an ADNOC vessel was attacked with 11 hurt, even as Iran talked mediation with Qatar and Oman.",
          hsize=30, bsize=15, blines_max=5)
hline(24, 664, y+4, GREY, 1)

# Right rail top
rx = 688
text(rx, 114, "2  APEC • SHENZHEN", F(SANS_B, 15), RED)
block(rx, 136, 312, "TRUMP, XI & PUTIN CONVERGE ON SHENZHEN",
      "Leaders gathered in China's tech hub as the APEC CEO Summit opened. Xi urged free and open trade, Putin attacked Western sanctions, and Trump flew in for Thursday's first-ever three-way summit on Iran, Ukraine, trade, AI and nuclear arms.",
      hsize=19, bsize=13, blines_max=7)
hline(rx, W-24, 330, GREY, 1)
text(rx, 340, "3  US POLITICS", F(SANS_B, 15), RED)
block(rx, 362, 312, "ALASKA CALLED: PELTOLA WINS, SENATE SETTLED 56–44",
      "AP called the last Senate race Tuesday evening for Democrat Mary Peltola — the first Alaska Native elected to the US Senate. The House stood at 257–171 with seven races still uncalled.",
      hsize=17, bsize=13, blines_max=5)

# Map band
my = 352
d.rectangle([24, my, 664, 540], fill=(214, 228, 238), outline=BLUE, width=2)
text(36, my+8, "THE DAY ON THE MAP", F(SANS_B, 16), BLUE)
# simplified continents (schematic polygons)
land = (168, 188, 150)
continents = [
    [(60,420),(150,395),(210,410),(205,450),(160,490),(120,470),(70,460)],          # N America-ish (lower left in box coords offset)
    [(185,470),(220,465),(225,505),(200,535),(180,505)],
    [(330,400),(390,390),(420,415),(400,450),(350,445),(325,425)],                  # Europe
    [(340,450),(410,445),(430,490),(395,530),(355,505)],                            # Africa
    [(425,400),(540,390),(610,420),(590,470),(500,455),(440,440)],                  # Asia
    [(545,475),(600,470),(615,500),(575,520),(550,500)],                            # SE Asia / Oceania-ish
]
# Map box is 24..664 x 352..540; polygons above are absolute-ish, clip mentally: shift y -0
for poly in continents:
    d.polygon(poly, fill=land, outline=(120,140,110))
pins = [
    (470, 425, "1", "Hormuz / Qeshm"),
    (545, 415, "2", "Shenzhen • APEC"),
    (95, 415, "3", "Alaska"),
    (385, 410, "4", "Crimea Bridge"),
    (445, 435, "5", "Gaza"),
    (575, 445, "6", "Tokyo"),
]
for px, py, num, label in pins:
    d.ellipse([px-10, py-10, px+10, py+10], fill=RED, outline=(255,255,255), width=2)
    text(px, py-1, num, F(SANS_B, 12), (255,255,255), "ma")
text(36, 512, "1 Gulf  •  2 APEC Shenzhen  •  3 Alaska  •  4 Crimea  •  5 Gaza  •  6 Tokyo", F(SANS_B, 12), BLUE)

# Middle grid, 3 columns below map/lead
gy = 552
cols = [(24, 320), (352, 320), (680, 320)]
stories = [
    ("4  UKRAINE", "KERCH BRIDGE STRUCK AND CLOSED", "Ukraine hit the Crimean Bridge again, badly damaging the span; Russia answered by striking bridges in Kyiv. A Russian strike on Zaporizhzhia killed 40."),
    ("5  GAZA", "WEST TO ISRAEL: OPEN THE CROSSINGS", "Britain, Australia, Canada and Italy called Gaza's aid situation catastrophic and urged rapid access, as winter rains flooded shelters. London sanctioned settlement firms."),
    ("6  ASIA-PACIFIC", "JAPAN SCRAMBLES JETS OVER RUSSIAN AIRCRAFT", "Tokyo protested an airspace violation by two suspected Russian aircraft. India and Japan held 2+2 talks; Modi joined ASEAN-India leaders in Manila."),
    ("7  TECH", "US TIGHTENS AI CHIP RULES ON CHINA", "Washington now requires licences for advanced AI chips and servers in overseas data centres, closing the remote-access route for Chinese firms. Nvidia earnings loom."),
    ("8  MARKETS", "WALL STREET FALLS AS AI STOCKS SLIDE", "US indexes closed lower under pressure from tech shares. Dubai Airports said passenger traffic fell 28% in nine months as the Gulf war hit travel."),
    ("9  YEMEN", "HOUTHIS ADVANCE; GOVERNMENT RETREATS", "Government forces quit the Red Sea coast to defend Aden as the Iran-backed Houthis advanced — a new threat to shipping already rattled by Hormuz."),
]
for i, (kicker, head, body) in enumerate(stories):
    cx, cw = cols[i % 3]
    cy = gy if i < 3 else gy + 150
    text(cx, cy, kicker, F(SANS_B, 13), RED)
    block(cx, cy+18, cw, head, body, hsize=16, bsize=12, blines_max=5)
    if i % 3 != 2:
        d.line([(cx+cw+14, cy), (cx+cw+14, cy+132)], fill=(200,195,180), width=1)
hline(24, W-24, gy+142, GREY, 1)
hline(24, W-24, gy+292, GREY, 1)

# Bottom briefs
by = gy + 302
text(24, by, "IN BRIEF — THE REST OF THE WORLD IN ONE LINE EACH", F(SANS_B, 15), BLUE)
briefs = [
    "IRELAND: Man charged over an attack that destroyed a US military plane parked at an Irish airport.",
    "HEALTH: The United States loses its measles elimination status after a year of uninterrupted spread.",
    "FRANCE: Gérard Depardieu drops his appeal and admits sexual assault charges before a Paris court.",
    "CLIMATE: COP31 draft deal in Antalya seeks a faster fossil-fuel phase-out and $120bn a year for adaptation.",
    "WASHINGTON: FAA pauses router installs tied to last week's nationwide ground stop; the cause is still unclear.",
    "SPORT: India edge Pakistan by one wicket on the last ball to win the U19 Asia Cup; Germany rout Netherlands 5–0.",
]
yy = by + 24
for b in briefs:
    text(24, yy, "•  " + b, F(SANS, 12.5 if False else 12), (35,35,35))
    yy += 17

d.rectangle([0, H-28, W, H], fill=INK)
text(W//2, H-22, "All the day's news, in one image — Tuesday 17 November 2026  •  Sources: Reuters, AP, AFP, Al Jazeera, NPR, PAHO", F(SANS, 11), (255,255,255), "ma")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "news.png")
img.save(out, optimize=True)
print(out, os.path.getsize(out))
