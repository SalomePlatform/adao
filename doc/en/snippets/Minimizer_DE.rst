.. index:: single: Minimizer

Minimizer
  *Predefined name*. This key allows to choose the optimization strategy for
  the minimizer. The default choice is "BEST1BIN", and the possible ones, among
  the multiples crossover and mutation strategies, are
  "BEST1BIN",
  "BEST1EXP",
  "RAND1EXP",
  "RANDTOBEST1EXP",
  "BEST2EXP",
  "RAND2EXP",
  "RANDTOBEST1BIN",
  "BEST2BIN",
  "RAND2BIN",
  "RAND1BIN".
  It is greatly recommanded to keep the default value.

  Example:
  ``{"Minimizer":"BEST1BIN"}``
