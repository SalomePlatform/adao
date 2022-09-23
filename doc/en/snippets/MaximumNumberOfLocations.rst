.. index:: single: MaximumNumberOfLocations

MaximumNumberOfLocations
  *Integer value*. This key specifies the maximum possible number of positions
  found in the optimal search. The default value is 1. The optimal search may
  eventually find less positions than required by this key, as for example in
  the case where the residual associated to the approximation is lower than the
  criterion and leads to the early termination of the optimal search.

  Example :
  ``{"MaximumNumberOfLocations":5}``
