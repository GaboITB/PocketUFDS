"""PocketUFDS installer: sets up a RadioMaster Pocket (EdgeTX 2.12) for Ukrainian Fight Drone Simulator.

Double-click the .exe: it finds the radio by itself, speaks the player's language, shows numbered
steps, and never closes before the player has read the result (same spirit as the Homicide Desk FR patch).

Non-interactive mode (tests):
  installer.py --sd E:/ --lang fr --anim yes --yes [--backup-dir DIR]
  installer.py --restore --sd E:/ --backup-dir DIR --yes

Safety rules:
  - refuses anything that is not a RadioMaster Pocket SD card on EdgeTX 2.12.x;
  - backs up the WHOLE SD card before touching it, and can restore it;
  - never overwrites an existing model (UFDS goes to the first free slot);
  - in radio.yml, changes ONLY: switch types, audio mute, voice language, inactivity alarm;
    the user's stick calibration is untouched; the EdgeTX checksum is recomputed.
Error and info codes in brackets ([E-VERSION]…) are identical in every language (support, tests).
"""

import argparse
import ctypes
import datetime
import os
import re
import shutil
import string
import sys
import zipfile
from pathlib import Path

VERSION_PACK = "1.0"


def dossier_data() -> Path:
    """Distributed layout: the 'data' folder next to the .exe (or next to this script)."""
    base = (
        Path(sys.executable).parent
        if getattr(sys, "frozen", False)
        else Path(__file__).resolve().parent
    )
    return Path(os.environ.get("POCKETUFDS_DATA", base / "data"))


PACK = dossier_data()
LANGUES = {  # code -> (dossier EdgeTX, ttsLanguage, pack de voix)
    "en": ("en", "en", PACK / "voix/en"),
    "uk": ("ua", "ua", PACK / "voix/ua"),
    "fr": ("fr", "fr", PACK / "voix/fr"),
}
TYPES_INTERS = {"SA": "2POS", "SB": "3POS", "SC": "3POS", "SD": "2POS", "SE": "TOGGLE"}

T = {
    "en": {
        "titre": "PocketUFDS {v}: RadioMaster Pocket for Ukrainian Fight Drone Simulator",
        "menu": "What do you want to do?\n  1. Install the pack on my radio\n  2. Restore my radio from a backup\nYour choice (1 or 2): ",
        "cherche": "Looking for the radio...",
        "absente": "No RadioMaster Pocket found.\n  1. Plug the radio into the PC with a USB-C data cable.\n  2. Turn it on and choose USB STORAGE on its screen.\n  3. Wait a few seconds, then press Enter to search again.",
        "plusieurs": "Several radios found. Type the number of yours: ",
        "trouvee": "RadioMaster Pocket found on {d} (EdgeTX {v}).",
        "anim_q": "Optional: animated GaboLabs boot screen, with soundtrack and LED light show.\nIt needs a custom EdgeTX firmware that you flash yourself afterwards (see the guide).\n  1. Yes, include it\n  2. No, keep the official firmware\nYour choice (1 or 2): ",
        "recap": "Ready to install: voices {l}, animated firmware {a}. A full backup of the SD card is made first.",
        "oui": "yes",
        "non": "no",
        "go": "Type Y then Enter to start (anything else cancels): ",
        "etape": "Step {n} of {t}: {x}",
        "e1": "backup of the whole SD card",
        "e2": "radio settings",
        "e3": "UFDS model",
        "e4": "voice pack",
        "e5": "firmware files",
        "sauve": "Backup: {p}",
        "modele_ok": "UFDS model added as {f} (position {n} in the model list).",
        "modele_la": "[I-MODEL-PRESENT] A UFDS model is already on the radio ({f}): kept as is.",
        "voix_ok": "{n} voice files installed.",
        "fw_ok": "Copied to FIRMWARE: {f}",
        "fini": "Done! Next steps:\n  1. Eject the radio in Windows (USB icon near the clock), unplug it.\n  2. If you chose the animated firmware: flash it (guide, section 3).\n  3. On the radio: long press MDL, select UFDS.\n  4. In the game: map the controls (guide, section 5).",
        "guide": "Guide: {g}",
        "annule": "Cancelled. Nothing was changed.",
        "rien": "Nothing was changed on the radio.",
        "e_version": "[E-VERSION] EdgeTX {v} found, version 2.12 is required.\nFlash EdgeTX 2.12 first, turn the radio on once, then run this installer again.",
        "e_board": "[E-BOARD] This SD card is not from a RadioMaster Pocket.",
        "e_cle": "[E-SETTINGS] Unexpected radio settings file ({c}).",
        "e_sauve": "[E-BACKUP] The backup is incomplete ({n}/{t} files).",
        "fin_touche": "Press Enter to close this window.",
        "fw_q": "The pack can prepare the official update to EdgeTX 2.12.4:\n  - full backup of the SD card,\n  - official EdgeTX SD card content,\n  - startup switch checks of your models rewritten in the 2.12 format (same positions),\n  - official EdgeTX 2.12.4 firmware copied to the radio.\nType Y then Enter to prepare it (any other answer cancels): ",
        "fw_etapes": "Official EdgeTX 2.12.4 copied to the radio: FIRMWARE/OFFICIAL-2.12.4.bin\nNow flash it (about one minute):\n  1. Eject the radio in Windows (USB icon near the clock), unplug it and turn it off.\n  2. The trims are the two mini joysticks on each side of the power button.\n     Push both toward the power button (toward the center) and hold them,\n     then, without releasing them, press and hold the power button until the screen turns on.\n     A black and white menu opens: the bootloader. Release the trims.\n  3. Turn the scroll wheel to select Write Firmware, then press the wheel.\n  4. Select OFFICIAL-2.12.4.bin, press the wheel,\n     then hold the wheel pressed until Writing... appears.\n  5. Wait for Writing complete, press the wheel, select Exit, press the wheel.\n  6. The radio starts with EdgeTX 2.12: let it start fully once.\n     If a warning shows on the screen, do what it asks (for example, switches up).\n  7. Plug the radio back in, choose USB STORAGE and run this installer again.",
        "alertes_ok": "Startup switch check rewritten in the EdgeTX 2.12 format (same positions): {n} model(s).",
        "sd_ok": "Official EdgeTX {v} SD card content installed ({n} files).",
        "patiente": "Copying, please wait. Do NOT unplug the radio.",
        "r_aucune": "[E-NOBACKUP] No backup found in {d}.",
        "r_liste": "Backups found (most recent first):",
        "r_choix": "Type the number of the backup to restore: ",
        "r_confirm": "The SD card of the radio will be replaced by this backup: {b}\nType Y then Enter to confirm: ",
        "r_ok": "Radio restored from {b}. Eject it, unplug it and turn it on.",
    },
    "uk": {
        "titre": "PocketUFDS {v}: RadioMaster Pocket для Ukrainian Fight Drone Simulator",
        "menu": "Що потрібно зробити?\n  1. Встановити пакет на апаратуру\n  2. Відновити апаратуру з резервної копії\nВаш вибір (1 або 2): ",
        "cherche": "Пошук апаратури...",
        "absente": "RadioMaster Pocket не знайдено.\n  1. Під'єднайте апаратуру до ПК кабелем USB-C з підтримкою передачі даних.\n  2. Увімкніть її та виберіть на екрані USB STORAGE.\n  3. Зачекайте кілька секунд і натисніть Enter, щоб шукати знову.",
        "plusieurs": "Знайдено кілька апаратур. Введіть номер вашої: ",
        "trouvee": "RadioMaster Pocket знайдено на диску {d} (EdgeTX {v}).",
        "anim_q": "За бажанням: анімована заставка GaboLabs зі звуковим супроводом і світлодіодною анімацією.\nПотрібна власна прошивка EdgeTX, яку ви прошиваєте самі після встановлення (див. інструкцію).\n  1. Так, додати\n  2. Ні, залишити офіційну прошивку\nВаш вибір (1 або 2): ",
        "recap": "Усе готово до встановлення: мова голосу {l}, прошивка з анімацією: {a}. Спочатку буде створено повну резервну копію SD-карти.",
        "oui": "так",
        "non": "ні",
        "go": "Введіть Y і натисніть Enter, щоб почати (будь-що інше скасовує): ",
        "etape": "Крок {n} з {t}: {x}",
        "e1": "резервна копія всієї SD-карти",
        "e2": "налаштування апаратури",
        "e3": "модель UFDS",
        "e4": "голосовий пакет",
        "e5": "файли прошивки",
        "sauve": "Резервна копія: {p}",
        "modele_ok": "Модель UFDS додано як {f} (позиція {n} у списку моделей).",
        "modele_la": "[I-MODEL-PRESENT] Модель UFDS уже є на апаратурі ({f}): її залишено без змін.",
        "voix_ok": "Встановлено голосових файлів: {n}.",
        "fw_ok": "Скопійовано в FIRMWARE: {f}",
        "fini": "Готово! Що далі:\n  1. Безпечно вилучіть апаратуру у Windows (значок USB біля годинника) і від'єднайте її.\n  2. Якщо ви обрали прошивку з анімацією: прошийте її (інструкція, розділ 3).\n  3. На апаратурі: довго натисніть MDL і виберіть UFDS.\n  4. У грі: призначте керування (інструкція, розділ 5).",
        "guide": "Інструкція: {g}",
        "annule": "Скасовано. Нічого не змінено.",
        "rien": "На апаратурі нічого не змінено.",
        "e_version": "[E-VERSION] Знайдено EdgeTX {v}, потрібна версія 2.12.\nСпочатку прошийте EdgeTX 2.12, один раз увімкніть апаратуру й запустіть інсталятор знову.",
        "e_board": "[E-BOARD] Ця SD-карта не з RadioMaster Pocket.",
        "e_cle": "[E-SETTINGS] Неочікуваний файл налаштувань апаратури ({c}).",
        "e_sauve": "[E-BACKUP] Резервна копія неповна ({n}/{t} файлів).",
        "fin_touche": "Натисніть Enter, щоб закрити це вікно.",
        "fw_q": "Пакет може підготувати офіційне оновлення до EdgeTX 2.12.4:\n  - повна резервна копія SD-карти,\n  - офіційний вміст SD-карти EdgeTX,\n  - перевірку перемикачів під час увімкнення у ваших моделях буде переписано у форматі 2.12 (ті самі положення),\n  - офіційну прошивку EdgeTX 2.12.4 буде скопійовано на апаратуру.\nВведіть Y і натисніть Enter, щоб підготувати оновлення (будь-яка інша відповідь скасує його): ",
        "fw_etapes": "Офіційну прошивку EdgeTX 2.12.4 скопійовано на апаратуру: FIRMWARE/OFFICIAL-2.12.4.bin\nТепер прошийте її (близько хвилини):\n  1. Безпечно вилучіть апаратуру у Windows (значок USB біля годинника), від'єднайте й вимкніть її.\n  2. Трими – це два міні-джойстики з обох боків від кнопки живлення.\n     Натисніть обидва в бік кнопки живлення (до центру) й утримуйте їх,\n     потім, не відпускаючи їх, натисніть і утримуйте кнопку живлення, доки не засвітиться екран.\n     Відкриється чорно-біле меню, завантажувач (bootloader). Відпустіть трими.\n  3. Прокрутіть коліщатко, виберіть Write Firmware і натисніть на коліщатко.\n  4. Виберіть OFFICIAL-2.12.4.bin, натисніть на коліщатко,\n     потім утримуйте коліщатко натиснутим, доки не з'явиться Writing...\n  5. Дочекайтеся напису Writing complete, натисніть на коліщатко, виберіть Exit і знову натисніть на коліщатко.\n  6. Апаратура запуститься з EdgeTX 2.12: дайте їй один раз повністю завантажитися.\n     Якщо на екрані з'явиться попередження, виконайте його вказівку (наприклад, переведіть перемикачі вгору).\n  7. Під'єднайте апаратуру знову, виберіть USB STORAGE і запустіть інсталятор ще раз.",
        "alertes_ok": "Перевірку перемикачів під час увімкнення переписано у форматі EdgeTX 2.12 (ті самі положення), моделей: {n}.",
        "sd_ok": "Встановлено офіційний вміст SD-карти EdgeTX {v} (файлів: {n}).",
        "patiente": "Триває копіювання, зачекайте. НЕ від'єднуйте апаратуру.",
        "r_aucune": "[E-NOBACKUP] У {d} не знайдено жодної резервної копії.",
        "r_liste": "Знайдені резервні копії (найновіші першими):",
        "r_choix": "Введіть номер копії для відновлення: ",
        "r_confirm": "SD-карту апаратури буде замінено цією копією: {b}\nВведіть Y і натисніть Enter, щоб підтвердити: ",
        "r_ok": "Апаратуру відновлено з {b}. Вилучіть її, від'єднайте й увімкніть.",
    },
    "fr": {
        "titre": "PocketUFDS {v} : RadioMaster Pocket pour Ukrainian Fight Drone Simulator",
        "menu": "Que veux-tu faire ?\n  1. Installer le pack sur ma radio\n  2. Restaurer ma radio depuis une sauvegarde\nTon choix (1 ou 2) : ",
        "cherche": "Recherche de la radio...",
        "absente": "Aucune RadioMaster Pocket trouvée.\n  1. Branche la radio au PC avec un câble USB-C de données.\n  2. Allume-la et choisis USB STORAGE sur son écran.\n  3. Attends quelques secondes, puis appuie sur Entrée pour chercher à nouveau.",
        "plusieurs": "Plusieurs radios trouvées. Tape le numéro de la tienne : ",
        "trouvee": "RadioMaster Pocket trouvée sur {d} (EdgeTX {v}).",
        "anim_q": "En option : l'écran de démarrage animé GaboLabs, avec bande-son et jeu de lumière.\nIl faut un firmware EdgeTX maison, que tu flasheras toi-même ensuite (voir le guide).\n  1. Oui, l'inclure\n  2. Non, garder le firmware officiel\nTon choix (1 ou 2) : ",
        "recap": "Prêt à installer : voix {l}, firmware animé {a}. Une sauvegarde complète de la carte SD est faite d'abord.",
        "oui": "oui",
        "non": "non",
        "go": "Tape Y puis Entrée pour commencer (toute autre réponse annule) : ",
        "etape": "Étape {n} sur {t} : {x}",
        "e1": "sauvegarde de toute la carte SD",
        "e2": "réglages de la radio",
        "e3": "modèle UFDS",
        "e4": "pack de voix",
        "e5": "fichiers du firmware",
        "sauve": "Sauvegarde : {p}",
        "modele_ok": "Modèle UFDS ajouté sous {f} (position {n} dans la liste des modèles).",
        "modele_la": "[I-MODEL-PRESENT] Un modèle UFDS est déjà sur la radio ({f}) : il est conservé tel quel.",
        "voix_ok": "{n} fichiers de voix installés.",
        "fw_ok": "Copié dans FIRMWARE : {f}",
        "fini": "Terminé ! La suite :\n  1. Éjecte la radio dans Windows (icône USB près de l'horloge), débranche-la.\n  2. Si tu as choisi le firmware animé : flashe-le (guide, partie 3).\n  3. Sur la radio : appui long sur MDL, puis choisis UFDS.\n  4. Dans le jeu : associe les commandes (guide, partie 5).",
        "guide": "Guide : {g}",
        "annule": "Annulé. Rien n'a été modifié.",
        "rien": "Rien n'a été modifié sur la radio.",
        "e_version": "[E-VERSION] EdgeTX {v} trouvé, la version 2.12 est nécessaire.\nFlashe d'abord EdgeTX 2.12, allume la radio une fois, puis relance cet installateur.",
        "e_board": "[E-BOARD] Cette carte SD ne vient pas d'une RadioMaster Pocket.",
        "e_cle": "[E-SETTINGS] Fichier de réglages de la radio inattendu ({c}).",
        "e_sauve": "[E-BACKUP] La sauvegarde est incomplète ({n}/{t} fichiers).",
        "fin_touche": "Appuie sur Entrée pour fermer cette fenêtre.",
        "fw_q": "Le pack peut préparer la mise à jour officielle vers EdgeTX 2.12.4 :\n  - sauvegarde complète de la carte SD,\n  - contenu officiel EdgeTX de la carte SD,\n  - vérification des interrupteurs au démarrage de tes modèles réécrite au format 2.12 (mêmes positions),\n  - firmware officiel EdgeTX 2.12.4 copié sur la radio.\nTape Y puis Entrée pour la préparer (toute autre réponse annule) : ",
        "fw_etapes": "EdgeTX 2.12.4 officiel copié sur la radio : FIRMWARE/OFFICIAL-2.12.4.bin\nFlashe-le maintenant (environ une minute) :\n  1. Éjecte la radio dans Windows (icône USB près de l'horloge), débranche-la et éteins-la.\n  2. Les trims sont les deux mini-joysticks de chaque côté du bouton d'allumage.\n     Pousse-les tous les deux vers le bouton d'allumage (vers le centre) et maintiens-les,\n     puis, sans les relâcher, appuie sur le bouton d'allumage et maintiens-le jusqu'à ce que l'écran s'allume.\n     Un menu noir et blanc s'ouvre : le bootloader. Relâche les trims.\n  3. Tourne la molette jusqu'à Write Firmware, puis appuie sur la molette.\n  4. Choisis OFFICIAL-2.12.4.bin, appuie sur la molette,\n     puis garde-la enfoncée jusqu'à voir Writing...\n  5. Attends Writing complete, appuie sur la molette, choisis Exit, appuie sur la molette.\n  6. La radio démarre en EdgeTX 2.12 : laisse-la démarrer complètement une fois.\n     Si un avertissement s'affiche, fais ce qu'il demande (par exemple, interrupteurs vers le haut).\n  7. Rebranche la radio, choisis USB STORAGE et relance cet installateur.",
        "alertes_ok": "Vérification des interrupteurs au démarrage réécrite au format EdgeTX 2.12 (mêmes positions) : {n} modèle(s).",
        "sd_ok": "Contenu officiel EdgeTX {v} de la carte SD installé ({n} fichiers).",
        "patiente": "Copie en cours, patiente. NE débranche PAS la radio.",
        "r_aucune": "[E-NOBACKUP] Aucune sauvegarde trouvée dans {d}.",
        "r_liste": "Sauvegardes trouvées (la plus récente d'abord) :",
        "r_choix": "Tape le numéro de la sauvegarde à restaurer : ",
        "r_confirm": "La carte SD de la radio va être remplacée par cette sauvegarde : {b}\nTape Y puis Entrée pour confirmer : ",
        "r_ok": "Radio restaurée depuis {b}. Éjecte-la, débranche-la et allume-la.",
    },
}
GUIDES = {"en": "GUIDE.md", "uk": "GUIDE_UK.md", "fr": "GUIDE_FR.md"}
# nom court : le bootloader de la Pocket coupe les noms vers 20 caractères (128 px)
FIRMWARE_OFFICIEL = "OFFICIAL-2.12.4.bin"
ZIP_SD_OFFICIEL = "edgetx-sdcard-bw128x64-2.12.3.zip"  # EdgeTX/edgetx-sdcard, GPL
BANNIERE = r"""
   ____    _    ____   ___  _        _    ____  ____
  / ___|  / \  | __ ) / _ \| |      / \  | __ )/ ___|
 | |  _  / _ \ |  _ \| | | | |     / _ \ |  _ \\___ \
 | |_| |/ ___ \| |_) | |_| | |___ / ___ \| |_) |___) |
  \____/_/   \_\____/ \___/|_____/_/   \_\____/|____/
            PocketUFDS  ·  Слава Україні!
"""
L = "en"
INTERACTIF = True


def tr(cle: str, **k) -> str:
    return T[L][cle].format(**k)


def couleur(texte: str, code: str) -> str:
    return f"\033[{code}m{texte}\033[0m"


def fin_fenetre() -> None:
    if INTERACTIF:
        input("\n" + tr("fin_touche"))


def stop(message: str) -> None:
    print("\n" + couleur(message, "91"))
    print(tr("rien"))
    fin_fenetre()
    sys.exit(1)


def etape(n: int, total: int, cle: str) -> None:
    print("\n" + couleur(tr("etape", n=n, t=total, x=tr(cle)), "96"))


def crc16(data: bytes) -> int:
    """EdgeTX radio.yml checksum: CRC-16 CCITT-FALSE over everything after the checksum line."""
    crc = 0xFFFF
    for b in data:
        crc ^= b << 8
        for _ in range(8):
            crc = (
                ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
            )
    return crc


def langue_windows() -> str:
    try:
        primaire = ctypes.windll.kernel32.GetUserDefaultUILanguage() & 0x3FF
        return {0x22: "uk", 0x0C: "fr"}.get(primaire, "en")
    except Exception:
        return "en"


def infos_carte(sd: Path) -> tuple[bool, str]:
    """(est une Pocket, version EdgeTX) ou (False, '') si ce n'est pas une carte EdgeTX."""
    try:
        t = (sd / "RADIO/radio.yml").read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False, ""
    m = re.search(r"^semver: (\S+)", t, re.M)
    return bool(re.search(r"^board: pocket\s*$", t, re.M)), (m.group(1) if m else "?")


def trouver_radios() -> list[Path]:
    trouvees = []
    for lettre in string.ascii_uppercase:
        racine = Path(f"{lettre}:/")
        try:
            if (racine / "RADIO/radio.yml").is_file() and infos_carte(racine)[0]:
                trouvees.append(racine)
        except OSError:
            continue  # lecteur vide (lecteur de cartes sans carte) : on l'ignore
    return trouvees


def choisir_radio() -> Path:
    while True:
        print(tr("cherche"))
        radios = trouver_radios()
        if len(radios) == 1:
            return radios[0]
        if len(radios) > 1:
            for i, r in enumerate(radios, 1):
                print(f"  {i}. {r}")
            choix = input(tr("plusieurs")).strip()
            if choix.isdigit() and 1 <= int(choix) <= len(radios):
                return radios[int(choix) - 1]
            continue
        print("\n" + couleur(tr("absente"), "93"))
        input()


def convertir_alertes(sd: Path) -> None:
    """Réécrit « switchWarningState: AuBuCuDu » (format 2.10) en « switchWarning: » natif 2.12.

    EdgeTX 2.12.4 relit mal l'ancien format (3 bits par interrupteur rangés, 2 lus) : sans cette
    réécriture, AuBuCuDu devient « SB milieu, SE milieu ». Les positions écrites sont exactement
    celles de l'ancien format, rien d'autre ne change dans le fichier.
    """
    positions = {"u": "up", "-": "mid", "d": "down"}
    n = 0
    for f in sorted((sd / "MODELS").glob("model*.yml")):
        brut = f.read_bytes()
        fin = "\r\n" if b"\r\n" in brut else "\n"
        texte = brut.decode("utf-8")
        m = re.search(rf"^switchWarningState: ?\"?([A-Za-z\-]*)\"?{fin}", texte, re.M)
        if not m:
            continue
        valeur, bloc = m.group(1), ""
        for k in range(0, len(valeur) - 1, 2):
            lettre, etat = valeur[k], valeur[k + 1]
            if etat in positions:
                bloc += f"   S{lettre.upper()}:{fin}      pos: {positions[etat]}{fin}"
        bloc = f"switchWarning: {fin}{bloc}" if bloc else ""
        f.write_bytes((texte[: m.start()] + bloc + texte[m.end() :]).encode("utf-8"))
        n += 1
    if n:
        print("  " + tr("alertes_ok", n=n))


def maj_contenu_sd(sd: Path) -> None:
    """Pose le contenu SD officiel d'EdgeTX 2.12 (scripts, README) si la carte est d'une version antérieure."""
    try:
        actuelle = (sd / "edgetx.sdcard.version").read_text(encoding="utf-8").strip()
    except OSError:
        actuelle = ""
    if actuelle.startswith("2.12."):
        return
    with zipfile.ZipFile(PACK / "sdcard" / ZIP_SD_OFFICIEL) as z:
        fichiers = [i for i in z.infolist() if not i.is_dir()]
        for i in fichiers:
            cible = sd / i.filename
            cible.parent.mkdir(parents=True, exist_ok=True)
            cible.write_bytes(
                z.read(i)
            )  # écrase comme la mise à jour officielle, ne supprime rien
        version = z.read("edgetx.sdcard.version").decode().strip()
    print("  " + tr("sd_ok", v=version, n=len(fichiers)))


def plus_ancienne(version: str) -> bool:
    """Vrai pour une EdgeTX antérieure à 2.12 (2.10, 2.11...), faux pour 2.13 ou illisible."""
    m = re.match(r"(\d+)\.(\d+)\.", version)
    return bool(m) and (int(m.group(1)), int(m.group(2))) < (2, 12)


def proposer_officiel(
    sd: Path, version: str, copie: str | None, dossier_sauv: Path
) -> None:
    """Radio trop ancienne : propose de poser EdgeTX 2.12.4 officiel et explique le flash pas à pas."""
    print("\n" + couleur(tr("e_version", v=version).split("\n")[0], "93"))
    if copie:
        reponse = copie
    else:
        reponse = input(tr("fw_q")).strip().lower() if INTERACTIF else "no"
    if reponse not in ("y", "yes"):
        stop(tr("e_version", v=version))
    print("  " + tr("sauve", p=sauvegarder(sd, dossier_sauv)))
    maj_contenu_sd(sd)
    convertir_alertes(sd)
    source = PACK / "firmware" / FIRMWARE_OFFICIEL
    cible = sd / "FIRMWARE" / FIRMWARE_OFFICIEL
    cible.parent.mkdir(exist_ok=True)
    shutil.copyfile(source, cible)
    if (
        cible.read_bytes() != source.read_bytes()
    ):  # carte pleine ou retirée pendant la copie
        cible.unlink(missing_ok=True)
        stop(tr("e_version", v=version))
    print("\n" + couleur(tr("fw_etapes"), "92"))
    fin_fenetre()
    sys.exit(0)


def verifier_carte(
    sd: Path,
    copie_officiel: str | None = None,
    proposer: bool = False,
    dossier_sauv: Path = Path.home() / "Documents",
) -> str:
    est_pocket, version = infos_carte(sd)
    if not (sd / "RADIO/radio.yml").exists() or not est_pocket:
        stop(tr("e_board"))
    if not version.startswith("2.12."):
        if proposer and plus_ancienne(version):
            proposer_officiel(sd, version, copie_officiel, dossier_sauv)
        stop(tr("e_version", v=version))
    return version


def copier_avec_progression(source: Path, cible: Path) -> int:
    """Copie un dossier fichier par fichier en affichant une barre de progression. Rend le nombre copié."""
    fichiers = [
        f
        for f in source.rglob("*")
        if f.is_file() and "System Volume Information" not in f.parts
    ]
    print("  " + couleur(tr("patiente"), "93"))
    total = max(len(fichiers), 1)
    for i, f in enumerate(fichiers, 1):
        dest = cible / f.relative_to(source)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, dest)
        if i == total or i % 5 == 0:
            plein = round(24 * i / total)
            print(
                f"\r  [{'█' * plein}{'░' * (24 - plein)}] {round(100 * i / total):3d} % ({i}/{total})",
                end="",
                flush=True,
            )
    print()
    return len(fichiers)


def sauvegarder(sd: Path, dest_racine: Path) -> Path:
    dest = dest_racine / f"PocketUFDS_backup_{datetime.datetime.now():%Y%m%d_%H%M%S}"
    copier_avec_progression(sd, dest)
    n_src = sum(
        1
        for p in sd.rglob("*")
        if p.is_file() and "System Volume Information" not in p.parts
    )
    n_dst = sum(1 for p in dest.rglob("*") if p.is_file())
    if n_src != n_dst:
        stop(tr("e_sauve", n=n_dst, t=n_src))
    return dest


def regler_radio(sd: Path, tts: str) -> None:
    radio = sd / "RADIO/radio.yml"
    brut = radio.read_bytes()
    fin = "\r\n" if b"\r\n" in brut else "\n"
    t = brut.decode()

    def poser_cle(cle: str, valeur: str) -> None:
        nonlocal t
        # [^\r\n]* et pas .* : le point avale le \r des fins de ligne CRLF (fichier mixte, 11/10)
        motif = re.compile(rf"^{cle}: [^\r\n]*", re.M)
        if len(motif.findall(t)) != 1:
            stop(tr("e_cle", c=cle))
        t = motif.sub(f"{cle}: {valeur}", t)
        print(f"  {cle} = {valeur}")

    poser_cle("audioMuteEnable", "1")
    poser_cle("ttsLanguage", f'"{tts}"')
    inactivite = re.search(r"^inactivityTimer: (\d+)", t, re.M)
    if inactivite and int(inactivite.group(1)) > 30:
        poser_cle("inactivityTimer", "10")
    # Écran principal : la page d'usine (view 18 = VIEW_INPUTS + ALTERNATE_VIEW) dessine les interrupteurs
    # logiques en barres. Vide sur les modèles d'usine, elle devient illisible avec les 9 du modèle UFDS.
    # On passe à la page « entrées » (2 : manches et interrupteurs), seulement si le joueur n'a rien choisi.
    if re.search(r"^view: 18\r?$", t, re.M):
        poser_cle("view", "2")
    # Section switchConfig : EdgeTX ne l'écrit que si un type diffère du défaut. Les défauts de la
    # Pocket (util/hw_defs/switch_config.py) sont exactement TYPES_INTERS : section ou ligne absente
    # = déjà correct. Seuls les types écrits ET faux sont corrigés (usine RadioMaster, 11/10).
    bloc = re.search(rf"^switchConfig: ?{fin}((?:   .*{fin})*)", t, re.M)
    if not bloc:
        print("  switches = EdgeTX defaults (already correct)")
    else:
        section = bloc.group(1)
        for sw, typ in TYPES_INTERS.items():
            motif = re.compile(
                rf"(^   {sw}:{fin}(?:      [^\r\n]*{fin})*?      type: )[^\r\n]+", re.M
            )
            n = len(motif.findall(section))
            if n > 1:
                stop(tr("e_cle", c=sw))
            if n == 1:
                section = motif.sub(rf"\g<1>{typ}", section)
                print(f"  {sw} = {typ}")
        t = t[: bloc.start(1)] + section + t[bloc.end(1) :]
    lignes = t.encode().split(fin.encode())
    corps = fin.encode().join(lignes[1:])
    radio.write_bytes(f"checksum: {crc16(corps)}".encode() + fin.encode() + corps)


def installer_modele(sd: Path) -> None:
    modeles = sd / "MODELS"
    for f in sorted(modeles.glob("model*.yml")):
        if re.search(
            r'^   name: "UFDS"', f.read_text(encoding="utf-8", errors="replace"), re.M
        ):
            print("  " + tr("modele_la", f=f.name))
            return
    libres = [i for i in range(60) if not (modeles / f"model{i:02d}.yml").exists()]
    cible = modeles / f"model{libres[0]:02d}.yml"
    shutil.copyfile(PACK / "modele/UFDS.yml", cible)
    print("  " + tr("modele_ok", f=cible.name, n=f"{libres[0] + 1:02d}"))


def installer_voix(sd: Path, langue: str, anim: bool) -> None:
    dossier, _, source = LANGUES[langue]
    cible = sd / "SOUNDS" / dossier
    copier_avec_progression(source, cible)
    if anim:
        shutil.copyfile(
            PACK / f"demarrage/hello_{langue}.wav", cible / "SYSTEM/hello.wav"
        )
    print("  " + tr("voix_ok", n=sum(1 for _ in cible.rglob("*.wav"))))


def copier_firmwares(sd: Path) -> None:
    (sd / "FIRMWARE").mkdir(exist_ok=True)
    for f in sorted((PACK / "firmware").glob("*.bin")):
        shutil.copyfile(f, sd / "FIRMWARE" / f.name)
        print("  " + tr("fw_ok", f=f.name))


def restaurer(sd: Path, dossier_sauvegardes: Path, confirme: bool) -> None:
    sauvegardes = sorted(dossier_sauvegardes.glob("PocketUFDS_backup_*"), reverse=True)
    if not sauvegardes:
        stop(tr("r_aucune", d=dossier_sauvegardes))
    choix = sauvegardes[0]
    if not confirme:
        print(tr("r_liste"))
        for i, s in enumerate(sauvegardes, 1):
            print(f"  {i}. {s.name}")
        n = input(tr("r_choix")).strip()
        if not (n.isdigit() and 1 <= int(n) <= len(sauvegardes)):
            stop(tr("annule"))
        choix = sauvegardes[int(n) - 1]
        if input(tr("r_confirm", b=choix.name)).strip().lower() != "y":
            stop(tr("annule"))
    for p in sorted(
        sd.rglob("*"), reverse=True
    ):  # la carte devient l'image exacte de la sauvegarde
        if "System Volume Information" in p.parts:
            continue
        if p.is_file():
            p.unlink()
        elif p.is_dir() and not any(p.iterdir()):
            p.rmdir()
    copier_avec_progression(choix, sd)
    print("\n" + couleur(tr("r_ok", b=choix.name), "92"))


def main() -> None:
    global L, INTERACTIF
    os.system("")  # active les couleurs ANSI dans la console Windows
    try:
        sys.stdout.reconfigure(
            encoding="utf-8"
        )  # cyrillique et accents même si la sortie est redirigée
    except (AttributeError, ValueError):
        pass
    if os.name == "nt":
        ctypes.windll.kernel32.SetConsoleTitleW("GaboLabs PocketUFDS")
    print(couleur(BANNIERE, "93"))
    a = argparse.ArgumentParser()
    a.add_argument("--sd")
    a.add_argument("--lang", choices=LANGUES)
    a.add_argument("--anim", choices=("yes", "no"))
    a.add_argument("--restore", action="store_true")
    a.add_argument(
        "--copy-official", choices=("yes", "no"), help="radio < 2.12 (tests)"
    )
    a.add_argument("--backup-dir", default=str(Path.home() / "Documents"))
    a.add_argument("--yes", action="store_true", help="no question, no pause (tests)")
    args = a.parse_args()
    INTERACTIF = not args.yes

    if args.lang or args.yes:
        L = args.lang or "en"
    else:
        defaut = langue_windows()
        ordre = ["en", "uk", "fr"]
        print("  1. English\n  2. Українська\n  3. Français")
        choix = input(
            f"Language / Мова / Langue (1-3, Enter = {ordre.index(defaut) + 1}): "
        ).strip()
        L = ordre[int(choix) - 1] if choix in ("1", "2", "3") else defaut
    print("\n" + couleur(tr("titre", v=VERSION_PACK), "1"))

    restauration = args.restore or (
        INTERACTIF and input("\n" + tr("menu")).strip() == "2"
    )
    sd = Path(args.sd) if args.sd else choisir_radio()
    version = verifier_carte(
        sd, args.copy_official, not restauration, Path(args.backup_dir)
    )
    print(couleur(tr("trouvee", d=str(sd).rstrip("\\/"), v=version), "92"))

    if restauration:
        restaurer(sd, Path(args.backup_dir), confirme=args.yes)
        fin_fenetre()
        return

    anim = (
        args.anim == "yes" if args.anim else input("\n" + tr("anim_q")).strip() == "1"
    )
    print("\n" + tr("recap", l=L, a=tr("oui") if anim else tr("non")))
    if INTERACTIF and input(tr("go")).strip().lower() != "y":
        stop(tr("annule"))

    total = 5 if anim else 4
    etape(1, total, "e1")
    print("  " + tr("sauve", p=sauvegarder(sd, Path(args.backup_dir))))
    etape(2, total, "e2")
    regler_radio(sd, LANGUES[L][1])
    maj_contenu_sd(sd)
    convertir_alertes(sd)
    etape(3, total, "e3")
    installer_modele(sd)
    etape(4, total, "e4")
    installer_voix(sd, L, anim)
    if anim:
        etape(5, total, "e5")
        copier_firmwares(sd)
    print("\n" + couleur(tr("fini"), "92"))
    guide = (
        Path(sys.executable).parent if getattr(sys, "frozen", False) else PACK.parent
    ) / GUIDES[L]
    print(tr("guide", g=guide))
    fin_fenetre()


if __name__ == "__main__":
    main()
