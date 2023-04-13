.. index::
    single: Minimizer
    pair: Minimizer ; BOBYQA
    pair: Minimizer ; COBYLA
    pair: Minimizer ; NEWUOA
    pair: Minimizer ; POWELL
    pair: Minimizer ; SIMPLEX
    pair: Minimizer ; SUBPLEX

Minimizer
  *Predefined name*. This key allows to choose the optimization minimizer. The
  default choice is "BOBYQA", and the possible ones are
  "BOBYQA" (minimization, with or without constraints, by quadratic approximation, see [Powell09]_),
  "COBYLA" (minimization, with or without constraints, by linear approximation, see [Powell94]_ [Powell98]_).
  "NEWUOA" (minimization, with or without constraints, by iterative quadratic approximation, see [Powell04]_),
  "POWELL" (minimization, unconstrained, using conjugate directions, see [Powell64]_),
  "SIMPLEX" (minimization, with or without constraints, using Nelder-Mead simplex algorithm, see [Nelder65]_),
  "SUBPLEX" (minimization, with or without constraints, using Nelder-Mead on a sequence of subspaces, see [Rowan90]_).
  Only the "POWELL" minimizer does not allow to deal with boundary constraints,
  all the others take them into account if they are present in the case
  definition.

  Remark: the "POWELL" method perform a dual outer/inner loops optimization,
  leading then to less control on the cost function evaluation number because
  it is the outer loop limit than is controlled. If precise control on the
  evaluation number is required, choose an another minimizer.

  Example:
  ``{"Minimizer":"BOBYQA"}``
