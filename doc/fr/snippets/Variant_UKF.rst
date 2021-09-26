.. index::
    single: Variant
    pair: Variant ; UKF
    pair: Variant ; 2UKF

Variant
  *Nom prédéfini*. Cette clé permet de choisir l'une des variantes possibles
  pour l'algorithme principal. La variante par défaut est la version contrainte
  "2UKF" de l'algorithme original "UKF", et les choix possibles sont
  "UKF" (Unscented Kalman Filter),
  "2UKF" (Constrained Unscented Kalman Filter).

  Exemple :
  ``{"Variant":"2UKF"}``
