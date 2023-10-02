Définition d'un ensemble artificiel de champs physiques
-------------------------------------------------------
- Dimension de l'espace des champs physiques...........: 7
- Nombre de vecteurs de champs physiques...............: 7

Recherche des positions optimales de mesure
-------------------------------------------
- Calcul ADAO effectué

Affichage des positions optimales de mesure
-------------------------------------------
- Nombre de positions optimales de mesure..............: 2
- Positions optimales de mesure, numérotées par défaut.: [6 0]

Reconstruction par interpolation d'états mesurés connus
-------------------------------------------------------
- État de référence 1 utilisé pour l'apprentissage.....: [1 2 3 4 5 6 7]
- Positions optimales de mesure, numérotées par défaut.: [6 0]
- Mesures extraites de l'état 1 pour la reconstruction.: [7 1]
- État 1 reconstruit avec la précision de 1%...........: [1. 2. 3. 4. 5. 6. 7.]
  ===> Aucune différence n'existe entre les deux états, comme attendu

Reconstruction par interpolation d'états mesurés non connus
-----------------------------------------------------------
  Illustration d'une interpolation sur mesures réelles non connues
- Positions optimales de mesure, numérotées par défaut.: [6 0]
- Mesures non présentes dans les états connus..........: [4 3]
- État reconstruit avec la précision de 1%.............: [3.    3.167 3.333 3.5   3.667 3.833 4.   ]
  ===> Aux positions de mesure [6 0], le champ reconstruit est égal à la mesure

