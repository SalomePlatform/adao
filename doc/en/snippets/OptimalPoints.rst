.. index:: single: OptimalPoints

OptimalPoints
  *List of integer series*. Each element is a series, containing the indices of
  ideal positions or optimal points where a measurement is required, determined
  by the optimal search, ordered by decreasing preference and in the same order
  as the reduced basis vectors found iteratively.

  Example :
  ``op = ADD.get("OptimalPoints")[-1]``
