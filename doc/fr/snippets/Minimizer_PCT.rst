.. index::
    single: Minimizer
    pair: Minimizer ; LBFGSB
    pair: Minimizer ; BFGS
    pair: Minimizer ; BOBYQA
    pair: Minimizer ; COBYLA
    pair: Minimizer ; NEWUOA
    pair: Minimizer ; POWELL
    pair: Minimizer ; SIMPLEX
    pair: Minimizer ; SUBPLEX

Minimizer
  *Nom prédéfini*. Cette clé permet de changer le minimiseur pour l'optimiseur.
  Le choix par défaut est "LBFGSB", et les choix possibles sont les suivants
  **pour les variants variationnels**
  "LBFGSB"  (minimisation non linéaire sous contraintes, voir [Byrd95]_, [Morales11]_, [Zhu97]_),
  "BFGS" (minimisation non linéaire sans contraintes),
  et les suivants **pour les variants sans dérivation**
  "BOBYQA" (minimisation, avec ou sans contraintes, par approximation quadratique, voir [Powell09]_),
  "COBYLA" (minimisation, avec ou sans contraintes, par approximation linéaire, voir [Powell94]_ [Powell98]_).
  "NEWUOA" (minimisation, avec ou sans contraintes, par approximation quadratique itérative, voir [Powell04]_),
  "POWELL" (minimisation, sans contraintes, de type directions conjuguées, voir [Powell64]_),
  "SIMPLEX" (minimisation, avec ou sans contraintes, de type Nelder-Mead utilisant le concept de simplexe, voir [Nelder65]_ et [WikipediaNM]_),
  "SUBPLEX" (minimisation, avec ou sans contraintes, de type Nelder-Mead utilisant le concept de simplexe sur une suite de sous-espaces, voir [Rowan90]_).
  Seul le minimiseur "POWELL" ne permet pas de traiter les contraintes de
  bornes, tous les autres en tiennent compte si elles sont présentes dans la
  définition du cas.

  Exemple :
  ``{"Minimizer":"LBFGSB"}``
