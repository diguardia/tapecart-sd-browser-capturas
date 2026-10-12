#!/bin/sh
# Compila browser.prg con cc65 (https://cc65.github.io). cl65 tiene que estar en el PATH.
# __HIMEM__=$C000 deja libre $C000-$FFFF para mostrar las capturas (bitmap en $E000, pantalla en $CC00).
set -e
cd "$(dirname "$0")/browser"
cl65 -t c64 -Oi -Wl -D,__HIMEM__=0xC000 browser.c tapecartif.c minidelay.s getbyte_fast.s loader.s -o ../bin/browser.prg
echo "Listo: bin/browser.prg"
