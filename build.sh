#!/bin/sh
# Compila el browser en espanol e ingles con cc65 (https://cc65.github.io). cl65 tiene que estar en el PATH.
# Builds the Spanish and English browser with cc65. cl65 must be in the PATH.
#   bin/browser_es.prg  (espanol / Spanish)
#   bin/browser_en.prg  (ingles / English)
# Copiar uno a la raiz de la SD con el nombre browser.prg / Copy one to the SD root as browser.prg.
# __HIMEM__=$C000 deja libre $C000-$FFFF para las capturas (bitmap en $E000, pantalla en $CC00).
set -e
cd "$(dirname "$0")/browser"
SRC="browser.c tapecartif.c minidelay.s getbyte_fast.s loader.s"
cl65 -t c64 -Oi -Wl -D,__HIMEM__=0xC000 $SRC -o ../bin/browser_es.prg
rm -f *.o
cl65 -t c64 -Oi -Wl -D,__HIMEM__=0xC000 -DLANG_EN $SRC -o ../bin/browser_en.prg
rm -f *.o
cl65 -t c64 -O ../norma/norma.c -o ../bin/norma.prg
rm -f ../norma/*.o
echo "Listo / Done: bin/browser_es.prg bin/browser_en.prg bin/norma.prg"
