.. index::
    single: Variant
    pair: Variant ; EKF
    pair: Variant ; CEKF

Variant
  *Nom prédéfini*. Cette clé permet de choisir l'une des variantes possibles
  pour l'algorithme principal. La variante par défaut est la version contrainte
  "CEKF" de l'algorithme original "EKF", et les choix possibles sont
  "EKF" (Extended Kalman Filter),
  "CEKF" (Constrained Extended Kalman Filter).
  Il est fortement recommandé de conserver la valeur par défaut.

  Exemple :
  ``{"Variant":"CEKF"}``
