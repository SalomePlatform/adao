.. index:: single: SampleAsMinMaxLatinHyperCube
.. index:: single: Latin hypercube

SampleAsMinMaxLatinHyperCube
  *List of real valued pairs [Min, Max], plus [Dimension, Number]*. This key
  describes the bounded domain in which the calculations points will be placed,
  from a *[Min, Max]* pair for each state component. The lower bounds are
  included. This list of pairs, identical in number to the size of the state
  space, is augmented by a pair of integers *[Dimension, Number]* containing
  the dimension of the state space and the desired number of sample points.
  Sampling is then automatically constructed using the Latin hypercube method
  (LHS). By nature, the points are included in the domain defined by the
  explicit bounds.

  Example :
  ``{"SampleAsMinMaxLatinHyperCube":[[0.,1.],[-1,3]]+[[2,11]]}`` for a state space of dimension 2 and for 11 sampling points.
