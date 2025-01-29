.. index:: single: DistributionByComponents

SwarmInitialization
  *List of predefined names*. This keyword only needs to be defined when the
  particle swarm initialization for the "*ParticleSwarmOptimization*" algorithm
  is set to "DistributionByComponents". In this case, for each state component,
  the chosen distribution must be indicated in the form of a predefined name.
  Possible names are 'uniform' and 'loguniform', and the distributions use the
  bounds specified for the "*ParticleSwarmOptimization*" algorithm.
  Distributions can be different for each axis.

  Example :
  ``{"DistributionByComponents":['loguniform', 'uniform', 'loguniform']}`` for a state space of dimension 3.
