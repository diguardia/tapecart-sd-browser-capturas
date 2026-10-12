"""Genera un catalogo HTML (pensado para el celular) con capturas, a partir de catalog.json.

Uso:
  python -I catalogo_html.py <catalog.json> <carpeta_capturas_gb64> <salida>

Crea <salida>/index.html y <salida>/img/. Para verlo en el celular, servilo en la red de casa con
servir_catalogo.py. Las capturas de GameBase64 son de uso personal: no publiques el resultado.
"""
import json, os, shutil, sys

GEN = {'Arcade': 'Arcade', "Shoot'em Up": "Shoot'em up", 'Adventure': 'Aventura', 'Brain': 'Ingenio',
       'Educational': 'Educativo', 'Sports': 'Deportes', 'Strategy': 'Estrategia', 'Gambling': 'Azar',
       'Board Game': 'Tablero', 'Cards': 'Cartas', 'Racing': 'Carreras', 'Simulation': 'Simulador',
       'Miscellaneous': 'Varios'}


def main():
    catalog, shots, out = sys.argv[1:4]
    os.makedirs(os.path.join(out, 'img'), exist_ok=True)
    rows = []
    for c in json.load(open(catalog)):
        img = ''
        if c.get('shot'):
            src = os.path.join(shots, c['shot'].replace('\\', '/'))
            if os.path.exists(src):
                img = f"{c['gbid']}.png"
                dst = os.path.join(out, 'img', img)
                if not os.path.exists(dst):
                    shutil.copyfile(src, dst)
        ext = c['short'].rsplit('.', 1)[-1].lower() if '.' in c['short'] else ''
        rows.append(dict(t=c['title'], y=c.get('year', ''), p=c.get('publisher', ''),
                         g=GEN.get(c.get('genre', ''), ''), f=c['folder'], n=c['short'],
                         i=img, x=ext, ok=ext in ('prg', 'p00', 'tap', 'tcrt')))
    rows.sort(key=lambda r: (r['t'].lower(), r['f']))
    tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'catalogo_tpl.html'), encoding='utf-8').read()
    with open(os.path.join(out, 'index.html'), 'w', encoding='utf-8') as fh:
        fh.write(tpl.replace('__DATA__', json.dumps(rows, ensure_ascii=False, separators=(',', ':'))))
    print(f"{len(rows)} juegos, {sum(1 for r in rows if r['i'])} con captura -> {out}")


if __name__ == '__main__':
    main()
