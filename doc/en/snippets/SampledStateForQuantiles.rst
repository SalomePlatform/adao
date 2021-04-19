.. index:: single: SampledStateForQuantiles

SampledStateForQuantiles
  *List of vector series*. Each element is a series of column state vectors,
  generated to estimate by simulation and/or observation the quantile values
  required by the user. There are as many states as the number of samples
  required for this quantile estimate.

  Example :
  ``Xq = ADD.get("SampledStateForQuantiles")[:]``
