.. index:: single: StateBoundsForQuantiles

StateBoundsForQuantiles
  *List of pairs of real values*. This key allows to define pairs of upper and
  lower bounds for every state variable used for quantile simulations. Bounds
  have to be given by a list of list of pairs of lower/upper bounds for each
  variable, with possibly ``None`` every time there is no bound.

  If these bounds are not defined for quantile simulation and if optimization
  bounds are defined, they are used for quantile simulation. If these bounds
  for quantile simulation are defined, they are used regardless of the
  optimization bounds defined. If this variable is set to ``None``, then no
  bounds are used for the states used in the quantile simulation regardless of
  the optimization bounds defined.

  Example :
  ``{"StateBoundsForQuantiles":[[2.,5.],[1.e-2,10.],[-30.,None],[None,None]]}``
