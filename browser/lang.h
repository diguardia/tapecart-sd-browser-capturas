/*
 * lang.h - textos de pantalla / on-screen texts
 *
 * Compilar con -DLANG_EN para ingles; por defecto, espanol.
 * Build with -DLANG_EN for English; Spanish is the default.
 *
 * Los textos van en minusculas: el browser usa el juego de caracteres
 * de minusculas, donde las mayusculas del codigo fuente se ven como mayusculas.
 * Lines must fit in 40 columns.
 */
#ifndef LANG_H_
#define LANG_H_

#ifdef LANG_EN

#define S_TITLE        "tapecart sd browser + screenshots v2.0"
#define S_BY           "by "
#define S_FORK_BY      "fork by "
#define S_FORK_OF      "fork of tapecart sd browser v1.4-tap"
#define S_FORK_AUTHORS "(rainisto, kim jorgensen, ingo korb)"
#define S_PRESS_DOT    "press . for credits and help"
#define S_SHOTS_DATA   "screenshots, data: gamebase64 (gb64.com)"
#define S_PERSONAL     "for personal use only"
#define S_K_RET        "ret  play / open folder"
#define S_K_SPC        "spc  show screenshot"
#define S_K_DEL        "del  parent folder"
#define S_K_HOME       "home root folder"
#define S_K_CRSR       "crsr up/down, left/right = page"
#define S_K_TB         "t/b  top / bottom"
#define S_K_Q          "q    quit"
#define S_NOWARRANTY   "no warranty. use at your own risk."
#define S_READING      " reading...                             "
#define S_LOADING_SHOT " loading screenshot...                  "
#define S_SHOT_TAG     " [shot]"
#define S_HELP_SHOTS   "ret play  spc shot  del back  home root"
#define S_HELP_PLAIN   "ret play/open   del back   home root   "
#define S_ERR_JOY      "error: joystick driver"
#define S_ERR_TC       "error: tapecart not detected."
#define S_GENRES       "", "Arcade", "Shoot'em up", "Adventure", "Puzzle", "Educational", \
                       "Sports", "Strategy", "Gambling", "Board game", "Cards", "Racing", \
                       "Simulation", "Misc"

#else

#define S_TITLE        "tapecart sd browser con capturas v2.0"
#define S_BY           "por "
#define S_FORK_BY      "fork por "
#define S_FORK_OF      "fork de tapecart sd browser v1.4-tap"
#define S_FORK_AUTHORS "(rainisto, kim jorgensen, ingo korb)"
#define S_PRESS_DOT    "tecla . para creditos y ayuda"
#define S_SHOTS_DATA   "capturas y datos: gamebase64 (gb64.com)"
#define S_PERSONAL     "solo para uso personal"
#define S_K_RET        "ret  jugar / abrir carpeta"
#define S_K_SPC        "spc  ver captura"
#define S_K_DEL        "del  carpeta anterior"
#define S_K_HOME       "home carpeta raiz"
#define S_K_CRSR       "crsr arriba/abajo, izq/der = pagina"
#define S_K_TB         "t/b  principio / final"
#define S_K_Q          "q    salir"
#define S_NOWARRANTY   "sin garantia. use bajo su riesgo."
#define S_READING      " leyendo...                             "
#define S_LOADING_SHOT " cargando foto...                       "
#define S_SHOT_TAG     " [foto]"
#define S_HELP_SHOTS   "ret jugar spc foto del atras home raiz"
#define S_HELP_PLAIN   "ret jugar/abrir  del atras  home raiz  "
#define S_ERR_JOY      "error: joystick"
#define S_ERR_TC       "error: no se detecta el tapecart."
#define S_GENRES       "", "Arcade", "Shoot'em up", "Aventura", "Ingenio", "Educativo", \
                       "Deportes", "Estrategia", "Azar", "Tablero", "Cartas", "Carreras", \
                       "Simulador", "Varios"

#endif

#endif /* LANG_H_ */
