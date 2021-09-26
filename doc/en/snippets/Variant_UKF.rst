.. index::
    single: Variant
    pair: Variant ; UKF
    pair: Variant ; 2UKF

Variant
  *Predifined name*. This key allows to choose one of the possible variants for
  the main algorithm. The default variant is the constrained version "2UKF" of
  the original algorithm "UKF", and the possible choices are
  "UKF" (Unscented Kalman Filter),
  "2UKF" (Constrained Unscented Kalman Filter).

  Example :
  ``{"Variant":"2UKF"}``
