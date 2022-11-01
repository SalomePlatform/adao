.. index:: single: QualityCriterion

QualityCriterion
  *Predefined name*. This key indicates the quality criterion, minimized to
  find the optimal state estimate. The default is the usual data assimilation
  criterion named "DA", the augmented weighted least squares. The possible
  criteria has to be in the following list, where the equivalent names are
  indicated by the sign "<=>":
  ["AugmentedWeightedLeastSquares" <=> "AWLS" <=> "DA",
  "WeightedLeastSquares" <=> "WLS", "LeastSquares" <=> "LS" <=> "L2",
  "AbsoluteValue" <=> "L1", "MaximumError" <=> "ME" <=> "Linf"].

  Example:
  ``{"QualityCriterion":"DA"}``
