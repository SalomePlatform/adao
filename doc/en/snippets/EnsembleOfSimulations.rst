.. index:: single: EnsembleOfSimulations

EnsembleOfSimulations
  *List of vectors or matrix*. This key contains an ordered collection of
  physical state vectors or simulated state vectors :math:`\mathbf{y}` that may
  be observed. These are :math:`H` operator **outputs**, i.e. simulated
  observation states (called "*snapshots*" in reduced-base terminology). At
  each step index, there is 1 state per column if this list is in matrix form,
  or 1 state per element if it's actually a list. Caution: the numbering of the
  support or points, on which or to which a state value is given in each
  vector, is implicitly that of the natural order of numbering of the state
  vector, from 0 to the "size minus 1" of this vector.

  Example :
  ``{"EnsembleOfSimulations":[y1, y2, y3...]}``
