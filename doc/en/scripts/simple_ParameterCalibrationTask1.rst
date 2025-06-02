.. index:: single: ParameterCalibrationTask (example)

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

A 3DVAR variational optimization is used (default method), explicitly requested
here by the "3DVARGradientOptimization" variant specified for this algorithm.
By nature, the same results are obtained as in the first "3DVAR" algorithme
example (see its :ref:`section_ref_algorithm_3DVAR_examples`).
