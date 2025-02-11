.. index:: single: SwarmInitialization

SwarmInitialization
  *Predefined name*. The name defines the particle swarm initialization mode
  for the "*ParticleSwarmOptimization*" algorithm. The particle series is
  initialized by specifying the distribution per component, which can be
  identical for all components (this is the case for all values except
  "DistributionByComponents"), or component-specific with
  "DistributionByComponents". In the latter case, it is also necessary to
  specify the "DistributionByComponents" keyword content. The default value is
  "UniformByComponents".

  The possible name is therefore in the following list:
  ["UniformByComponents",
  "LogUniformByComponents",
  "LogarithmicByComponents",
  "DistributionByComponents"].

  Example :
  ``{"SwarmInitialization":"UniformByComponents"}``
