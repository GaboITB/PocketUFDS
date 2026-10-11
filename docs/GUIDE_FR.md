# PocketUFDS : la RadioMaster Pocket prête pour Ukrainian Fight Drone Simulator

Pack gratuit de GaboLabs. Il transforme une **RadioMaster Pocket** en radiocommande prête à voler pour
**Ukrainian Fight Drone Simulator (UFDS)**, en une quinzaine de minutes :

- un **modèle radio UFDS** : les 10 actions du jeu sur la radio, sans clavier,
- des **packs de voix de qualité** en **ukrainien, anglais et français** (alertes et annonces de vol),
- en option, un **écran de démarrage animé**, avec bande-son et jeu de lumière (version EdgeTX maison).

> **Testé sur :** RadioMaster Pocket (ELRS), EdgeTX 2.12.4, UFDS sous Windows 11. Les autres radios ne sont pas prises en charge.

---

## 1. Avant de commencer

| Il te faut | Pourquoi |
|---|---|
| Une RadioMaster Pocket en **EdgeTX 2.12.x** | version plus ancienne (2.10, 2.11) ? L'installateur prépare pour toi la mise à jour officielle vers EdgeTX 2.12.4 et t'explique comment la flasher |
| Un câble USB-C de données | pour accéder à la carte SD de la radio |
| Un PC Windows avec UFDS | pour le réglage du jeu |

**Sécurité :** l'installateur fait une **sauvegarde complète de ta carte SD** avant toute modification
(dans ton dossier Documents : `PocketUFDS_backup_<date>`). Il n'écrase jamais tes modèles existants
et garde ta calibration des manches.

---

## 2. Installer le pack (installateur)

1. Branche la radio avec un câble USB-C de données, allume-la et choisis **USB Storage** sur son écran.
2. Lance `PocketUFDS-Installer.exe`. Si Windows affiche *Windows a protégé votre ordinateur*, clique sur
   **Informations complémentaires**, puis **Exécuter quand même** (l'installateur est gratuit et non signé).
3. Choisis la langue (Entrée = celle de Windows), puis **1. Installer**. L'installateur trouve la radio tout seul.
4. Réponds à la question sur l'écran de démarrage animé (1 = oui, 2 = non), relis le résumé, tape `Y` puis Entrée.
5. Une barre montre l'avancement de chaque étape. Ne débranche pas la radio avant **Terminé !**, puis éjecte-la
   dans Windows et débranche-la.

**Radio en EdgeTX plus ancien (2.10, 2.11) :** l'installateur prépare la mise à jour officielle vers EdgeTX
2.12.4, incluse dans le pack : sauvegarde complète, contenu officiel EdgeTX de la carte SD, firmware officiel.
Il réécrit aussi la vérification des interrupteurs au démarrage de tes modèles au format 2.12, avec les mêmes
positions : EdgeTX 2.12.4 relit mal l'ancien format (ton modèle d'usine demanderait SB et SE au milieu). Puis il
affiche les étapes du flash (même méthode que la partie 3, avec `OFFICIAL-2.12.4.bin`). Flashe-le, laisse la
radio démarrer une fois, puis relance l'installateur.

Ce que l'installateur modifie sur ta radio :

| Élément | Modification |
|---|---|
| Types d'interrupteurs | SA et SD à 2 positions, SB et SC à 3 positions, SE en bouton à ressort (le réglage d'usine est souvent faux) |
| Audio mute | activé : supprime le grésillement du haut-parleur entre deux sons |
| Langue des voix | celle que tu as choisie |
| Alerte d'inactivité | 10 minutes (si elle était plus longue) |
| Modèles | ajout du modèle **UFDS** sur le premier emplacement libre |

---

## 3. En option : flasher le firmware animé

Seulement si tu as répondu **1 (oui)** à la question sur l'écran de démarrage. Deux firmwares sont maintenant dans le dossier `FIRMWARE` de la radio :

| Fichier | Ce que c'est |
|---|---|
| `GABOLABS-2.12.4.bin` | EdgeTX 2.12.4, avec écran de démarrage animé, bande-son et jeu de lumière |
| `OFFICIAL-2.12.4.bin` | EdgeTX 2.12.4 officiel, pour revenir en arrière à tout moment |

1. **Éteins** la radio.
2. Les **trims** sont les deux mini-joysticks de chaque côté du bouton d'allumage. Pousse-les tous les deux
   **vers le bouton d'allumage** (vers le centre) et maintiens-les, puis, sans les relâcher, appuie sur **le bouton d'allumage** et maintiens-le
   jusqu'à ce que l'écran s'allume : le bootloader s'ouvre (menu noir et blanc). Relâche les trims.
3. Tourne la molette jusqu'à **Write Firmware**, appuie sur la molette, choisis `GABOLABS-2.12.4.bin`, appuie
   sur la molette, puis **garde-la enfoncée** jusqu'à voir `Writing...`.
4. Attends `Writing complete`, appuie sur la molette, choisis **Exit**, appuie sur la molette. Si un avertissement
   s'affiche, fais ce qu'il demande. Ne touche pas aux manches pendant le premier démarrage.

**Ce que la version maison retire pour tenir dans les 512 Ko de mémoire de la Pocket :** le menu
hélicoptère, et la prise en charge des modules externes FrSky (PXX1) et ImmersionRC Ghost. Le module
ELRS interne, la manette USB, Lua et les voix ne sont pas touchés. Le correctif du code source est
publié avec le pack (licence GPL v2, comme EdgeTX).

Pendant l'animation de démarrage, **n'importe quelle touche la passe** (le son et la lumière
s'arrêtent aussi). Les manches et les interrupteurs, eux, ne l'interrompent pas.

---

## 4. Sélectionner le modèle et préparer la radio

1. Allume la radio. Appui long sur **MDL**, puis sélectionne **UFDS**.
2. Conseillé une fois : **SYS, Hardware, Calibration** (les manches ET la molette arrière S1, sur toute leur course).
3. Branche la radio au PC et choisis **USB Joystick**.

---

## 5. Régler le jeu

Dans UFDS : **Paramètres, Contrôles**, choisis **EdgeTX Radiomaster Pocket Joystick** dans la liste,
puis règle chaque action :

| Action du jeu | Associer | Commande de la radio |
|---|---|---|
| Accélérateur | Axis 3 | manche gauche, vertical |
| Lacet | Axis 4 | manche gauche, horizontal |
| Tangage | Axis 2 | manche droit, vertical |
| Roulis | Axis 1 | manche droit, horizontal |
| Arm./Désarm. | Axis 5 | **SD** (droite, à l'extérieur) |
| Mode de vol | Axis 6 | **SB** (gauche, 3 positions) |
| Puissance VTX | Axis 8 | **SC** (droite, 3 positions) |
| Caméra servo | Axis 7 | **S1** (molette arrière, à droite) |
| Bombe | Button 1 | **SE** (bouton) |
| Armer la bombe | Button 2 | **SA** (gauche, à l'extérieur, juste devant SE) |

> Les axes 7 et 8 sont inversés par rapport aux voies de la radio : c'est normal (ordre de Windows).

**Profil réaliste** (comme les pilotes FPV) : dans les lignes des manches, mets **Zone morte 0,005 et
Exposant 0,20** pour le roulis et le tangage, **0,01 et 0,15** pour le lacet, **0 et 0** pour
l'accélérateur. Joue en **plein écran**.

**Les modes de vol sur SB** dépendent du drone. Sur les drones FPV, SB en haut ou au milieu donne ACRO,
en bas STAB. Sur les gros bombardiers, en haut STAB, au milieu ALTH (maintien d'altitude), en bas LOIT
(maintien de position).

---

## 6. Annonces vocales (modèle UFDS)

| Commande | Annonce |
|---|---|
| SA | bombe armée / bombe sécurisée |
| SB | mode de vol un / deux / trois |
| SC | vidéo, puissance basse / moyenne / haute |
| SD | armé / désarmé |
| SE | largage |

Une **minuterie de vol silencieuse (VOL)** tourne quand le drone est armé (SD). À l'allumage, tous les interrupteurs
doivent être **vers l'avant, loin de toi** : SD désarmé, SA bombe sécurisée, SB en mode de vol un, SC en vidéo basse
puissance, ainsi que les gaz en bas.

**Pourquoi cette disposition :** la sécurité de la bombe (SA) et le bouton de largage (SE) sont sous le même
doigt, comme la sûreté et la détente d'une arme. L'armement des moteurs (SD) est de l'autre côté : en
cherchant SE en vol, tu ne peux pas couper les moteurs par erreur.

**Tu préfères une autre disposition ?** Change-la dans la radio, pas dans le jeu : MDL, page MIXES, change la
source des lignes de voies (CH5 = armement, CH10 = armer la bombe). Les annonces vocales et la minuterie
suivent les voies, elles restent justes. N'échange que des interrupteurs du même type : SA avec SD
(2 positions), SB avec SC (3 positions).

**Un modèle par jeu :** choisis UFDS (appui long sur MDL) avant de jouer à UFDS, et ton modèle habituel
pour les autres jeux. Le modèle UFDS ne change rien à tes autres modèles.

---

## 7. Dépannage

| Problème | Solution |
|---|---|
| Plus aucun son après avoir activé Audio mute | **redémarre la radio** une fois : le réglage s'applique à l'allumage |
| Le jeu utilise le clavier, pas la radio | la radio est en mode USB Storage : rebranche-la et choisis **USB Joystick** |
| La vue caméra « sous le drone » est difficile à atteindre | calibre **S1** (SYS, Hardware, Calibration) |
| Alerte d'interrupteurs au démarrage | pousse **SA, SB, SC et SD** vers l'avant, loin de toi, gaz en bas |
| Bips et vibrations à des moments aléatoires sur le modèle d'usine (POCKET) | la molette arrière S1 est posée pile au milieu, et ce modèle bipe à son centre : tourne S1 vers une butée. Le modèle UFDS ne le fait pas |
| Alerte `SB SE` à l'allumage sur un modèle, après une mise à jour de 2.10 ou 2.11 vers 2.12 faite **toi-même** | EdgeTX 2.12.4 relit mal l'ancien format de vérification des interrupteurs. Appuie sur une touche pour la passer, ou refais la vérification dans ce modèle (MDL, page SETUP, section Pre-start Checks, ligne S-Warning). Une mise à jour préparée par l'installateur l'évite |
| Quelque chose ne va pas | recopie le dossier de sauvegarde de Documents sur la carte SD, ou flashe `OFFICIAL-2.12.4.bin` |

---

## 8. Crédits et licences

- **EdgeTX** (GPL v2) : le correctif du firmware et la procédure de compilation sont fournis.
- **Voix** générées avec ElevenLabs (bibliothèque de voix) : **Yaroslava** (ukrainien), **Nichalia Schwartz**
  (anglais), **Manon** (français), et **Yaroslava** pour « Слава Україні! ». Listes de phrases basées sur
  les listes officielles d'EdgeTX, corrigées et complétées.
- **Armoiries de l'Ukraine** : domaine public (Wikimedia Commons).
- **Les textes ukrainiens** ont été vérifiés par transcription automatique et par deux relecteurs
  automatiques indépendants, mais **pas encore par un locuteur natif**. Signale toute erreur : elle sera corrigée.

Слава Україні ! GaboLabs
