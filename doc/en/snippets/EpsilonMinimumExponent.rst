.. index:: single: EpsilonMinimumExponent

EpsilonMinimumExponent
  This key indicates the minimal exponent value of the power of 10 coefficient
  to be used to decrease the increment multiplier. The default is -8, and it
  has to be between 0 and -20. For example, its default value leads to
  calculate the residue of the scalar product formula with a fixed increment
  multiplied from 1.e0 to 1.e-8.

  Example :
  ``{"EpsilonMinimumExponent":-12}``
