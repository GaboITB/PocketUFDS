# PocketUFDS: RadioMaster Pocket ready for Ukrainian Fight Drone Simulator

Free pack by GaboLabs. It turns a **RadioMaster Pocket** into a ready-to-fly controller for
**Ukrainian Fight Drone Simulator (UFDS)** in about 15 minutes:

- a **UFDS radio model**: all 10 game actions on the radio, no keyboard needed,
- **high-quality voice packs** in **Ukrainian, English and French** (alerts and flight announcements),
- an **optional animated boot screen** with soundtrack and LED light show (custom EdgeTX build).

> **Tested on:** RadioMaster Pocket (ELRS), EdgeTX 2.12.4, UFDS on Windows 11. Other radios are not supported.

---

## 1. Before you start

| You need | Why |
|---|---|
| A RadioMaster Pocket on **EdgeTX 2.12.x** | older version (2.10, 2.11)? The installer prepares the official update to EdgeTX 2.12.4 for you and shows how to flash it |
| A USB-C data cable | to reach the radio's SD card |
| Windows PC with UFDS installed | to map the game |

**Safety:** the installer makes a **full backup of your SD card** before changing anything
(in your Documents folder: `PocketUFDS_backup_<date>`). It never overwrites your existing models
and keeps your stick calibration.

---

## 2. Install the pack (installer)

1. Connect the radio with a USB-C data cable, turn it on and choose **USB Storage** on its screen.
2. Run `PocketUFDS-Installer.exe`. If Windows shows *Windows protected your PC*, click **More info**,
   then **Run anyway** (the installer is free and not code-signed).
3. Choose the language (Enter = your Windows language), then **1. Install**. The installer finds the radio by itself.
4. Answer the question about the animated boot screen (1 = yes, 2 = no), read the summary, type `Y` then Enter.
5. A progress bar shows each step. Do not unplug the radio before **Done!**, then eject it in Windows and unplug it.

**Radio on an older EdgeTX (2.10, 2.11):** the installer prepares the official update to EdgeTX 2.12.4,
included in the pack: full backup, official EdgeTX SD card content, official firmware. It also rewrites the
startup switch check of your models in the 2.12 format, with the same positions: EdgeTX 2.12.4 reads the old
format wrongly (your factory model would ask for SB and SE in the middle). Then it shows the flash steps (same
method as part 3, with `OFFICIAL-2.12.4.bin`). Flash it, let the radio start once, then run the installer again.

What the installer changes on your radio:

| Item | Change |
|---|---|
| Switch types | SA and SD = 2 positions, SB and SC = 3 positions, SE = momentary button (factory setting is often wrong) |
| Audio mute | ON: removes the speaker hiss between sounds |
| Voice language | the language you chose |
| Inactivity alarm | 10 minutes (if it was longer) |
| Models | adds the **UFDS** model on the first free slot |

---

## 3. Optional: flash the animated firmware

Only if you answered **1 (yes)** to the boot screen question. Two firmware files are now in the radio's `FIRMWARE` folder:

| File | What it is |
|---|---|
| `GABOLABS-2.12.4.bin` | EdgeTX 2.12.4 + animated boot screen, soundtrack and LED show |
| `OFFICIAL-2.12.4.bin` | the official EdgeTX 2.12.4, to go back at any time |

1. Turn the radio **off**.
2. The **trims** are the two mini joysticks on each side of the power button. Push both **toward the power
   button** (toward the center) and hold them, then, without releasing them, press and hold **power** until the screen turns on: the bootloader
   opens (black and white menu). Release the trims.
3. Turn the scroll wheel to **Write Firmware**, press the wheel, select `GABOLABS-2.12.4.bin`, press the wheel,
   then **hold the wheel pressed** until `Writing...` appears.
4. Wait for `Writing complete`, press the wheel, select **Exit**, press the wheel. If a warning shows, do what it asks.
   Do not touch the sticks during the first boot animation.

**What the custom build removes to fit in the Pocket's 512 KB flash:** the heli menu, and support for
external FrSky (PXX1) and ImmersionRC Ghost modules. The internal ELRS module, USB joystick, Lua and voice
are untouched. The source patch is published with the pack (GPL v2, as EdgeTX).

During the boot animation, **any key skips it** (sound and LED stop too). Sticks and switches don't.

---

## 4. Select the model and prepare the radio

1. Turn the radio on. Long press **MDL**, select **UFDS**.
2. Recommended once: **SYS → Hardware → Calibration** (sticks AND the rear wheel S1, full travel).
3. Plug the radio into the PC and choose **USB Joystick**.

---

## 5. Map the game

In UFDS: **Settings → Control**, choose **EdgeTX Radiomaster Pocket Joystick** in the device list,
then set each action:

| Game action | Assign | Radio control |
|---|---|---|
| Throttle | Axis 3 | left stick, vertical |
| Yaw | Axis 4 | left stick, horizontal |
| Pitch | Axis 2 | right stick, vertical |
| Roll | Axis 1 | right stick, horizontal |
| Arm/Disarm | Axis 5 | **SD** (right, outer) |
| Flight mode | Axis 6 | **SB** (left, 3 positions) |
| VTX Power | Axis 8 | **SC** (right, 3 positions) |
| Servo camera | Axis 7 | **S1** (rear wheel, right) |
| Bomb | Button 1 | **SE** (button) |
| Arm bomb | Button 2 | **SA** (left, outer, just in front of SE) |

> Axis 7 and Axis 8 are swapped compared to the radio channels: this is normal (Windows order).

**Realistic profile** (as FPV pilots fly): in the stick rows set **Dead zone 0.005 / Exponent 0.20**
for Roll and Pitch, **0.01 / 0.15** for Yaw, **0 / 0** for Throttle. Play in **full screen**.

**Flight modes on SB** depend on the drone: on FPV drones SB up/middle = ACRO, down = STAB,
on heavy bombers up = STAB, middle = ALTH (altitude hold), down = LOIT (position hold).

---

## 6. Voice announcements (UFDS model)

| Control | Announcement |
|---|---|
| SA | bomb armed / bomb safe |
| SB | flight mode one / two / three |
| SC | video, low / medium / high power |
| SD | armed / disarmed |
| SE | drop |

A silent **flight timer (VOL)** runs while the drone is armed (SD). At power-on, every switch must be
**away from you**: SD disarmed, SA bomb safe, SB flight mode one, SC low video power, plus throttle low.

**Why this layout:** the bomb safety (SA) and the drop button (SE) sit under the same finger, like the
safety and the trigger of a weapon. The motor arming switch (SD) is on the other side: reaching for SE
in flight can never disarm the motors by mistake.

**Prefer another layout?** Change it in the radio, not in the game: MDL, MIXES page, change the source of
the channel lines (CH5 = arming, CH10 = arm bomb). Voice announcements and the flight timer follow the
channels, so they stay right. Only swap switches of the same type: SA with SD (2 positions),
SB with SC (3 positions).

**One model per game:** select UFDS (long press MDL) before playing UFDS, and your usual model for
other games. The UFDS model changes nothing in your other models.

---

## 7. Troubleshooting

| Problem | Fix |
|---|---|
| No sound at all after enabling Audio mute | **reboot the radio** once: the setting applies at power-on |
| The game uses keyboard, not the radio | the radio is in USB Storage mode: replug and choose **USB Joystick** |
| Camera "down" view hard to reach | calibrate **S1** (SYS → Hardware → Calibration) |
| Startup alert about switches | push **SA, SB, SC and SD** away from you, throttle low |
| Short beeps and vibrations at random moments on the factory model (POCKET) | the rear wheel S1 rests exactly in its middle and this model beeps at the centre: turn S1 to one end. The UFDS model does not do it |
| Alert `SB SE` at power-on on a model, after updating EdgeTX 2.10 or 2.11 to 2.12 **yourself** | EdgeTX 2.12.4 reads the old switch check format wrongly. Press any key to skip it, or set the check again in that model (MDL, page SETUP, section Pre-start Checks, line S-Warning). Updates prepared by the installer avoid it |
| Something went wrong | restore the backup folder from Documents onto the SD card, or flash `OFFICIAL-2.12.4.bin` |

---

## 8. Credits and licenses

- **EdgeTX** (GPL v2): the custom firmware patch and build instructions are included.
- **Voices** generated with ElevenLabs (Voice Library): **Yaroslava** (Ukrainian), **Nichalia Schwartz**
  (English), **Manon** (French) and **Yaroslava** for « Слава Україні! ». Phrase lists based on the
  official EdgeTX voice lists, corrected and completed.
- **Ukrainian coat of arms**: public domain (Wikimedia Commons).
- **Ukrainian texts** were checked by machine transcription and two independent automatic proofreaders,
  but **not yet by a native speaker**. Please report any mistake: it will be fixed.

Слава Україні! GaboLabs
