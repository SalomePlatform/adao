.. index:: single: GradientNormTolerance

GradientNormTolerance
  This key indicates a limit value, leading to stop successfully the
  iterative optimization process when the norm of the gradient is under this
  limit. It is only used for non-constrained optimizers.  The default is
  1.e-5 and it is not recommended to change it.

  Example:
  ``{"GradientNormTolerance":1.e-5}``
