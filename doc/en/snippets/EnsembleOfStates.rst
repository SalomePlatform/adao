.. index:: single: EnsembleOfStates

EnsembleOfStates
  *List of vectors or matrix*. Each element is an ordered collection of
  physical or parameter state vectors :math:`\mathbf{x}`. These are :math:`H`
  operator **entries**, i.e. current states before observation. At each step
  index, there is 1 state per column if this list is in matrix form, or 1 state
  per element if it's actually a list. Caution: the numbering of the support or
  points, on which or to which a state value is given in each vector, is
  implicitly that of the natural order of numbering of the state vector, from 0
  to the "size minus 1" of this vector.

  Example :
  ``{"EnsembleOfStates":[x1, x2, x3...]}``
