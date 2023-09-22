.. index:: single: ExcludedPoints

ExcludedPoints
  *List of integer series*. Each element is a series, containing the indices of
  the points excluded from the optimal search, according to the order of the
  variables of a state vector considered arbitrarily in one-dimensional form.

  Example :
  ``ep = ADD.get("ExcludedPoints")[-1]``
