.. index:: single: KalmanFilter (example)

First example
.............

The Kalman Filter can be used for a **reanalysis of observations of a given
dynamical model**. It is because the whole set of the observation  full history
is already known at the beginning of the time windows that it is called
*reanalysis*, even if the iterative analysis keeps unkown the future
observations at a given time step.

This example describes iterative estimation of a constant physical quantity (a
voltage) following seminal example of [Welch06]_ (pages 11 and following, also
available in the SciPy Cookbook). This model allows to illustrate the excellent
behavior of this algorithm with respect to the measurement noise when the
evolution model is simple. The physical problem is the estimation of the
voltage, observed on 50 time steps, with noise, which imply 50 analysis steps
by the filter. The idealized state (said the "true" value, unknown in a real
case) is specified as ``Xtrue`` in the example. The observations
:math:`\mathbf{y}^o` (denoted by ``Yobs`` in the example) are to be set, using
the keyword "*VectorSerie*", as a measure time series. We choose to emphasize
the observations versus the background, by setting a great value for the
background error variance with respect to the observation error variance. The
first observation is not used because the background :math:`\mathbf{x}^b` is
used as the first state estimate.

The adjustment is carried out by displaying intermediate results during
iterative filtering. Using these intermediate results, one can also obtain
figures that illustrate the state estimation and the associated *a posteriori*
covariance estimation.
