/* Simulacion del tapecart para probar el browser en VICE.
   Lee "dirlist", "index.db" y "shots.db" de la unidad 8 (directorio del PC). */
#include <cbm.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>
#include "tapecartif.h"

static uint8_t state, pcount, params[5];
static uint8_t buf[128];
static uint8_t bpos, blen;

static void fopen_name(const char *n) { cbm_close(2); cbm_open(2, 8, 2, n); bpos = blen = 0; }
static uint8_t fget(void) {
    if (bpos >= blen) { int r = cbm_read(2, buf, sizeof(buf)); blen = r > 0 ? r : 0; bpos = 0; if (!blen) return 0; }
    return buf[bpos++];
}

bool tapecart_cmdmode(void) { return true; }
void tapecart_streammode(void) {}
void tapecart_sendbyte(uint8_t b) {
    if (state == 0) {
        if (b == CMD_SD_READ_DIR_FAST) { state = 1; pcount = 0; }
        return;
    }
    params[pcount++] = b;
    if (state == 1 && pcount == 2) { state = 0; fopen_name("dirlist"); }
}
void tapecart_send_u16(uint16_t v) { tapecart_sendbyte(v & 0xff); tapecart_sendbyte(v >> 8); }
void tapecart_send_u24(uint32_t v) { (void)v; }
uint8_t tapecart_getbyte(void) { return 0; }
uint8_t tapecart_getbyte_fast(void) { return fget(); }
void tapecart_read_loader(uint8_t *d) { (void)d; }
void tapecart_open_dir(char *path, char *new_path) { (void)path; memset(new_path, 0, 16); new_path[0] = 'w'; }

static char selected = 'i';
void tapecart_select_file(const char *name) { selected = name[0]; }

void tapecart_read_flash_fast(uint32_t offset, uint16_t len, void *data) {
    uint8_t *p = data;
    fopen_name(selected == 0x73 ? "shots.db" : "index.db");
    while (offset--) fget();
    while (len--) *p++ = fget();
}
