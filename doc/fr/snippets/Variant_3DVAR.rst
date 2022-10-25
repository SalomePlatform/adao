.. index::
    single: Variant
    pair: Variant ; 3DVAR
    pair: Variant ; 3DVAR-VAN
    pair: Variant ; 3DVAR-Incr
    pair: Variant ; 3DVAR-PSAS

Variant
  *Nom prédéfini*. Cette clé permet de choisir l'une des variantes possibles
  pour l'algorithme principal. La variante par défaut est le "3DVAR" d'origine,
  et les choix possibles sont
  "3DVAR" (3D Variational analysis classique),
  "3DVAR-VAN" (3D Variational Analysis with No inversion of B),
  "3DVAR-Incr" (Incremental 3DVAR),
  "3DVAR-PSAS" (Physical-space Statistical Analysis Scheme for 3DVAR),
  Il est fortement recommandé de conserver la valeur par défaut.

  Exemple :
  ``{"Variant":"3DVAR"}``
