.. index:: single: 3DVAR (example)

First example
.............

This example describes the calibration of parameters  :math:`\mathbf{x}` of a
quadratic observation model :math:`H`. This model :math:`H` is here represented
as a function named ``QuadFunction`` for the purpose of this example. This
function get as input the coefficients vector :math:`\mathbf{x}` of the
quadratic form, and return as output the evaluation vector :math:`\mathbf{y}`
of the quadratic model at the predefined internal control points, predefined in
a static way in the model.

The calibration is done using an initial coefficient set (background state
specified by ``Xb`` in the example), and with the information
:math:`\mathbf{y}^o` (specified by ``Yobs`` in the example) of 5 measures
obtained in these same internal control points. We set twin experiments (see
:ref:`section_methodology_twin`) and the measurements are supposed to be
perfect. We choose to emphasize the observations, versus the background, by
setting artificially a great variance for the background error, here of
:math:`10^{6}`.

The adjustment is carried out by displaying intermediate results using
"*observer*" (for reference, see :ref:`section_advanced_observer`) during
iterative optimization.
