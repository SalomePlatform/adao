.. index:: single: SwarmTopology

SwarmTopology
  *Predefined name*. This key indicates how the particles (or insects)
  communicate information to each other during the evolution of the particle
  swarm. The most classical method consists in exchanging information between
  all particles (called "gbest" or "FullyConnectedNeighborhood"). But it is
  often more efficient to exchange information on a reduced neighborhood, as in
  the classical method "lbest" (or "RingNeighborhoodWithRadius1") exchanging
  information with the two neighboring particles in numbering order (the
  previous one and the next one), or the method "RingNeighborhoodWithRadius2"
  exchanging with the 4 neighbors (the two previous ones and the two following
  ones). A variant of reduced neighborhood consists in exchanging with 3
  neighbors (method "AdaptativeRandomWith3Neighbors") or 5 neighbors (method
  "AdaptativeRandomWith5Neighbors") chosen randomly (the particle can be drawn
  several times). The default value is "FullyConnectedNeighborhood", and it is
  advisable to change it carefully depending on the properties of the simulated
  physical system. The possible communication topology is to be chosen from the
  following list, in which the equivalent names are indicated by a "<=>" sign:
  ["FullyConnectedNeighborhood" <=> "FullyConnectedNeighbourhood" <=> "gbest",
  "RingNeighborhoodWithRadius1" <=> "RingNeighbourhoodWithRadius1" <=> "lbest",
  "RingNeighborhoodWithRadius2" <=> "RingNeighbourhoodWithRadius2",
  "AdaptativeRandomWith3Neighbors" <=> "AdaptativeRandomWith3Neighbours" <=> "abest",
  "AdaptativeRandomWith5Neighbors" <=> "AdaptativeRandomWith5Neighbours"].

  Example :
  ``{"SwarmTopology":"FullyConnectedNeighborhood"}``
