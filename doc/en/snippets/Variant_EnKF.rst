.. index::
    single: Variant
    pair: Variant ; EnKF
    pair: Variant ; ETKF
    pair: Variant ; ETKF-N
    pair: Variant ; MLEF
    pair: Variant ; IEnKF
    pair: Variant ; E3DVAR
    pair: Variant ; EnKS

Variant
  *Predefined name*.  This key allows to choose one of the possible variants
  for the main algorithm. The default variant is the original "EnKF"
  formulation, and the possible choices are
  "EnKF" (Ensemble Kalman Filter),
  "ETKF" (Ensemble-Transform Kalman Filter),
  "ETKF-N" (Ensemble-Transform Kalman Filter),
  "MLEF" (Maximum Likelihood Kalman Filter),
  "IEnKF" (Iterative_EnKF),
  "E3DVAR" (EnKF 3DVAR),
  "EnKS" (Ensemble Kalman Smoother).

  One recommends to try the "ETKF-N" or "IEnKF" variants for a robust
  performance, and to reduce the number of members to about 10 or less for all
  variants other than the original "EnKF" formulation.

  Example :
  ``{"Variant":"EnKF"}``
