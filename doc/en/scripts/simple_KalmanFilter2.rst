The Kalman filter can also be used for a **running analysis of the observations
of a given dynamic model**. In this case, the analysis is conducted
iteratively, at the arrival of each observation.

The following example deals with the same simple dynamic system from the
reference [Welch06]_. The essential difference consists in carrying out the
execution of a Kalman step at the arrival of each observation provided
iteratively. The keyword "*nextStep*", included in the execution order, allows
to not store the background in duplicate of the previous analysis.

In an entirely similar way to the reanalysis (knowing that intermediate results
can be displayed, which are omitted here for simplicity), estimation gives the
same results during iterative filtering. Thanks to these intermediate
information, one can also obtain the graphs illustrating the estimation of the
state and the associated *a posteriori* error covariance.
