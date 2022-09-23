.. index:: single: ExcludeLocations

ExcludeLocations
  *List of integers*. This key specifies the list of points in the state vector
  excluded from the optimal search. The default value is an empty list.
  Important: the numbering of these excluded points must be identical to the
  one implicitly adopted in the states provided by the "*EnsembleOfSnapshots*"
  key.

  Example :
  ``{"ExcludeLocations":[3, 125, 286]}``
