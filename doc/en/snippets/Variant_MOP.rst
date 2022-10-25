.. index::
    single: Variant
    pair: Variant ; PositioningByEIM
    pair: Variant ; PositioningBylcEIM

Variant
  *Predefined name*.  This key allows to choose one of the possible variants
  for the optimal positioning search. The default variant is the constrained by
  excluded locations "PositioningBylcEIM", and the possible choices are
  "PositioningByEIM" (using the original EIM algorithm),
  "PositioningBylcEIM" (using the constrained by excluded locations EIM, named "Location Constrained EIM").
  It is highly recommended to keep the default value.

  Example :
  ``{"Variant":"PositioningBylcEIM"}``
