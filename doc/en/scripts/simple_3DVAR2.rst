Second example
..............

The 3DVAR can also be used for a **time analysis of the observations of a given
dynamic model**. In this case, the analysis is performed iteratively, at the
arrival of each observation. For this example, we use the same simple dynamic
system [Welch06]_ that is analyzed in the Kalman Filter
:ref:`section_ref_algorithm_KalmanFilter_examples`.

At each step, the classical 3DVAR analysis updates only the state of the
system. By modifying the *a priori* covariance values with respect to the
initial assumptions of the filtering, this 3DVAR reanalysis allows to converge
towards the true trajectory, as illustrated in the associated figure, in a
slightly slower speed than with a Kalman Filter.

.. note::

    Note about *a posteriori* covariances: classically, the 3DVAR iterative
    analysis updates only the state and not its covariance. As the assumptions
    of operators and *a priori* covariance remain unchanged here during the
    evolution, the *a posteriori* covariance is constant. The following plot of
    this *a posteriori* covariance allows us to insist on this property, which
    is entirely expected from the 3DVAR analysis. A more advanced hypothesis is
    proposed in the forthcoming example.
