.. index:: single: EvolutionaryCovarianceOverallScale

EvolutionaryCovarianceOverallScale
  *Real value*. This key indicates the overall scaling factor for the
  covariance matrix during the CMA-ES evolutionary search process. It is also
  referred to as the search step size, or :math:`\sigma^g`, or
  :math:`\sigma^0`. It is a positive real number. The default value is
  :math:`0.5`, and it is important to adjust it to the specific physical case
  being studied by increasing or decreasing it.

  Example :
  ``{"EvolutionaryCovarianceOverallScale":0.5}``
