.. index:: single: ParameterCalibrationTask (example)

Second example
..............

Since it's easy to change optimization approach, the aim of this second example
is to calibrate parameters using derivative-free optimization. This is
indicated to this algorithm by the variant "DerivativeFreeOptimization"
(accompanied by a change of optimizer by the keyword "Minimizer"). Only the
values of these two keywords "Variant" and "Minimizer" therefore change between
the two approaches.

In this extremely simple case, of small dimensions and without any special
optimization difficulty, the control parameters remain the same. The results
are of the same quality as for the reference variational optimization.
