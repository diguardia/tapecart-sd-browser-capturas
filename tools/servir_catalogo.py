"""Sirve el catalogo en la red de casa para abrirlo desde el celular.

Uso:
  python -I servir_catalogo.py <carpeta_del_catalogo> [puerto]

Muestra la direccion para escribir en el navegador del celular (tiene que estar en el mismo Wi-Fi).
La primera vez Windows puede preguntar si permite el acceso a la red: elegi "Redes privadas".
Ctrl+C para cortar.
"""
import functools, http.server, socket, sys


def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))  # no envia nada; solo elige la interfaz de salida
        return s.getsockname()[0]
    except OSError:
        return '127.0.0.1'
    finally:
        s.close()


def main():
    folder = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8064
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=folder)
    with http.server.ThreadingHTTPServer(('0.0.0.0', port), handler) as srv:
        print(f'Abri en el celular:  http://{lan_ip()}:{port}/')
        print('Ctrl+C para cortar.')
        try:
            srv.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    main()
