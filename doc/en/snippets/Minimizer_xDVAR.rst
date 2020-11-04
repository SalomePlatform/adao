  .. index:: single: Minimizer

Minimizer
  *Predefined name*. This key allows to choose the optimization minimizer. The
  default choice is "LBFGSB", and the possible ones are
  "LBFGSB" (nonlinear constrained minimizer, see [Byrd95]_, [Morales11]_ and [Zhu97]_),
  "TNC" (nonlinear constrained minimizer),
  "CG" (nonlinear unconstrained minimizer),
  "BFGS" (nonlinear unconstrained minimizer),
  "NCG" (Newton CG minimizer).
  It is strongly recommended to stay with the default.

  Example :
  ``{"Minimizer":"LBFGSB"}``

