.. index:: single: EvolutionaryPopulationSize

EvolutionaryPopulationSize
  *Real value*. This key indicates the population size of the states evaluated
  at each step during the CMA-ES evolutionary search process. It is an integer.
  If the default value is zero, it is automatically set to the value
  recommended by the theoretical method to :math:`4+3\log(dimension)`, where
  :math:`dimension` is the dimension of the state space.

  Example :
  ``{"EvolutionaryPopulationSize":15}``

