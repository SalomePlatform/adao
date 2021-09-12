.. index::
    single: Variant
    pair: Variant ; UKF
    pair: Variant ; CUKF

Variant
  *Predifined name*. This key allows to choose one of the possible variants for
  the main algorithm. The default variant is the constrained version "CUKF" of
  the original algorithm "UKF", and the possible choices are
  "UKF" (Unscented Kalman Filter),
  "CUKF" (Constrained Unscented Kalman Filter).

  Example :
  ``{"Variant":"CUKF"}``
