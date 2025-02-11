.. index:: single: DistributionByComponents

DistributionByComponents
  *List of predefined names*. This keyword only needs to be defined when the
  particle swarm initialization for the "*ParticleSwarmOptimization*" algorithm
  is set to "DistributionByComponents". In this case, for each state component,
  the chosen distribution must be indicated in the form of a predefined name.
  Possible names are "uniform", "loguniform", "logarithmic", "['normal’,σ]",
  "['lognormal’,σ]" and "['logarithmicnormal’,σ]". All "*normal" distributions
  must be accompanied by an indication of the standard deviation σ, given that
  they are centered in the definition domain. The values "uniform",
  "loguniform", "normal", "lognormal" only affect position initialization by
  applying the indicated distribution, while the values "logarithmic" and
  "logarithmicnormal" affect both position and motion initialization. There
  must be the same number of values indicated as the size of an individual
  state. Distributions conform to the limits specified for the
  "*ParticleSwarmOptimization*" algorithm. Distributions can be different for
  each axis. When an identical distribution is chosen for all components, this
  is equivalent to choosing the global value of the previous keyword instead,
  if it exists.

  Example :
  ``{"DistributionByComponents" : ['uniform', 'loguniform', 'logarithmic', ['normal', 1]]}`` for a state space of dimension 4.
