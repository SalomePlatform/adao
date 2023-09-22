.. index:: single: EnsembleOfSimulations

EnsembleOfSimulations
  *List of vectors or matrix*. This key contains an ordered collection of
  physical or simulated state vectors :math:`\mathbf{y}` (called "*snapshots*"
  in reduced basis terminology), with 1 state per column if it is a matrix, or
  1 state per element if it is a list. Caution: the numbering of the support or
  points, on which or to which a state value is given in each vector, is
  implicitly that of the natural order of numbering of the state vector, from 0
  to the "size minus 1" of this vector.

  Example :
  ``{"EnsembleOfSimulations":[y1, y2, y3...]}``
