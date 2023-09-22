.. index:: single: ReducedBasis

ReducedBasis
  *List of matrix*. Each element is a matrix, containing in each column a
  vector of the reduced basis obtained by the optimal search, ordered by
  decreasing preference and in the same order as the ideal points found
  iteratively.

  When it is an input, it is identical to a single output of a
  :ref:`section_ref_algorithm_MeasurementsOptimalPositioningTask`.

  Example :
  ``rb = ADD.get("ReducedBasis")[-1]``
