.. index:: single: SetSeed

SetSeed
  *Integer value*. This key allow to give an integer in order to fix the seed
  of the random generator used in the algorithm. By default, the seed is left
  uninitialized, and so use the default initialization from the computer, which
  then change at each study. To ensure the reproducibility of results involving
  random samples, it is strongly advised to initialize the seed. A simple
  convenient value is for example 123456789. It is recommended to put an integer
  with more than 6 or 7 digits to properly initialize the random generator.

  Example:
  ``{"SetSeed":123456789}``
