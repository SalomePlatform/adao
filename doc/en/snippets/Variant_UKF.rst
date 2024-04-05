.. index::
    single: Variant
    pair: Variant ; UKF
    pair: Variant ; CUKF
    pair: Variant ; 2UKF
    pair: Variant ; S3F
    pair: Variant ; CS3F

Variant
  *Predefined name*. This key allows to choose one of the possible variants for
  the main algorithm. The default variant is the constrained version
  "CUKF/2UKF" of the original algorithm "UKF", and the possible choices are
  "UKF" (Unscented Kalman Filter),
  "CUKF" ou "2UKF" (Constrained Unscented Kalman Filter),
  "S3F" (Scaled Spherical Simplex Filter),
  "CS3F" (Constrained Scaled Spherical Simplex Filter).
  It is highly recommended to keep the default value.

  Example :
  ``{"Variant":"2UKF"}``
