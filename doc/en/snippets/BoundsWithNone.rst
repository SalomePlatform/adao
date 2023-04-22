.. index:: single: Bounds

Bounds
  *List of pairs of real values*. This key allows to define pairs of upper and
  lower bounds for every state variable being optimized. Bounds have to be
  given by a list of list of pairs of lower/upper bounds for each variable,
  with a value of ``None`` each time there is no bound. The bounds can always
  be specified, but they are taken into account only by the constrained
  optimizers.

  Example:
  ``{"Bounds":[[2.,5.],[1.e-2,10.],[-30.,None],[None,None]]}``
