/* norma.prg - Christian Di Guardia, 2026. Compilar: cl65 -t c64 -O norma.c -o norma.prg */
/* Detecta la norma de video de la C64/C128: PAL, PAL-N (Drean) o NTSC.
   Mide los ciclos de un cuadro completo con el timer A del CIA 1. */
#include <stdio.h>
#include <conio.h>
#include <c64.h>
#include <6502.h>

#define RASTER (*(volatile unsigned char *)0xD012)
#define CTRL1  (*(volatile unsigned char *)0xD011)
#define TALO   (*(volatile unsigned char *)0xDC04)
#define TAHI   (*(volatile unsigned char *)0xDC05)
#define CRA    (*(volatile unsigned char *)0xDC0E)

static unsigned int frame_cycles(void)
{
    unsigned int t;
    SEI();
    CRA = 0x00;                 /* timer A detenido */
    TALO = 0xFF; TAHI = 0xFF;
    while (RASTER != 0x30 || (CTRL1 & 0x80)) ;
    while (RASTER == 0x30) ;
    CRA = 0x11;                 /* carga y arranca, continuo */
    while (RASTER != 0x30 || (CTRL1 & 0x80)) ;
    while (RASTER == 0x30) ;
    CRA = 0x00;
    { unsigned char lo = TALO, hi = TAHI; t = 0xFFFF - (lo | (hi << 8)); }
    /* restaurar el timer del sistema (IRQ de 60 Hz) */
    TALO = 0x25; TAHI = 0x40;
    CRA = 0x11;
    CLI();
    return t;
}

int main(void)
{
    unsigned int c = frame_cycles();
    unsigned int lines;
    const char *norma;

    lines = 0;
    while (RASTER != 0) ;
    /* linea maxima: bit 7 de $D011 es el bit 8 del raster */
    {
        unsigned int maxl = 0, l;
        unsigned int n;
        for (n = 0; n < 40000U; ++n) {
            l = RASTER | ((CTRL1 & 0x80) << 1);
            if (l > maxl) maxl = l;
        }
        lines = maxl + 1;
    }

    if (c > 19900)       norma = "PAL-N (Drean / Argentina)";
    else if (c > 19000)  norma = "PAL (Europa)";
    else if (c > 16900)  norma = "NTSC (EE.UU.)";
    else                 norma = "NTSC viejo (6567R56A)";

    clrscr();
    bordercolor(COLOR_BLACK);
    bgcolor(COLOR_BLACK);
    textcolor(COLOR_YELLOW);
    cputs("norma de video\r\n\r\n");
    textcolor(COLOR_WHITE);
    cprintf("ciclos por cuadro: %u\r\n", c);
    cprintf("lineas por cuadro: %u\r\n\r\n", lines);
    textcolor(COLOR_LIGHTGREEN);
    cprintf("tu maquina es: %s\r\n\r\n", norma);
    textcolor(COLOR_GRAY2);
    cputs("pal 19656 / pal-n 20280 / ntsc 17095\r\n");
    return 0;
}
