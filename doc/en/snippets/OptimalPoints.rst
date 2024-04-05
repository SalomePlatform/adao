.. index:: single: OptimalPoints

OptimalPoints
  *List of integer series*. Each element is a series, containing the indices of
  ideal positions or optimal points where a measurement is required, determined
  by the optimal search, ordered by decreasing preference and in the same order
  as the vectors iteratively found to form the reduced basis.

  Example :
  ``op = ADD.get("OptimalPoints")[-1]``
