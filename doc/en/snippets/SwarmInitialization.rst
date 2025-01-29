.. index:: single: SwarmInitialization

SwarmInitialization
  *Predefined name*. The name defines the particle swarm initialization mode
  for the "*ParticleSwarmOptimization*" algorithm. The particle series is
  initialized by specifying the distribution per component, which can be
  identical for all components (as with "UniformByComponents" or
  "LogUniformByComponents"), or component-specific with
  "DistributionByComponents". In the latter case, the content of the
  "DistributionByComponents" keyword must also be specified. The default value
  is "UniformByComponents".

  The possible name is therefore in the following list:
  ["UniformByComponents",
  "LogUniformByComponents",
  "DistributionByComponents"].

  Example :
  ``{"SwarmInitialization":"UniformByComponents"}``
