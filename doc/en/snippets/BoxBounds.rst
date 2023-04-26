.. index:: single: BoxBounds

BoxBounds
  *List of pairs of real values*. This key allows to define pairs of upper and
  lower bounds for *increments* on every state variable being optimized (and
  not on state variables themselves, whose bounds can be indicated by the
  "*Bounds*" variable). Increment bounds have to be given by a list of list of
  pairs of lower/upper bounds for each increment on variable, with a value of
  ``None`` each time there is no bound. This key is only required if there are
  no variable bounds, and there are no default values.

  Example :
  ``{"BoxBounds":[[-0.5,0.5], [0.01,2.], [0.,None], [None,None]]}``
