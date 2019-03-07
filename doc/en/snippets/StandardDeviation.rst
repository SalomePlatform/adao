.. index:: single: StandardDeviation

StandardDeviation
  This key indicates, only in the case of a "Gaussian" distribution type asked
  through the keyword "*NoiseDistribution*", the standard deviation of the
  state Gaussian perturbations for each state component. The default is an
  empty list, this key must therefore be filled in in the case of a "Gaussian"
  distribution. A simple way to do this is to give a list of the length of the
  desired state with identical standard deviations, as in the example below
  with standard deviations of 5%. It is recommended to take standard deviations
  of a few percent maximum.

  Example :
  ``{"StandardDeviation":<longueur de l'état>*[0.05]}``
