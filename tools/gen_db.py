"""Genera index.db y shots.db para cada carpeta indexada de la SD.

Uso: python -I gen_db.py <raiz_sd> <catalog.json> <carpeta_capturas_gb64> <salida> [carpeta ...]
Escribe en <salida>/<carpeta>/index.db y shots.db; despues se copian a la misma carpeta de la SD.
Formato de los archivos: docs/FORMATO.md
"""
import json, os, re, struct, sys
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from png2c64 import convert, SLOT

REC = 80
TITLE_LEN = 30
PUB_LEN = 24
TYPES = {'prg': 2, 'tcrt': 3, 'tap': 4}
GENRES = {'Arcade': 1, "Shoot'em Up": 2, 'Adventure': 3, 'Brain': 4, 'Educational': 5,
          'Sports': 6, 'Strategy': 7, 'Gambling': 8, 'Board Game': 9, 'Cards': 10,
          'Racing': 11, 'Simulation': 12, 'Miscellaneous': 13}


def petscii(s, n):
    """ASCII -> PETSCII (juego de minusculas), recortado/rellenado a n bytes."""
    out = bytearray()
    for ch in s:
        c = ord(ch)
        if 0x61 <= c <= 0x7A:
            c -= 0x20
        elif 0x41 <= c <= 0x5A:
            c += 0x80
        elif c in (0x5F, 0x60, 0x7B, 0x7C, 0x7D, 0x7E) or c > 0x7E or c < 0x20:
            c = 0x20 if c != 0x5F else 0x2D
        out.append(c)
    return bytes(out[:n]).ljust(n, b'\0')


def display_title(t):
    return t if len(t) <= TITLE_LEN else t[:TITLE_LEN - 1] + '~'


def folder_title(folder):
    """Titulo de la carpeta: "Juegos A-Z/W" -> "Juegos A-Z - W" (sin prefijos numericos "2 ")."""
    parts = [re.sub(r'^\d+ ', '', p) for p in folder.split('/')]
    return ' - '.join(parts[-2:])


def build(folder, entries, shots_dir, out_dir, sd_root):
    files = sorted(f for f in os.listdir(os.path.join(sd_root, folder))
                   if os.path.isfile(os.path.join(sd_root, folder, f))
                   and f.lower() not in ('index.db', 'shots.db'))
    by_short = {e['short'].lower(): e for e in entries}
    rows = []
    for f in files:
        e = by_short.get(f.lower(), {})
        title = e.get('title') or os.path.splitext(f)[0]
        rows.append((title.lower(), f, e))
    rows.sort()

    recs = bytearray()
    shot_jobs = []
    for title_key, f, e in rows:
        ext = f.rsplit('.', 1)[-1].lower() if '.' in f else 'prg'
        typ = TYPES.get(ext, 0xFF)
        if len(f) > 16:
            # el firmware no ve nombres de mas de 16 caracteres: no se podria cargar
            print(f'  AVISO: "{folder}/{f}" tiene mas de 16 caracteres; renombralo para poder cargarlo')
            typ = 0xFF
        slot = 0xFFFF
        shot = e.get('shot', '')
        if shot:
            png = os.path.join(shots_dir, shot.replace('\\', '/'))
            if os.path.exists(png):
                slot = len(shot_jobs)
                shot_jobs.append(png)
        year = (e.get('year') or '')[:4]
        rec = struct.pack('<B16s30s4sBBH24sB', typ, f.encode('ascii', 'replace')[:16].ljust(16, b'\0'),
                          petscii(display_title(e.get('title') or os.path.splitext(f)[0]), TITLE_LEN),
                          petscii(year, 4), GENRES.get(e.get('genre', ''), 0), 0, slot,
                          petscii(e.get('publisher', ''), PUB_LEN), 0)
        assert len(rec) == REC
        recs += rec

    hdr = bytearray(REC)
    hdr[0:4] = b'TCIX'
    hdr[4] = 1
    struct.pack_into('<H', hdr, 6, len(rows))
    hdr[8] = 1 if shot_jobs else 0
    struct.pack_into('<H', hdr, 10, len(files))
    hdr[16:16 + TITLE_LEN] = petscii(folder_title(folder), TITLE_LEN)

    od = os.path.join(out_dir, folder)
    os.makedirs(od, exist_ok=True)
    with open(os.path.join(od, 'index.db'), 'wb') as fh:
        fh.write(hdr + recs)
    return od, shot_jobs


def conv(png):
    try:
        return convert(png)
    except Exception as ex:  # imagen rara: slot negro
        print('ERR', png, ex, flush=True)
        return bytes(SLOT)


def main():
    sd_root, catalog, shots_dir, out_dir = sys.argv[1:5]
    only = sys.argv[5:]  # opcional: limitar a algunas carpetas
    cat = json.load(open(catalog))
    folders = {}
    for e in cat:
        folders.setdefault(e['folder'], []).append(e)
    targets = list(folders)
    if only:
        targets = [f for f in targets if f in only]
    with Pool() as pool:
        for folder in sorted(targets):
            od, jobs = build(folder, folders[folder], shots_dir, out_dir, sd_root)
            with open(os.path.join(od, 'shots.db'), 'wb') as fh:
                for slot in pool.imap(conv, jobs, chunksize=8):
                    fh.write(slot)
            if not jobs:
                os.remove(os.path.join(od, 'shots.db'))
            print(f'{folder}: {len(jobs)} capturas', flush=True)


if __name__ == '__main__':
    main()
