.. index:: single: SimulationQuantiles

SimulationQuantiles
  *List of vector series*. Each element is a series of observation column
  vectors, corresponding, for a particular quantile required by the user, to
  the observed state that achieves the requested quantile. Each observation
  column vector is rendered in the same order as the quantile values required
  by the user.

  Example:
  ``sQuantiles = ADD.get("SimulationQuantiles")[:]``
