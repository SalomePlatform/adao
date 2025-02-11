.. index:: single: CognitiveAccelerationControl

CognitiveAccelerationControl
  *Real value*. This key indicates the factor of change in the recall rate
  towards the best previously known value of the current insect's history. It
  is a positive real value whose default is 0, that is, by default, there is no
  change in the recall rate.

  In the ASAPSO adaptive case [Wang09]_, the value of this key indicates the
  **linear decrease** factor of the recall rate with the number of generations
  (with respect to the requested total number of generations), given that the
  initial value of the rate is indicated by the associated
  "*CognitiveAcceleration*" factor. There is no recommended value, but you
  could, for example, use the initial value :math:`1.19315` of the associated
  factor if you want to cancel any recall towards the best known value of the
  history at the end of the iterations.

  Example :
  ``{"CognitiveAccelerationControl":0.}``
