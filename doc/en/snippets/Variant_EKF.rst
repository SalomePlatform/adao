.. index::
    single: Variant
    pair: Variant ; EKF
    pair: Variant ; CEKF

Variant
  *Predefined name*. This key allows to choose one of the possible variants for
  the main algorithm. The default variant is the constrained version "CEKF" of
  the original algorithm "EKF", and the possible choices are
  "EKF" (Extended Kalman Filter),
  "CEKF" (Constrained Extended Kalman Filter).
  It is highly recommended to keep the default value.

  Example :
  ``{"Variant":"CEKF"}``
