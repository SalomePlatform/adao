.. index::
    single: Minimizer
    pair: Minimizer ; BOBYQA
    pair: Minimizer ; COBYLA
    pair: Minimizer ; NEWUOA
    pair: Minimizer ; POWELL
    pair: Minimizer ; SIMPLEX
    pair: Minimizer ; SUBPLEX

Minimizer
  *Nom prédéfini*. Cette clé permet de changer le minimiseur pour l'optimiseur.
  Le choix par défaut est "BOBYQA", et les choix possibles sont
  "BOBYQA" (minimisation avec ou sans contraintes par approximation quadratique, voir [Powell09]_),
  "COBYLA" (minimisation avec ou sans contraintes par approximation linéaire, voir [Powell94]_ [Powell98]_).
  "NEWUOA" (minimisation avec ou sans contraintes par approximation quadratique itérative, voir [Powell04]_),
  "POWELL" (minimisation sans contraintes de type directions conjuguées, voir [Powell64]_),
  "SIMPLEX" (minimisation avec ou sans contraintes de type simplexe ou Nelder-Mead, voir [Nelder65]_),
  "SUBPLEX" (minimisation avec ou sans contraintes de type simplexe sur une suite de sous-espaces, voir [Rowan90]_).
  Remarque : la méthode "POWELL" effectue une optimisation par boucles
  imbriquées interne/externe, conduisant ainsi à un contrôle relaché du nombre
  d'évaluations de la fonctionnelle à optimiser. Si un contrôle précis du
  nombre d'évaluations est requis, il faut choisir un autre minimiseur.

  Exemple :
  ``{"Minimizer":"BOBYQA"}``
