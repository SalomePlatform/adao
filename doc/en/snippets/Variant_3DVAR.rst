.. index::
    single: Variant
    pair: Variant ; 3DVAR
    pair: Variant ; 3DVAR-VAN
    pair: Variant ; 3DVAR-Incr
    pair: Variant ; 3DVAR-PSAS

Variant
  *Predifined name*.  This key allows to choose one of the possible variants
  for the main algorithm. The default variant is the original "3DVAR", and the
  possible ones are
  "3DVAR" (3D Variational analysis, see [Lorenc86]_, [LeDimet86]_, [Talagrand97]_),
  "3DVAR-VAN" (3D Variational Analysis with No inversion of B, see [Lorenc88]_),
  "3DVAR-Incr" (Incremental 3DVAR, see [Courtier94]_),
  "3DVAR-PSAS" (Physical-space Statistical Analysis Scheme for 3DVAR, see [Cohn98]_),
  It is highly recommended to keep the default value.

  Exemple :
  ``{"Variant":"3DVAR"}``
