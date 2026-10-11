"""Démo v2 d'animation de démarrage, écran 128 x 64 monochrome (RadioMaster Pocket).

Scénario GaboLabs : GABOLABS, le PNJ arrive, GABOLABS s'efface, le drone arrive, largue sa bombe
et continue sa route, explosion, tête de mort, СЛАВА УКРАЇНІ en ukrainien.
"""

import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

L, H = 128, 64
SOL = 62
ICI = Path(__file__).parent  # tryzub_52_35.png doit être à côté
random.seed(7)


def sprite(dessin: str) -> list[tuple[int, int]]:
    return [(x, y) for y, l in enumerate(dessin.strip("\n").splitlines()) for x, c in enumerate(l) if c == "#"]


DRONE_A = sprite("""
####.......####
..#.........#..
..###########..
....#######....
.....#####.....
......#.#......
""")
DRONE_B = sprite("""
.##.........##.
..#.........#..
..###########..
....#######....
.....#####.....
......#.#......
""")
BOMBE = sprite("""
.#.
###
###
###
.#.
""")
PNJ_1 = sprite("""
..##..
..##..
.####.
#.##.#
..##..
..##..
.#..#.
.#..#.
#....#
""")
PNJ_2 = sprite("""
..##..
..##..
.####.
#.##.#
..##..
..##..
..##..
..#.#.
..#.#.
""")
PNJ_MORT = sprite("""
#.#.....##
.#######.#
#.#.....##
""")
TRYZUB = sprite("""
#......#......#
#......#......#
#.....###.....#
##....###....##
##....###....##
##....###....##
.##..#####..##.
.##.##.#.##.##.
..###..#..###..
..##########...
....#######....
......###......
......#.#......
......###......
""")
CRANE = sprite("""
....########....
..############..
.##############.
.##############.
###....##....###
###....##....###
###....##....###
.######..######.
..#####..#####..
...###.##.###...
...##########...
...#.#.##.#.#...
....########....
""")


CRANE_OUVERT = [(x, y + 1) if y >= 10 else (x, y) for x, y in CRANE]


def poser(d, pts, x, y, t=1):
    for px, py in pts:
        d.rectangle([x + px * t, y + py * t, x + px * t + t - 1, y + py * t + t - 1], fill=1)


def grand_texte(txt: str, largeur_max: int, hauteur_max: int) -> Image.Image:
    """Texte (cyrillique compris) en pixels purs, le plus grand possible dans la boîte donnée."""
    meilleur = None
    for taille in range(8, 60):
        police = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", taille)
        img = Image.new("1", (300, 80), 0)
        d = ImageDraw.Draw(img)
        d.fontmode = "1"
        d.text((0, 0), txt, font=police, fill=1)
        img = img.crop(img.getbbox())
        if img.width > largeur_max or img.height > hauteur_max:
            break
        meilleur = img
    return meilleur


def titre() -> Image.Image:
    return grand_texte("GABOLABS", 124, 30)


def devise() -> Image.Image:
    """СЛАВА УКРАЇНІ en pixels purs (police Windows avec cyrillique, rendu sans lissage)."""
    police = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 10)
    img = Image.new("1", (128, 14), 0)
    d = ImageDraw.Draw(img)
    d.fontmode = "1"
    d.text((0, 0), "СЛАВА УКРАЇНІ", font=police, fill=1)
    return img.crop(img.getbbox())


TITRE, DEVISE = titre(), devise()
SLAVA, UKRAINI = grand_texte("СЛАВА", 76, 16), grand_texte("УКРАЇНІ", 76, 16)
pts_titre = [(x, y) for y in range(TITRE.height) for x in range(TITRE.width) if TITRE.getpixel((x, y))]
X_T = (L - TITRE.width) // 2
Y_T = (SOL - 10 - TITRE.height) // 2
images: list[tuple[Image.Image, int]] = []


def scene(titre_pts=None, pnj=None, drone=None, bombe=None, decalage=0):
    img = Image.new("1", (L, H), 0)
    d = ImageDraw.Draw(img)
    for x, y in titre_pts or []:
        d.point((X_T + x, Y_T + y), fill=1)
    d.line([0, SOL + decalage, L - 1, SOL + decalage], fill=1)
    if pnj:
        poser(d, pnj[0], pnj[1], SOL - 9 + decalage)
    if drone:
        poser(d, drone[0], drone[1], drone[2])
    if bombe:
        poser(d, BOMBE, bombe[0], bombe[1])
    return img, d


# 1. GABOLABS s'écrit
for n in range(1, len(pts_titre) + 1, max(1, len(pts_titre) // 10)):
    images.append((scene(sorted(pts_titre)[:n])[0], 60))
images.append((scene(pts_titre)[0], 400))

# 2. le PNJ arrive en marchant depuis la droite
X_PNJ = 84
for i, x in enumerate(range(L, X_PNJ - 1, -4)):
    images.append((scene(pts_titre, ((PNJ_1, PNJ_2)[i % 2], x))[0], 90))
images.append((scene(pts_titre, (PNJ_2, X_PNJ))[0], 300))

# 3. GABOLABS se dissout pixel par pixel
restants = pts_titre[:]
random.shuffle(restants)
while restants:
    restants = restants[: int(len(restants) * 0.6)]
    images.append((scene(restants, (PNJ_2, X_PNJ))[0], 70))

# 4. le drone arrive, largue au-dessus du PNJ, continue sa route ; la bombe tombe
Y_DRONE = 12
X_LARGAGE = X_PNJ + 3 - 7  # centre du drone au-dessus du PNJ
bombe_y = None
for i, x in enumerate(range(-16, L + 2, 4)):
    helices = (DRONE_A, DRONE_B)[i % 2]
    if bombe_y is None and x >= X_LARGAGE:
        for k in range(8):  # arrêt au-dessus de la cible, léger flottement
            images.append((scene(None, (PNJ_2, X_PNJ), ((DRONE_A, DRONE_B)[k % 2], X_LARGAGE, Y_DRONE + (k // 2) % 2))[0], 70))
        x = X_LARGAGE
        bombe_y = Y_DRONE + 6
    elif bombe_y is not None:
        bombe_y += 3 + (bombe_y - Y_DRONE) // 8  # accélération
    if bombe_y is not None and bombe_y >= SOL - 12:
        break
    b = (X_PNJ + 2, bombe_y) if bombe_y is not None else None
    images.append((scene(None, (PNJ_2, X_PNJ), (helices, x, Y_DRONE), b)[0], 60))
x_drone = x

DEBUT_MORT = None
# 5. explosion avec tremblement, le drone s'éloigne
for k, r in enumerate((3, 7, 11, 15, 18, 14)):
    sec = (2, -2, 1, -1, 0, 0)[k]
    img, d = scene(None, None, ((DRONE_A, DRONE_B)[k % 2], x_drone + 4 * (k + 1), Y_DRONE), None, sec)
    cx, cy = X_PNJ + 3, SOL - 4 + sec
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=1)
    if r < 16:
        d.ellipse([cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2], fill=1)
    images.append((img, 80))
DEBUT_MORT = len(images) - 2
images.append((Image.new("1", (L, H), 0), 250))

# 6. tête de mort en grand (x4), centrée, puis dissolution comme GABOLABS
def grossir(pts):
    return [(px * 4 + dx, py * 4 + dy) for px, py in pts for dx in range(4) for dy in range(4)]


crane_pts = grossir(CRANE)
crane_ouvert = grossir(CRANE_OUVERT)
X_C, Y_C = (L - 64) // 2, 1


def ecran_crane(pts):
    img = Image.new("1", (L, H), 0)
    d = ImageDraw.Draw(img)
    for x, y in pts:
        d.point((X_C + x, Y_C + y), fill=1)
    return img


images.append((ecran_crane(crane_pts), 300))
for k in range(8):
    images.append((ecran_crane((crane_ouvert, crane_pts)[k % 2]), 130))
images.append((ecran_crane(crane_pts), 300))
restants = crane_pts[:]
random.shuffle(restants)
while restants:
    restants = restants[: int(len(restants) * 0.6)]
    images.append((ecran_crane(restants), 70))

# 7. СЛАВА УКРАЇНІ à gauche, le tryzub à droite
img = Image.new("1", (L, H), 0)
d = ImageDraw.Draw(img)
ZONE_TEXTE = 80
ecart = (SOL - 2 - SLAVA.height - UKRAINI.height) // 3
img.paste(1, ((ZONE_TEXTE - SLAVA.width) // 2, ecart), SLAVA)
img.paste(1, ((ZONE_TEXTE - UKRAINI.width) // 2, 2 * ecart + SLAVA.height), UKRAINI)
ARMOIRIES = Image.open(ICI / "tryzub_52_35.png").convert("1")  # armoiries officielles pixelisées
img.paste(1, (ZONE_TEXTE + (L - ZONE_TEXTE - ARMOIRIES.width) // 2, (SOL - ARMOIRIES.height) // 2), ARMOIRIES)
images.append((img, 2000))

FOND, ENCRE, ZOOM = (196, 206, 196), (24, 32, 24), 5
gif = []
for i, (img, duree) in enumerate(images):
    if DEBUT_MORT is not None and i >= DEBUT_MORT:
        img = img.copy()
        d = ImageDraw.Draw(img)
        d.line([0, SOL, L - 1, SOL], fill=1)
        poser(d, PNJ_MORT, X_PNJ - 2, SOL - 3)
    rgb = Image.new("RGB", (L, H), FOND)
    rgb.paste(ENCRE, mask=img)
    gif.append((rgb.resize((L * ZOOM, H * ZOOM), Image.Resampling.NEAREST), duree))
gif[0][0].save(ICI / "splash_demo6.gif", save_all=True, append_images=[g for g, _ in gif[1:]],
               duration=[d for _, d in gif], loop=0)
print(f"{len(images)} images, {sum(d for _, d in images) / 1000:.1f} s, devise {DEVISE.size}")
