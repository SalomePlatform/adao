.. index::
    single: Variant
    pair: Variant ; UKF
    pair: Variant ; CUKF
    pair: Variant ; 2UKF
    pair: Variant ; S3F
    pair: Variant ; CS3F

Variant
  *Nom prédéfini*. Cette clé permet de choisir l'une des variantes possibles
  pour l'algorithme principal. La variante par défaut est la version contrainte
  "CUKF/2UKF" de l'algorithme original "UKF", et les choix possibles sont
  "UKF" (Unscented Kalman Filter),
  "CUKF" ou "2UKF" (Constrained Unscented Kalman Filter),
  "S3F" (Scaled Spherical Simplex Filter),
  "CS3F" (Constrained Scaled Spherical Simplex Filter).
  Il est fortement recommandé de conserver la valeur par défaut.

  Exemple :
  ``{"Variant":"2UKF"}``
