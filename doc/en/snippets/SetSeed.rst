.. index:: single: SetSeed

SetSeed
  *Integer value*. This key allow to give an integer in order to fix the seed
  of the random generator used in the algorithm. A simple convenient value is
  for example 1000. By default, the seed is left uninitialized, and so use the
  default initialization from the computer, which then change at each study. To
  ensure the reproducibility of results involving random samples, it is
  strongly advised to initialize the seed.

  Example:
  ``{"SetSeed":1000}``
