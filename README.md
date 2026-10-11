# PocketUFDS

**Free ready-to-play pack for the RadioMaster Pocket and Ukrainian Fight Drone Simulator (UFDS).**

Players often find it hard to set up a radio for UFDS. PocketUFDS does it in about fifteen minutes:
an installer sets up the radio, and a step-by-step guide maps the game.

## What you get

- **A UFDS radio model**: the 10 game actions on the radio, no keyboard needed. Motor arming on SD,
  bomb safety on SA right in front of the drop button SE.
- **Voice packs** in **Ukrainian**, **English** and **French**: EdgeTX system alerts and flight
  announcements (armed, flight mode, video power, bomb armed, drop...). The announcements follow the
  channels, so they stay right if you swap switches in the radio.
- **An installer for Windows** that finds the radio by itself, backs up the whole SD card first, never
  overwrites your models and keeps your stick calibration. It can restore the backup.
- **Optional**: an EdgeTX firmware with an animated GaboLabs boot screen, soundtrack and LED light show.
- **Guides** in English, Ukrainian and French.

## Requirements

- RadioMaster Pocket with **EdgeTX 2.12**. Older EdgeTX (2.10, 2.11)? The installer copies the
  official EdgeTX 2.12.4 for you and shows how to flash it.
- A USB-C **data** cable and a Windows PC with UFDS.

## Quick start

1. Connect the radio, turn it on, choose **USB Storage**.
2. Run `PocketUFDS-Installer.exe` and follow the screen.
3. Follow the guide for your language: `GUIDE.md` (English), `GUIDE_UK.md` (Ukrainian), `GUIDE_FR.md` (French).

## About the Ukrainian texts

The Ukrainian voice texts, guide and installer were checked by machine transcription and several
independent automatic proofreaders (including a search for Russianisms), but **not yet by a native
speaker**. If you find a mistake, please report it: it will be fixed.

## Credits

- **EdgeTX**, the open source radio firmware.
- **Voices** generated with ElevenLabs (Voice Library): **Yaroslava** (Ukrainian, and « Слава Україні! »
  in every language), **Nichalia Schwartz** (English), **Manon** (French).
- Phrase lists based on the official EdgeTX voice lists, corrected and completed.
- **Coat of arms of Ukraine**: public domain (Wikimedia Commons).

## Licenses

- The **firmware** is a modified EdgeTX and is licensed under the **GNU GPL v2**. Its complete source
  changes and build steps are in the `source/` folder (`BUILD.md`).
- The **code** (installer, scripts) is licensed under the **GNU GPL v2** (`LICENSE`).
- The **voices, radio model, guides and animation artwork** are licensed under **CC BY 4.0**
  (`LICENSE-CONTENT.md`): share and adapt them freely, credit « PocketUFDS by GaboLabs ».

PocketUFDS is an independent fan project. It is not affiliated with RadioMaster, EdgeTX or the
developers of Ukrainian Fight Drone Simulator.

Слава Україні! **GaboLabs**
