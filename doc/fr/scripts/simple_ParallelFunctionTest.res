
     PARALLELFUNCTIONTEST
     ====================

     This test allows to analyze the (repetition of the) launch of some
     given simulation operator F, applied to one single vector argument x,
     in a parallel way.
     The output shows simple statistics related to its successful execution,
     or related to the similarities of repetition of its execution.

===> Information before launching:
     -----------------------------

     Characteristics of input vector X, internally converted:
       Type...............: <class 'numpy.ndarray'>
       Length of vector...: 30
       Minimum value......: 0.00e+00
       Maximum value......: 2.90e+01
       Mean of vector.....: 1.45e+01
       Standard error.....: 8.66e+00
       L2 norm of vector..: 9.25e+01

     ---------------------------------------------------------------------------

===> Beginning of repeated evaluation, without activating debug

     ---------------------------------------------------------------------------

     Appending the input vector to the agument set to be evaluated in parallel

     ---------------------------------------------------------------------------

===> Launching operator parallel evaluation for 50 states


===> End of operator parallel evaluation for 50 states

     ---------------------------------------------------------------------------

===> End of repeated evaluation, without deactivating debug

     ---------------------------------------------------------------------------

===> Launching statistical summary calculation for 50 states

     ---------------------------------------------------------------------------

===> Statistical analysis of the outputs obtained through parallel repeated evaluations

     (Remark: numbers that are (about) under 2e-16 represent 0 to machine precision)

     Number of evaluations...........................: 50

     Characteristics of the whole set of outputs Y:
       Size of each of the outputs...................: 30
       Minimum value of the whole set of outputs.....: 0.00e+00
       Maximum value of the whole set of outputs.....: 2.90e+01
       Mean of vector of the whole set of outputs....: 1.45e+01
       Standard error of the whole set of outputs....: 8.66e+00

     Characteristics of the vector Ym, mean of the outputs Y:
       Size of the mean of the outputs...............: 30
       Minimum value of the mean of the outputs......: 0.00e+00
       Maximum value of the mean of the outputs......: 2.90e+01
       Mean of the mean of the outputs...............: 1.45e+01
       Standard error of the mean of the outputs.....: 8.66e+00

     Characteristics of the mean of the differences between the outputs Y and their mean Ym:
       Size of the mean of the differences...........: 30
       Minimum value of the mean of the differences..: 0.00e+00
       Maximum value of the mean of the differences..: 0.00e+00
       Mean of the mean of the differences...........: 0.00e+00
       Standard error of the mean of the differences.: 0.00e+00

     ---------------------------------------------------------------------------

     End of the "PARALLELFUNCTIONTEST" verification

     ---------------------------------------------------------------------------

