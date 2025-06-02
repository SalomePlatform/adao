.. index::
    single: Minimizer
    pair: Minimizer ; LBFGSB
    pair: Minimizer ; BFGS
    pair: Minimizer ; BOBYQA
    pair: Minimizer ; COBYLA
    pair: Minimizer ; NEWUOA
    pair: Minimizer ; POWELL
    pair: Minimizer ; SIMPLEX
    pair: Minimizer ; SUBPLEX

Minimizer
  *Predefined name*. This key allows to choose the optimization minimizer. The
  default choice is "LBFGSB", and the possible ones **for variational
  variants** are
  "LBFGSB" (nonlinear constrained minimizer, see [Byrd95]_, [Morales11]_, [Zhu97]_),
  "BFGS" (nonlinear unconstrained minimizer),
  and the following ones **for variants without derivation** are
  "BOBYQA" (minimization, with or without constraints, by quadratic approximation, see [Powell09]_),
  "COBYLA" (minimization, with or without constraints, by linear approximation, see [Powell94]_ [Powell98]_).
  "NEWUOA" (minimization, with or without constraints, by iterative quadratic approximation, see [Powell04]_),
  "POWELL" (minimization, unconstrained, using conjugate directions, see [Powell64]_),
  "SIMPLEX" (minimization, with or without constraints, using Nelder-Mead simplex algorithm, see [Nelder65]_ and [WikipediaNM]_),
  "SUBPLEX" (minimization, with or without constraints, using Nelder-Mead simplex algorithm on a sequence of subspaces, see [Rowan90]_).
  Only the "POWELL" minimizer does not allow to deal with boundary constraints,
  all the others take them into account if they are present in the case
  definition.

  Example :
  ``{"Minimizer":"LBFGSB"}``
