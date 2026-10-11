// Test hors radio : même décompression que drawGabolabsFrame(), écrit chaque image en PBM.
#include <stdint.h>
#include <stdio.h>
#define LCD_W 128
#define LCD_H 64
#include <string.h>
#include "gabolabs_splash_test.h"

int main(void)
{
  static uint8_t ecran[LCD_W * LCD_H / 8];
  for (uint16_t idx = 0; idx < GABOLABS_ANIM_FRAMES; idx++) {
    // copie conforme de drawGabolabsFrame() (firmware)
    if (idx == 0) memset(ecran, 0, sizeof(ecran));
    const uint8_t * p = gabolabs_anim_data + gabolabs_anim_offsets[idx];
    uint16_t pos = 0;
    int change = 0;
    while (pos < LCD_W * LCD_H) {
      uint16_t n = *p++;
      if (n & 0x80) n = ((n & 0x7F) << 8) | *p++;
      if (change)
        for (uint16_t k = pos; k < pos + n; k++) ecran[k >> 3] ^= (1 << (k & 7));
      pos += n;
      change = !change;
    }
    char nom[64];
    snprintf(nom, sizeof nom, "/out/decode/f%03d.pbm", idx);
    FILE * f = fopen(nom, "w");
    fprintf(f, "P1\n%d %d\n", LCD_W, LCD_H);
    for (int i = 0; i < LCD_W * LCD_H; i++) fprintf(f, "%d%c", (ecran[i >> 3] >> (i & 7)) & 1, (i % LCD_W == LCD_W - 1) ? '\n' : ' ');
    fclose(f);
  }
  printf("%d images décodées\n", GABOLABS_ANIM_FRAMES);
  return 0;
}
