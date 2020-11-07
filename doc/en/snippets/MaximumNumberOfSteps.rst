.. index:: single: MaximumNumberOfSteps

MaximumNumberOfSteps
  *Integer value*. This key indicates the maximum number of iterations allowed
  for iterative optimization. The default is 15000, which is very similar to no
  limit on iterations. It is then recommended to adapt this parameter to the
  needs on real problems. For some optimizers, the effective stopping step can
  be slightly different of the limit due to algorithm internal control
  requirements.

  Example:
  ``{"MaximumNumberOfSteps":100}``
