.. index:: single: ResiduFormula

ResiduFormula
  *Predefined name*. This key indicates the residue formula that has to be
  used for the test. The default choice is "CenteredDL", and the possible ones
  are "CenteredDL" (residue of the difference between the function at nominal
  point and the values with positive and negative increments, which has to stay
  very small), "Taylor" (residue of the Taylor development of the operator
  normalized by the nominal value, which has to stay very small),
  "NominalTaylor" (residue of the order 1 approximations of the operator,
  normalized to the nominal point, which has to stay close to 1), and
  "NominalTaylorRMS" (residue of the order 1 approximations of the operator,
  normalized by RMS to the nominal point, which has to stay close to 0).

  Example :
  ``{"ResiduFormula":"CenteredDL"}``
