.. index:: single: InitializationPoint

InitializationPoint
  *Vector*. The variable specifies one vector to be used as the initial state
  around which an iterative algorithm starts. By default, this initial state is
  not required and is equal to the background :math:`\mathbf{x}^b`. Its value
  must allow to build a vector of the same size as the background. If provided,
  it replaces the background only for initialization.

  Example :
  ``{"InitializationPoint":[1, 2, 3, 4, 5]}``
