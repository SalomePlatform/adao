.. index:: single: EnsembleOfSnapshots

EnsembleOfSnapshots
  *List of vectors or matrix*. This key contains an ordered collection of
  physical state vectors :math:`\mathbf{y}`, called "*snapshots*" in reduced
  basis terminology. At each step index, there is 1 state per column if this
  list is in matrix form, or 1 state per element if it's actually a list.
  Caution: the numbering of the support or points, on which or to which a state
  value is given in each vector, is implicitly that of the natural order of
  numbering of the state vector, from 0 to the "size minus 1" of this vector.

  Example :
  ``{"EnsembleOfSnapshots":[y1, y2, y3...]}``
