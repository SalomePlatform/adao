.. index:: single: NonLinearLeastSquares (example)

This example describes the calibration of parameters  :math:`\mathbf{x}` of a
quadratic observation model :math:`H`. This model is here represented as a
function named ``QuadFunction``. This function get as input the coefficients
vector :math:`\mathbf{x}`, and return as output the evaluation vector
:math:`\mathbf{y}` of the quadratic model at the predefined internal control
points. The calibration is done using an initial coefficient set (background
state specified by ``Xb`` in the code), and with the information
:math:`\mathbf{y}^o` (specified by ``Yobs`` in the code) of 5 measures obtained
in these same internal control points. We set twin experiments (see
:ref:`section_methodology_twin`) and the measurements are supposed to be
perfect.

The adjustment is carried out by displaying intermediate results during
iterative optimization.
