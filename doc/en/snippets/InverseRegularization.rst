.. index:: single: InverseRegularization

InverseRegularization
  *Real value*. This key indicates the type of regularization used in the
  inverse calculation of reduced coordinates during a reduced-basis
  approximation. When it is strictly negative (which is the default value), the
  pseudo-inverse is used. When it is strictly positive, regularization is used
  with the value contained in the key as the additional coefficient. When it is
  zero, direct inversion is used. The three methods are equivalent in theory,
  and for common dimensions. The default method is the most accurate. It is
  strongly recommended to keep the default value.

  Example:
  ``{"InverseRegularization":-1}``
