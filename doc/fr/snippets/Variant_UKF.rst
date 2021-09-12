.. index::
    single: Variant
    pair: Variant ; UKF
    pair: Variant ; CUKF

Variant
  *Nom prédéfini*. Cette clé permet de choisir l'une des variantes possibles
  pour l'algorithme principal. La variante par défaut est la version contrainte
  "CUKF" de l'algorithme original "UKF", et les choix possibles sont
  "UKF" (Unscented Kalman Filter),
  "CUKF" (Constrained Unscented Kalman Filter).

  Exemple :
  ``{"Variant":"CUKF"}``
