Third example
.............

From the preceding example, if one wants to adapt the time convergence of the
3DVAR, one can change, for example, the *a priori* covariance assumptions of
the background errors during the iterations. This update is an **assumption**
of the user, and there are multiple alternatives that will depend on the
physics of the case. We illustrate one of them here.

We choose, in an arbitrary way, to make the *a priori* covariance of the
background errors to decrease by a constant factor :math:`0.9^2=0.81` as long
as it remains above a limit value of :math:`0.1^2=0.01` (which is the fixed
value of *a priori* covariance of the background errors of the previous
example), knowing that it starts at the value `1` (which is the fixed value of
*a priori* covariance of the background errors used for the first step of
Kalman filtering). This value is updated at each step, by reinjecting it as the
*a priori* covariance of the state which is used as a background in the next
step of analysis, in an explicit loop.

We notice in this case that the state estimation converges faster to the true
value, and that the assimilation then behaves similarly to the examples for the
Kalman Filter, or to the previous example with the manually adapted *a priori*
covariances. Moreover, the *a posteriori* covariance decreases as long as we
force the decrease of the *a priori* covariance.

.. note::

    We insist on the fact that the *a priori* covariance variations, which
    determine the *a posteriori* covariance variations, are a **user
    assumption** and not an obligation. This assumption must therefore be
    **adapted to the physical case**.
