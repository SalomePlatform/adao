.. index:: single: Minimizer

Minimizer
  *Nom prédéfini*. Cette clé permet de changer la stratégie de minimisation
  pour l'optimiseur. Le choix par défaut est "BEST1BIN", et les choix possibles
  sont les multiples variables pour les stratégies de croisement et mutation,
  décrites par les clés
  "BEST1BIN",
  "BEST1EXP",
  "RAND1EXP",
  "RANDTOBEST1EXP",
  "BEST2EXP",
  "RAND2EXP",
  "RANDTOBEST1BIN",
  "BEST2BIN",
  "RAND2BIN",
  "RAND1BIN".
  Il est fortement conseillé de conserver la valeur par défaut.

  Exemple :
  ``{"Minimizer":"BEST1BIN"}``
