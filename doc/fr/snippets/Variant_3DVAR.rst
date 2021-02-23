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
  "3DVAR" (3D Variational analysis, voir [Lorenc86]_, [LeDimet86]_, [Talagrand97]_),
  "3DVAR-VAN" (3D Variational Analysis with No inversion of B, voir [Lorenc88]_),
  "3DVAR-Incr" (Incremental 3DVAR, voir [Courtier94]_),
  "3DVAR-PSAS" (Physical-space Statistical Analysis Scheme for 3DVAR, voir [Cohn98]_),
  Il est fortement conseillé de conserver la valeur par défaut.

  Exemple :
  ``{"Variant":"3DVAR"}``
