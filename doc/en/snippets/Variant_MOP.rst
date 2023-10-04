.. index::
    single: Variant
    pair: Variant ; EIM
    pair: Variant ; DEIM
    pair: Variant ; lcEIM
    pair: Variant ; lcDEIM
    pair: Variant ; PositioningByEIM
    pair: Variant ; PositioningByDEIM
    pair: Variant ; PositioningBylcEIM
    pair: Variant ; PositioningBylcDEIM

Variant
  *Predefined name*.  This key allows to choose one of the possible variants
  for the optimal positioning search. The default variant is the constrained by
  excluded locations "lcEIM" or "PositioningBylcEIM", and the possible choices
  are "EIM" or "PositioningByEIM" (using the original EIM algorithm), "lcEIM"
  or "PositioningBylcEIM" (using the constrained by excluded locations EIM,
  named "Location Constrained EIM"), "DEIM" or "PositioningByDEIM" (using the
  original DEIM algorithm), "lcDEIM" or "PositioningBylcDEIM" (using the
  constrained by excluded locations DEIM, named "Location Constrained DEIM").
  It is highly recommended to keep the default value.

  Example :
  ``{"Variant":"lcEIM"}``
