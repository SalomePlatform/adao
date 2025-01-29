.. index:: single: SampleAsMinMaxStepHyperCube

SampleAsMinMaxStepHyperCube
  *List of triplets of real values [Min, Max, Step]*. This key describes the
  calculations points as an hyper-cube, from a given list of implicit sampling
  of each variable by a triplet *[Min, Max, Step]*. That is then a list of the
  same size than the one of the state. The bounds are included. By nature, the
  points are included in the domain defined by the explicit bounds.

  Example :
  ``{"SampleAsMinMaxStepHyperCube":[[0.,1.,0.25],[-1,3,1]]}`` for a state space of dimension 2.
