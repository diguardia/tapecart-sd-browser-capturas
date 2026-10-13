@echo off
rem Compila el browser en espanol e ingles con cc65 (https://cc65.github.io). cl65 tiene que estar en el PATH.
rem Builds the Spanish and English browser with cc65. cl65 must be in the PATH.
rem   bin\browser_es.prg  (espanol / Spanish)
rem   bin\browser_en.prg  (ingles / English)
rem Copiar uno a la raiz de la SD con el nombre browser.prg / Copy one to the SD root as browser.prg.
rem __HIMEM__=$C000 deja libre $C000-$FFFF para las capturas (bitmap en $E000, pantalla en $CC00).
cd /d "%~dp0browser"
set SRC=browser.c tapecartif.c minidelay.s getbyte_fast.s loader.s
cl65 -t c64 -Oi -Wl -D,__HIMEM__=0xC000 %SRC% -o ..\bin\browser_es.prg
if errorlevel 1 exit /b 1
del /q *.o 2>nul
cl65 -t c64 -Oi -Wl -D,__HIMEM__=0xC000 -DLANG_EN %SRC% -o ..\bin\browser_en.prg
if errorlevel 1 exit /b 1
del /q *.o 2>nul
cl65 -t c64 -O ..\norma\norma.c -o ..\bin\norma.prg
if errorlevel 1 exit /b 1
del /q ..\norma\*.o 2>nul
echo Listo / Done: bin\browser_es.prg bin\browser_en.prg bin\norma.prg
