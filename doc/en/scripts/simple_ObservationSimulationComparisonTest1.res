
     OBSERVATIONSIMULATIONCOMPARISONTEST
     ===================================

     This test allows to analyze the (repetition of the) launch of some
     given simulation operator F, applied to one single vector argument x,
     and its comparison to observations or measures y through the innovation
     difference OMB = y - F(x) (Observation minus evaluation at Background)
     and (if required) the data assimilation standard cost function J.
     The output shows simple statistics related to its successful execution,
     or related to the similarities of repetition of its execution.

===> Information before launching:
     -----------------------------

     Characteristics of input vector X, internally converted:
       Type...............: <class 'numpy.ndarray'>
       Length of vector...: 3
       Minimum value......: 0.00e+00
       Maximum value......: 2.00e+00
       Mean of vector.....: 1.00e+00
       Standard error.....: 8.16e-01
       L2 norm of vector..: 2.24e+00

     Characteristics of input vector of observations Yobs, internally converted:
       Type...............: <class 'numpy.ndarray'>
       Length of vector...: 3
       Minimum value......: 1.00e+00
       Maximum value......: 1.00e+00
       Mean of vector.....: 1.00e+00
       Standard error.....: 0.00e+00
       L2 norm of vector..: 1.73e+00

     ---------------------------------------------------------------------------

===> Beginning of repeated evaluation, without activating debug

     ---------------------------------------------------------------------------

===> End of repeated evaluation, without deactivating debug

     ---------------------------------------------------------------------------

===> Launching statistical summary calculation for 5 states

     ---------------------------------------------------------------------------

===> Statistical analysis of the outputs obtained through sequential repeated evaluations

     (Remark: numbers that are (about) under 2e-16 represent 0 to machine precision)

     Number of evaluations...........................: 5

     Characteristics of the whole set of outputs Y:
       Size of each of the outputs...................: 3
       Minimum value of the whole set of outputs.....: 0.00e+00
       Maximum value of the whole set of outputs.....: 6.67e-01
       Mean of vector of the whole set of outputs....: 3.33e-01
       Standard error of the whole set of outputs....: 2.72e-01

     Characteristics of the vector Ym, mean of the outputs Y:
       Size of the mean of the outputs...............: 3
       Minimum value of the mean of the outputs......: 0.00e+00
       Maximum value of the mean of the outputs......: 6.67e-01
       Mean of the mean of the outputs...............: 3.33e-01
       Standard error of the mean of the outputs.....: 2.72e-01

     Characteristics of the mean of the differences between the outputs Y and their mean Ym:
       Size of the mean of the differences...........: 3
       Minimum value of the mean of the differences..: 0.00e+00
       Maximum value of the mean of the differences..: 0.00e+00
       Mean of the mean of the differences...........: 0.00e+00
       Standard error of the mean of the differences.: 0.00e+00

     ---------------------------------------------------------------------------

===> Statistical analysis of the OMB differences obtained through sequential repeated evaluations

     (Remark: numbers that are (about) under 2e-16 represent 0 to machine precision)

     Number of evaluations...........................: 5

     Characteristics of the whole set of OMB differences:
       Size of each of the outputs...................: 3
       Minimum value of the whole set of differences.: 3.33e-01
       Maximum value of the whole set of differences.: 1.00e+00
       Mean of vector of the whole set of differences: 6.67e-01
       Standard error of the whole set of differences: 2.72e-01

     Characteristics of the vector Dm, mean of the OMB differences:
       Size of the mean of the differences...........: 3
       Minimum value of the mean of the differences..: 3.33e-01
       Maximum value of the mean of the differences..: 1.00e+00
       Mean of the mean of the differences...........: 6.67e-01
       Standard error of the mean of the differences.: 2.72e-01

     Characteristics of the mean of the differences between the OMB differences and their mean Dm:
       Size of the mean of the differences...........: 3
       Minimum value of the mean of the differences..: 0.00e+00
       Maximum value of the mean of the differences..: 0.00e+00
       Mean of the mean of the differences...........: 0.00e+00
       Standard error of the mean of the differences.: 0.00e+00

     ---------------------------------------------------------------------------

===> Statistical analysis of the cost function J values obtained through sequential repeated evaluations

     Number of evaluations...........................: 5

     Characteristics of the whole set of data assimilation cost function J values:
       Minimum value of the whole set of J...........: 7.78e-01
       Maximum value of the whole set of J...........: 7.78e-01
       Mean of vector of the whole set of J..........: 7.78e-01
       Standard error of the whole set of J..........: 0.00e+00
       (Remark: variations of the cost function J only come from the observation part Jo of J)

     ---------------------------------------------------------------------------

     End of the "OBSERVATIONSIMULATIONCOMPARISONTEST" verification

     ---------------------------------------------------------------------------

