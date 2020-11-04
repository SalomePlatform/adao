.. index:: single: BoxBounds

BoxBounds
  *List of pairs of real values*. This key allows to define upper and lower
  bounds for *increments* on every state variable being optimized (and not on
  state variables themselves). Bounds have to be given by a list of list of
  pairs of lower/upper bounds for each increment on variable, with extreme
  values every time there is no bound (``None`` is not allowed when there is no
  bound). This key is required and there is no default values.

  Example :
  ``{"BoxBounds":[[-0.5,0.5], [0.01,2.], [0.,1.e99], [-1.e99,1.e99]]}``
