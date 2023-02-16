
     CONTROLEDFUNCTIONTEST
     =====================

     This test allows to analyze the (repetition of the) launch of some
     given simulation operator F, applied to one single vector x and to
     one control vector u as arguments, in a sequential way.
     The output shows simple statistics related to its successful execution,
     or related to the similarities of repetition of its execution.

===> Information before launching:
     -----------------------------

     Characteristics of input vector X, internally converted:
       Type...............: <class 'numpy.ndarray'>
       Length of vector...: 3
       Minimum value......: 1.000e+00
       Maximum value......: 1.000e+00
       Mean of vector.....: 1.000e+00
       Standard error.....: 0.000e+00
       L2 norm of vector..: 1.732e+00

     Characteristics of control parameter U, internally converted:
       Type...............: <class 'numpy.ndarray'>
       Length of vector...: 2
       Minimum value......: 0.000e+00
       Maximum value......: 1.000e+00
       Mean of vector.....: 5.000e-01
       Standard error.....: 5.000e-01
       L2 norm of vector..: 1.000e+00

     ---------------------------------------------------------------------------

===> Beginning of repeated evaluation, without activating debug

     ---------------------------------------------------------------------------

===> End of repeated evaluation, without deactivating debug

     ---------------------------------------------------------------------------

===> Launching statistical summary calculation for 15 states

     ---------------------------------------------------------------------------

===> Statistical analysis of the outputs obtained through sequential repeated evaluations

     (Remark: numbers that are (about) under 2e-16 represent 0 to machine precision)

     Number of evaluations...........................: 15

     Characteristics of the whole set of outputs Y:
       Size of each of the outputs...................: 5
       Minimum value of the whole set of outputs.....: 1.000e+00
       Maximum value of the whole set of outputs.....: 1.110e+02
       Mean of vector of the whole set of outputs....: 2.980e+01
       Standard error of the whole set of outputs....: 4.123e+01

     Characteristics of the vector Ym, mean of the outputs Y:
       Size of the mean of the outputs...............: 5
       Minimum value of the mean of the outputs......: 1.000e+00
       Maximum value of the mean of the outputs......: 1.110e+02
       Mean of the mean of the outputs...............: 2.980e+01
       Standard error of the mean of the outputs.....: 4.123e+01

     Characteristics of the mean of the differences between the outputs Y and their mean Ym:
       Size of the mean of the differences...........: 5
       Minimum value of the mean of the differences..: 0.000e+00
       Maximum value of the mean of the differences..: 0.000e+00
       Mean of the mean of the differences...........: 0.000e+00
       Standard error of the mean of the differences.: 0.000e+00

     ---------------------------------------------------------------------------

     End of the "CONTROLEDFUNCTIONTEST" verification

     ---------------------------------------------------------------------------

