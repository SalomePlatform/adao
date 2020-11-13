.. index:: single: Blue (example)

This example describes the interpolation between two physical states. These two
vector fields, of identical discretization, are the observation
:math:`\mathbf{y}^o` and the background state :math:`\mathbf{x}^b`. The
confidence in errors on the two information are considered identical. The
:math:`H` model fully observe the available field, it is a matrix selection
operator.

The interpolated resulting field is simply the "middle" between the two fields,
with an increased confidence on the errors.
