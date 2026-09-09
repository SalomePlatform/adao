
     REDUCEDMODELINGTEST
     ===================

     This test allows to analyze the characteristics of the collection of
     states from a reduction point of view. Using an SVD, it measures how
     the information decreases with the number of singular values, either
     as values or, with a statistical point of view, as remaining variance.

===> Information before launching:
     -----------------------------

     Characteristics of input data:
       State dimension................: 100
       Number of snapshots to test....: 30

===> Summary of the 5 first singular values:
     ---------------------------------------

     Singular values σ:
       σ[1] = 1.03513e+01
       σ[2] = 1.03509e+01
       σ[3] = 1.03258e+01
       σ[4] = 1.02436e+01
       σ[5] = 1.02386e+01

     Singular values σ divided by the first one σ[1]:
       σ[1] / σ[1] = 1.00000e+00
       σ[2] / σ[1] = 9.99962e-01
       σ[3] / σ[1] = 9.97533e-01
       σ[4] / σ[1] = 9.89589e-01
       σ[5] / σ[1] = 9.89104e-01

===> Ordered singular values and remaining variance:
     -----------------------------------------------

     -------------------------------------------------------------------------
        i  | Singular value σ |        σ[i]/σ[1] | Variance: part, remaining
     -------------------------------------------------------------------------
       00  |      1.03513e+01 |      1.00000e+00 |            7% ,    92.8%
       01  |      1.03509e+01 |      9.99962e-01 |            7% ,    85.6%
       02  |      1.03258e+01 |      9.97533e-01 |            7% ,    78.5%
       03  |      1.02436e+01 |      9.89589e-01 |            7% ,    71.5%
       04  |      1.02386e+01 |      9.89104e-01 |            7% ,    64.4%
       05  |      1.01050e+01 |      9.76200e-01 |            6% ,    57.6%
       06  |      9.99948e+00 |      9.66009e-01 |            6% ,    50.9%
       07  |      9.99643e+00 |      9.65714e-01 |            6% ,    44.2%
       08  |      9.98375e+00 |      9.64489e-01 |            6% ,    37.5%
       09  |      9.90828e+00 |      9.57198e-01 |            6% ,    31.0%
       10  |      9.90691e+00 |      9.57066e-01 |            6% ,    24.4%
       11  |      9.64803e+00 |      9.32056e-01 |            6% ,    18.1%
       12  |      9.62587e+00 |      9.29916e-01 |            6% ,    11.9%
       13  |      9.62344e+00 |      9.29681e-01 |            6% ,     5.7%
       14  |      9.25446e+00 |      8.94035e-01 |            5% ,     0.0%
       15  |      2.47838e-15 |      2.39426e-16 |            0% ,     0.0%
       16  |      2.09564e-15 |      2.02451e-16 |            0% ,     0.0%
       17  |      1.95879e-15 |      1.89231e-16 |            0% ,     0.0%
       18  |      1.78333e-15 |      1.72280e-16 |            0% ,     0.0%
       19  |      1.55457e-15 |      1.50180e-16 |            0% ,     0.0%
       20  |      1.38662e-15 |      1.33955e-16 |            0% ,     0.0%
       21  |      1.22127e-15 |      1.17982e-16 |            0% ,     0.0%
       22  |      1.06733e-15 |      1.03111e-16 |            0% ,     0.0%
       23  |      9.85210e-16 |      9.51771e-17 |            0% ,     0.0%
       24  |      9.29354e-16 |      8.97811e-17 |            0% ,     0.0%
       25  |      8.31224e-16 |      8.03011e-17 |            0% ,     0.0%
       26  |      6.52763e-16 |      6.30608e-17 |            0% ,     0.0%
       27  |      5.98109e-16 |      5.77809e-17 |            0% ,     0.0%
       28  |      2.90708e-16 |      2.80841e-17 |            0% ,     0.0%
       29  |      2.11986e-16 |      2.04791e-17 |            0% ,     0.0%
     -------------------------------------------------------------------------

===> Summary of variance cut-off:
     ----------------------------
     Representing more than 90%    of variance requires at least 14 mode(s).
     Representing more than 99%    of variance requires at least 15 mode(s).
     Representing more than 99.9%  of variance requires at least 15 mode(s).
     Representing more than 99.99% of variance requires at least 15 mode(s).

     Plot and save results in a file named "simple_ReducedModelingTest1.png"

     ---------------------------------------------------------------------------

     End of the "REDUCEDMODELINGTEST" verification

     ---------------------------------------------------------------------------

