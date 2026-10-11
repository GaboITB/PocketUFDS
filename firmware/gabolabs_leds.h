// Jeu de lumière de l'animation GaboLabs, LED du bouton d'alimentation (Pocket).
// Couleur : bit 0 rouge, bit 1 vert, bit 2 bleu. Temps en pas de 10 ms depuis le début de l'animation.
// Chaque plage alterne couleur A / couleur B toutes les « periode » (0 = couleur A fixe).
#pragma once

#define GL_OFF 0
#define GL_R 1
#define GL_G 2
#define GL_J 3  // jaune = rouge + vert
#define GL_B 4
#define GL_W 7  // blanc = les trois

struct GabolabsLedPlage {
  uint16_t debut;
  uint8_t a, b, periode;
};

static const GabolabsLedPlage gabolabs_leds[] = {
  {0, GL_B, GL_B, 0},      // GABOLABS s'écrit : bleu
  {106, GL_G, GL_G, 0},    // le personnage marche : vert
  {244, GL_W, GL_OFF, 6},  // dissolution : scintillement blanc
  {335, GL_R, GL_G, 25},   // le drone : feux de navigation rouge / vert
  {535, GL_W, GL_OFF, 5},  // largage, la bombe tombe : blanc rapide
  {577, GL_R, GL_J, 6},    // explosion : flashs rouge / jaune
  {650, GL_R, GL_OFF, 13}, // tête de mort et rire : rouge qui pulse
  {814, GL_W, GL_OFF, 6},  // dissolution : scintillement blanc
  {912, GL_B, GL_J, 50},   // СЛАВА УКРАЇНІ : bleu / jaune, couleurs de l'Ukraine
};
