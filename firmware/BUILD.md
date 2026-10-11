# Building the GaboLabs EdgeTX firmware for the RadioMaster Pocket

`GABOLABS-2.12.4.bin` is the official **EdgeTX v2.12.4** firmware for the RadioMaster Pocket, plus
an animated boot screen, a soundtrack sync and an LED light show. EdgeTX is licensed under the
**GNU GPL v2** (see `LICENSE-EdgeTX-GPLv2.txt`), and so is this modified firmware. This folder
contains everything needed to rebuild it.

## Files

| File | Role |
|---|---|
| `edgetx-2.12.4-gabolabs-v3.patch` | changes to the EdgeTX source (splash screen, LED driver, key handling) |
| `gabolabs_leds.h` | LED light show timeline (copied into `radio/src/gui/128x64/`) |
| `animation_demarrage_v6.gif` | the boot animation, 128 x 64, 104 frames |
| `gif_vers_c.py` | converts the GIF into `gabolabs_splash.h` (XOR delta + RLE, about 10 KB) |
| `test_decodeur.c` | checks that the compressed frames decode back to the GIF, frame by frame |
| `animation_demarrage.py`, `tryzub_52_35.png` | how the animation itself was drawn |

## Steps

Requirements: Git, Python 3 with Pillow, Docker.

```bash
git clone --depth 1 --branch v2.12.4 --recurse-submodules --shallow-submodules \
  https://github.com/EdgeTX/edgetx.git edgetx
cd edgetx
git apply ../edgetx-2.12.4-gabolabs-v3.patch
cp ../gabolabs_leds.h radio/src/gui/128x64/
python3 ../gif_vers_c.py ../animation_demarrage_v6.gif radio/src/gui/128x64/gabolabs_splash.h

docker run --rm -v "$PWD:/src" -w /src ghcr.io/edgetx/edgetx-dev:2.12 bash -c '
  mkdir -p build && cd build
  cmake -DPCB=X7 -DPCBREV=POCKET -DHELI=NO -DPXX1=NO -DGHOST=NO -DCMAKE_BUILD_TYPE=Release ..
  make arm-none-eabi-configure
  cd arm-none-eabi && make firmware'
```

The result is `build/arm-none-eabi/firmware.bin`. Checked on 11 October 2026 from a fresh clone: the
rebuilt file is identical to `GABOLABS-2.12.4.bin` except for the 5 bytes of the build time stamp.

## Why some options are disabled

The Pocket uses an STM32F407xE with **512 KB of flash**. The animation does not fit with every
option enabled, so this build removes: the helicopter menu (`HELI`), external FrSky PXX1 modules
(`PXX1`) and ImmersionRC Ghost (`GHOST`). The internal ELRS module, USB joystick, Lua and voice
playback are untouched. The firmware uses about 509 KB of the 512 KB.

## Behaviour

- The animation starts with the soundtrack (`SOUNDS/<language>/SYSTEM/hello.wav`, played by
  EdgeTX right before the splash screen).
- Any key skips the animation and stops the sound and lights. Sticks and switches do not skip it.
- The power button LED follows the animation (7 colours), then returns to normal.
