.. index:: single: Bounds

Bounds
  *List of pairs of real values*. This key allows to define pairs of upper and
  lower bounds for every state variable being optimized. Bounds have to be
  given by a list of list of pairs of lower/upper bounds for each variable,
  with extreme values every time there is no bound (``None`` is not allowed
  when there is no bound). If the list is empty, there are no bounds.

  Example:
  ``{"Bounds":[[2.,5.],[1.e-2,10.],[-30.,1.e99],[-1.e99,1.e99]]}``
