.. index::
    single: Minimizer
    pair: Minimizer ; BEST1BIN",
    pair: Minimizer ; BEST1EXP",
    pair: Minimizer ; RAND1EXP",
    pair: Minimizer ; RANDTOBEST1EXP
    pair: Minimizer ; BEST2EXP
    pair: Minimizer ; RAND2EXP
    pair: Minimizer ; RANDTOBEST1BIN
    pair: Minimizer ; BEST2BIN
    pair: Minimizer ; RAND2BIN
    pair: Minimizer ; RAND1BIN

Minimizer
  *Nom prédéfini*. Cette clé permet de changer la stratégie de minimisation
  pour l'optimiseur. Le choix par défaut est "BEST1BIN", et les choix possibles
  sont les multiples variables pour les stratégies de croisement et mutation,
  décrites par les clés
  "BEST1BIN",
  "BEST1EXP",
  "BEST2BIN",
  "BEST2EXP",
  "RAND1BIN",
  "RAND1EXP",
  "RAND2BIN",
  "RAND2EXP",
  "RANDTOBEST1BIN",
  "RANDTOBEST1EXP".
  Il est fortement conseillé de conserver la valeur par défaut.

  Exemple :
  ``{"Minimizer":"BEST1BIN"}``
