.. index:: single: MeasurementsOptimalPositioningTask (example)

Third example
.............

This more complete example describes the optimal positioning of measurements
associated with a reduced DEIM-type decomposition on a classical parametric
non-linear function, as proposed in reference [Chaturantabut10]_. This
particular function has the notable advantage of being dependent only on a
position :math:`x` in 2D and a parameter :math:`\mu` in 2D too. It therefore
enables a pedagogical illustration of optimal measurement points.

This function depends on the position :math:`x=(x_1,x_2)\in\Omega=[0.1,0.9]^2`
in the 2D plane, and on the parameter
:math:`\mu=(\mu_1,\mu_2)\in\mathcal{D}=[-1,-0.01]^2` of dimension 2 :

.. math:: G(x;\mu) = \frac{1}{\sqrt{(x_1 - \mu_1)^2 + (x_2 - \mu_2)^2 + 0.1^2}}

The function is represented on a regular :math:`\Omega_G` spatial grid of size
20x20 points. It is available in ADAO built-in test models under the name
``TwoDimensionalInverseDistanceCS2010``, together with the spatial and
parametric domain default definition. So here we first build a set of
simulations of :math:`G`, then we look for the best locations for measurements
to obtain an DEIM interpolation representation of the fields, by applying the
DEIM-type decomposition algorithm to it, and then derive some simple
illustrations. We choose to look for an arbitrary number ``nbmeasures`` of 15
measurement locations.

It can be seen that the singular values decrease steadily down to numerical
noise, indicating that around a hundred basis elements are needed to fully
represent the information contained in the set of :math:`G` simulations.
Furthermore, the optimal measurement points in the :math:`\Omega_G` domain are
inhomogeneously distributed, favoring the spatial zone near the
:math:`(0.1,0.1)` corner in which the :math:`G` function varies more.
