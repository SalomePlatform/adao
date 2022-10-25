.. index::
    single: Variant
    pair: Variant ; 3DVAR
    pair: Variant ; 3DVAR-VAN
    pair: Variant ; 3DVAR-Incr
    pair: Variant ; 3DVAR-PSAS

Variant
  *Predefined name*.  This key allows to choose one of the possible variants
  for the main algorithm. The default variant is the original "3DVAR", and the
  possible choices are
  "3DVAR" (Classical 3D Variational analysis),
  "3DVAR-VAN" (3D Variational Analysis with No inversion of B),
  "3DVAR-Incr" (Incremental 3DVAR),
  "3DVAR-PSAS" (Physical-space Statistical Analysis Scheme for 3DVAR),
  It is highly recommended to keep the default value.

  Example :
  ``{"Variant":"3DVAR"}``
