.. index::
    single: Minimizer
    pair: Minimizer ; LBFGSB
    pair: Minimizer ; TNC
    pair: Minimizer ; CG
    pair: Minimizer ; BFGS
    pair: Minimizer ; NCG

Minimizer
  *Nom prédéfini*. Cette clé permet de changer le minimiseur pour l'optimiseur.
  Le choix par défaut est "LBFGSB", et les choix possibles sont
  "LBFGSB" (minimisation non linéaire sous contraintes, voir [Byrd95]_, [Morales11]_, [Zhu97]_),
  "TNC" (minimisation non linéaire sous contraintes),
  "CG" (minimisation non linéaire sans contraintes),
  "BFGS" (minimisation non linéaire sans contraintes),
  "NCG" (minimisation de type gradient conjugué de Newton).
  Il est fortement conseillé de conserver la valeur par défaut.

  Exemple :
  ``{"Minimizer":"LBFGSB"}``
