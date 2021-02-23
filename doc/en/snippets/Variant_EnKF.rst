.. index::
    single: Variant
    pair: Variant ; EnKF
    pair: Variant ; ETKF
    pair: Variant ; ETKF-N
    pair: Variant ; MLEF
    pair: Variant ; IEnKF

Variant
  *Predifined name*.  This key allows to choose one of the possible variants
  for the main algorithm. The default variant is the original "EnKF", and the
  possible ones are
  "EnKF" (Ensemble Kalman Filter),
  "ETKF" (Ensemble-Transform Kalman Filter),
  "ETKF-N" (Ensemble-Transform Kalman Filter),
  "MLEF" (Maximum Likelihood Kalman Filter),
  "IEnKF" (Iterative_EnKF).
  One recommends to try the "ETKF-N" or "IEnKF" variants, and to reduce the
  number of members to about 10 or less for all variants other then the
  original "EnKF".

  Example :
  ``{"Variant":"EnKF"}``
