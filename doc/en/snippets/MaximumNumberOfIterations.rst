.. index:: single: MaximumNumberOfIterations

MaximumNumberOfIterations
  *Integer value*. This key indicates the maximum number of iterations allowed
  for iterative optimization. The default is 15000, which is very similar to no
  limit on iterations. It is then recommended to adapt this parameter to the
  needs on real problems. For some optimizers, the effective stopping step can
  be slightly different of the limit due to algorithm internal control
  requirements. One can refer to the section describing ways for
  ref:`subsection_iterative_convergence_control` for more detailed
  recommendations.

  Example:
  ``{"MaximumNumberOfIterations":100}``
