.. index::
    single: Minimizer
    pair: Minimizer ; LBFGSB
    pair: Minimizer ; TNC
    pair: Minimizer ; CG
    pair: Minimizer ; BFGS

..    pair: Minimizer ; NCG

Minimizer
  *Predefined name*. This key allows to choose the optimization minimizer. The
  default choice is "LBFGSB", and the possible ones are
  "LBFGSB" (nonlinear constrained minimizer, see [Byrd95]_, [Morales11]_, [Zhu97]_),
  "TNC" (nonlinear constrained minimizer),
  "CG" (nonlinear unconstrained minimizer),
  "BFGS" (nonlinear unconstrained minimizer),
  It is strongly recommended to stay with the default.

..  "NCG" (Newton CG minimizer).

  Example :
  ``{"Minimizer":"LBFGSB"}``
