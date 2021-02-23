.. index::
    single: Minimizer
    pair: Minimizer ; BEST1BIN",
    pair: Minimizer ; BEST1EXP",
    pair: Minimizer ; RAND1EXP",
    pair: Minimizer ; RANDTOBEST1EXP
    pair: Minimizer ; BEST2EXP
    pair: Minimizer ; RAND2EXP
    pair: Minimizer ; RANDTOBEST1BIN
    pair: Minimizer ; BEST2BIN
    pair: Minimizer ; RAND2BIN
    pair: Minimizer ; RAND1BIN

Minimizer
  *Predefined name*. This key allows to choose the optimization strategy for
  the minimizer. The default choice is "BEST1BIN", and the possible ones, among
  the multiples crossover and mutation strategies, are
  "BEST1BIN",
  "BEST1EXP",
  "BEST2BIN",
  "BEST2EXP",
  "RAND1BIN",
  "RAND1EXP",
  "RAND2BIN",
  "RAND2EXP",
  "RANDTOBEST1BIN",
  "RANDTOBEST1EXP".
  It is highly recommended to keep the default value.

  Example:
  ``{"Minimizer":"BEST1BIN"}``
