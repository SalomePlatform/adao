.. index:: single: ResiduFormula

ResiduFormula
  *Predefined name*. This key indicates the residue formula that has to be
  used for the test. The default choice is "Taylor", and the possible ones are
  "Taylor" (normalized residue of the Taylor development of the operator, which
  has to decrease with the square power of the perturbation), "TaylorOnNorm"
  (residue of the Taylor development of the operator with respect to the
  perturbation to the square, which has to remain constant) and "Norm" (residue
  obtained by taking the norm of the Taylor development at zero order
  approximation, which approximate the gradient, and which has to remain
  constant).

  Example :
  ``{"ResiduFormula":"Taylor"}``
