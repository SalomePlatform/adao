.. index:: single: Alpha
.. index:: single: Beta
.. index:: single: Kappa
.. index:: single: Reconditioner

Alpha, Beta, Kappa, Reconditioner
  These keys are internal scaling parameters. "Alpha" requires a value between
  1.e-4 and 1. "Beta" has an optimal value of 2 for Gaussian *a priori*
  distribution. "Kappa" requires an integer value, and the right default is
  obtained by setting it to 0. "Reconditioner" requires a value between 1.e-3
  and 10, it defaults to 1.

  Example :
  ``{"Alpha":1,"Beta":2,"Kappa":0,"Reconditioner":1}``
