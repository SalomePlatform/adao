.. index:: single: ProjectedGradientTolerance

ProjectedGradientTolerance
  This key indicates a limit value, leading to stop successfully the iterative
  optimization process when all the components of the projected gradient are
  under this limit. It is only used for constrained optimizers. The default is
  -1, that is the internal default of each minimizer (generally 1.e-5), and it
  is not recommended to change it.

  Example :
  ``{"ProjectedGradientTolerance":-1}``
