# Tapecart SD Browser with screenshots

*[Versión en español](README.md)*

A browser for the Commodore 64 **Tapecart SD** that shows each game's **full name, year, genre and publisher**
and its **screenshot**, right on the C64.

It is a **fork of [Tapecart SD Browser v1.4-TAP](https://github.com/rainisto/tapecart/tree/new_tap_with_1.4)**
(Jonni Rainisto, with TAP support by Jarkko Sonninen), itself derived from [Tapecart SD](https://github.com/KimJorgensen/tapecart)
by Kim Jørgensen, [tapecart](https://github.com/ikorb/tapecart) by Ingo Korb and Draco Browser by Sascha Bader.
See [CREDITOS.md](CREDITOS.md).

Fork by **Christian Di Guardia**, 2026. The on-screen texts are in Spanish.

| List | Screenshot (SPACE) | Credits (`.`) |
|---|---|---|
| ![list](docs/img/listado.png) | ![shot](docs/img/captura.png) | ![credits](docs/img/creditos.png) |

*(Captured in the VICE emulator.)*

## What it adds

- Folders with an `index.db`: full name (up to 30 characters; the firmware only shows 16), year, genre and publisher.
- Folders with a `shots.db`: **SPACE** shows the game's screenshot (hires or multicolor bitmap); RETURN from there loads the game.
- Folders without an index work like the original, but are **sorted alphabetically** (the original shows the physical SD order).
- Hides system folders (`System Volume Information`, `$RECYCLE.BIN`, macOS files).
- Loads PRG, TCRT and TAP like the original. **No firmware change needed.**

## Requirements

- Tapecart SD with firmware **v1.4-TAP** ([rainisto/tapecart, branch `new_tap_with_1.4`](https://github.com/rainisto/tapecart/tree/new_tap_with_1.4)).
  It should also work with Kim Jørgensen's v1.4 firmware, except TAP loading. *Untested.*
- To build: [cc65](https://cc65.github.io).
- To generate indexes and screenshots: Python 3, your own copy of [GameBase64](https://www.gb64.com) and,
  to export its database, Windows with the Access ODBC driver and [innoextract](https://constexpr.org/innoextract/).

## Install

1. Back up your original `browser.prg`.
2. Copy `bin/browser.prg` to the SD root. The firmware always loads `/browser.prg`.
3. Without indexes it already works, with an alphabetically sorted listing.

## Generating indexes and screenshots for your collection

GameBase64 data and screenshots are **for personal use only** (see *Licenses*), so this project ships no
index files: every user builds their own from their own copy.

1. Download the *GB64 Database* and *GB64 Screenshots* from [gb64.com/downloads.php](https://www.gb64.com/downloads.php).
2. Extract `GBC_vXX.mdb` from the installer without running it:
   `innoextract -I GBC_v19.mdb gb64v19.exe`
3. Export the database to CSV:
   `powershell -File tools\export_gb64.ps1 -Mdb app\GBC_v19.mdb -Out games.csv`
4. Build the catalog of your SD (e.g. `E:\`):
   `python -I tools\build_catalog.py E:\ games.csv catalog.json`
   - For files with short names, put the real title in `E:\titulos.csv` (lines `folder/file;Title`).
5. Generate indexes and screenshots:
   `python -I tools\gen_db.py E:\ catalog.json Screenshots out`
6. Copy each `out\<folder>\index.db` and `shots.db` into the same folder on the SD.

Tips:
- **Keep file names at 16 characters or fewer** (extension included); longer ones show as 8.3 names (`LASTNI~1.TAP`).
- If you add games to an indexed folder, the browser notices and shows the plain listing until you regenerate the index.
- The firmware **does not load D64/G64/T64**.

## Keys

| Key | Action |
|---|---|
| RETURN / fire | play / open folder |
| SPACE | show screenshot |
| DEL | parent folder |
| HOME | root folder |
| Cursor ↑↓ | move |
| Cursor ←→ | previous / next page |
| T / B | top / bottom |
| `.` | credits and help |
| Q | quit |

## Build

```
build.bat      (Windows)
./build.sh     (Linux / macOS)
```

The browser can be tested in VICE with `browser/mock_tapecartif.c`, which fakes the tapecart by reading
`dirlist`, `index.db` and `shots.db` from a PC folder mounted as drive 8.

File formats: [docs/FORMATO.md](docs/FORMATO.md) (Spanish).

## Licenses

- **Code derived from Draco Browser:** free to use as long as the notice of origin and author is kept.
- **Code derived from tapecart (Ingo Korb):** 2-clause BSD license, kept in each file.
- **Changes in this fork:** same terms, keeping these notices.
- **GameBase64:** data and screenshots © GB64 Team, **personal use only**. This project **does not include or redistribute them**.
  The tools read each user's own copy from [gb64.com](https://www.gb64.com).
- **Games:** this project neither includes nor links to any games.

NO WARRANTY. USE AT YOUR OWN RISK.
