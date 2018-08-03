.. index:: single: Minimizer

Minimizer
  This key allows to choose the optimization minimizer. The default choice is
  "BOBYQA", and the possible ones are
  "BOBYQA" (minimization with or without constraints by quadratic approximation [Powell09]_),
  "COBYLA" (minimization with or without constraints by linear approximation [Powell94]_ [Powell98]_).
  "NEWUOA" (minimization with or without constraints by iterative quadratic approximation [Powell04]_),
  "POWELL" (minimization unconstrained using conjugate directions [Powell64]_),
  "SIMPLEX" (minimization with or without constraints using Nelder-Mead simplex algorithm [Nelder65]_),
  "SUBPLEX" (minimization with or without constraints using Nelder-Mead on a sequence of subspaces [Rowan90]_).
  Remark: the "POWELL" method perform a dual outer/inner loops optimization,
  leading then to less control on the cost function evaluation number because
  it is the outer loop limit than is controlled. If precise control on this
  cost function evaluation number is required, choose an another minimizer.

  Example:
  ``{"Minimizer":"BOBYQA"}``
