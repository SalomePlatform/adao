.. index:: single: SocialAccelerationControl

SocialAccelerationControl
  *Real value*. This key indicates the factor of change in the recall rate
  towards the best insect in the current insect's neighborhood, which by
  default is the complete swarm. It is a positive real value whose default is
  0, that is, by default, there is no change in the recall rate.

  In the ASAPSO adaptive case [Wang09]_, the value of this key indicates the
  **linear growth** factor of the recall rate with the number of generations (
  with respect to the requested total number of generations), given that the
  initial value of the rate is indicated by the associated
  "*SocialAcceleration*" factor. There is no recommended value, but you can use
  the initial value :math:`1.19315` of the associated factor, for example, if
  you want to double the recall towards the best known value of the
  neighborhood at the end of the iterations.

  Example :
  ``{"SocialAccelerationControl":0.}``
