"""Convertit l'animation GIF validée en en-tête C pour EdgeTX (écran 128 x 64 monochrome).

Usage : py -3 gif_vers_c.py animation_demarrage_v6.gif ../edgetx_src/radio/src/gui/128x64/gabolabs_splash.h
Format : par image, différence (XOR) avec la précédente, plages alternées inchangé/changé,
longueur sur 1 octet (< 128) ou 2 octets (bit 7 = suite), ordre ligne par ligne.
"""

import sys
from pathlib import Path

from PIL import Image, ImageSequence

L, H = 128, 64
gif = Image.open(sys.argv[1])
images, durees, donnees, decalages = [], [], [], []
precedente = [0] * (L * H)
for cadre in ImageSequence.Iterator(gif):
    rgb = cadre.convert("RGB").resize((L, H), Image.Resampling.NEAREST)
    bits = [1 if sum(rgb.getpixel((x, y))) < 300 else 0 for y in range(H) for x in range(L)]
    durees.append(max(1, round(cadre.info.get("duration", 100) / 10)))  # en pas de 10 ms
    decalages.append(len(donnees))
    # on ne code que les pixels qui changent (XOR avec l'image précédente), en plages alternées
    diff = [a ^ b for a, b in zip(bits, precedente)]
    etat, i = 0, 0
    while i < len(diff):
        n = 0
        while i < len(diff) and diff[i] == etat:
            n += 1
            i += 1
        # longueur sur 1 octet (< 128) ou 2 octets (bit de poids fort = suite)
        donnees += [n] if n < 128 else [0x80 | (n >> 8), n & 0xFF]
        etat ^= 1
    images.append(bits)
    precedente = bits

# contrôle : décompression identique à celle du firmware
ecran = [0] * (L * H)
for k, bits in enumerate(images):
    p, etat, pos = decalages[k], 0, 0
    while pos < L * H:
        n = donnees[p]
        p += 1
        if n & 0x80:
            n = ((n & 0x7F) << 8) | donnees[p]
            p += 1
        if etat:
            for j in range(pos, pos + n):
                ecran[j] ^= 1
        pos += n
        etat ^= 1
    assert ecran == bits, f"image {k} mal encodée"

lignes = [
    "// Généré par gif_vers_c.py, animation de démarrage GaboLabs (ne pas modifier à la main)",
    "#pragma once",
    f"#define GABOLABS_ANIM_FRAMES {len(images)}",
    "static const uint16_t gabolabs_anim_offsets[] = {"
    + ",".join(map(str, decalages))
    + "};",
    "static const uint8_t gabolabs_anim_durations[] = {"
    + ",".join(map(str, durees))
    + "};",
    "static const uint8_t gabolabs_anim_data[] = {",
]
for i in range(0, len(donnees), 32):
    lignes.append("  " + ",".join(map(str, donnees[i : i + 32])) + ",")
lignes.append("};")
assert max(decalages) < 65536
Path(sys.argv[2]).write_text("\n".join(lignes) + "\n", encoding="utf-8")
print(
    f"{len(images)} images, {sum(durees) / 100:.1f} s, {len(donnees)} octets compressés "
    f"(brut : {len(images) * L * H // 8})"
)
