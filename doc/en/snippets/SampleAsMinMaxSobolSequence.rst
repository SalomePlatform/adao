.. index:: single: SampleAsMinMaxSobolSequence
.. index:: single: Sobol Sequence

SampleAsMinMaxSobolSequence
  *List of triplets of pair values*. This key describes the bounded domain in
  which the calculations points will be placed, from a *[min,max]* pair for
  each state component. The lower bounds are included. This list of pairs,
  identical in number to the size of the state space, is augmented by a pair of
  integers *[dim,nbr]* containing the dimension of the state space and the
  minimum desired number of sample points (by construction, the number of
  points generated in the Sobol sequence will be the power of 2 immediately
  above this minimum number). Sampling is then automatically constructed using
  the Latin hypercube method (LHS).

  Example :
  ``{"SampleAsMinMaxSobolSequence":[[0.,1.],[-1,3]]+[[2,11]]}`` for a state space of dimension 2 and 11 sampling points (there will be 16 points in practice).
