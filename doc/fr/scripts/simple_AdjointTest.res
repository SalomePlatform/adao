
     ADJOINTTEST
     ===========

     This test allows to analyze the quality of an adjoint operator associated
     to some given direct operator F, applied to one single vector argument x.
     If the adjoint operator is approximated and not given, the test measures
     the quality of the automatic approximation, around an input checking point X.

===> Information before launching:
     -----------------------------

     Characteristics of input vector X, internally converted:
       Type...............: <class 'numpy.ndarray'>
       Length of vector...: 3
       Minimum value......: 0.000e+00
       Maximum value......: 2.000e+00
       Mean of vector.....: 1.000e+00
       Standard error.....: 8.165e-01
       L2 norm of vector..: 2.236e+00

     ---------------------------------------------------------------------------

===> Numerical quality indicators:
     -----------------------------

     Using the "ScalarProduct" formula, one observes the residue R which is the
     difference of two scalar products:

         R(Alpha) = | < TangentF_X(dX) , Y > - < dX , AdjointF_X(Y) > |

     which must remain constantly equal to zero to the accuracy of the calculation.
     One takes dX0 = Normal(0,X) and dX = Alpha*dX0, where F is the calculation
     operator. If it is given, Y must be in the image of F. If it is not given,
     one takes Y = F(X).

     (Remark: numbers that are (about) under 2e-16 represent 0 to machine precision)


     -------------------------------------------------------------
       i   Alpha     ||X||       ||Y||       ||dX||     R(Alpha)
     -------------------------------------------------------------
        0  1e+00   2.236e+00   1.910e+01   3.536e+00   0.000e+00
        1  1e-01   2.236e+00   1.910e+01   3.536e-01   0.000e+00
        2  1e-02   2.236e+00   1.910e+01   3.536e-02   0.000e+00
        3  1e-03   2.236e+00   1.910e+01   3.536e-03   0.000e+00
        4  1e-04   2.236e+00   1.910e+01   3.536e-04   0.000e+00
        5  1e-05   2.236e+00   1.910e+01   3.536e-05   0.000e+00
        6  1e-06   2.236e+00   1.910e+01   3.536e-06   0.000e+00
        7  1e-07   2.236e+00   1.910e+01   3.536e-07   0.000e+00
        8  1e-08   2.236e+00   1.910e+01   3.536e-08   0.000e+00
        9  1e-09   2.236e+00   1.910e+01   3.536e-09   0.000e+00
       10  1e-10   2.236e+00   1.910e+01   3.536e-10   0.000e+00
       11  1e-11   2.236e+00   1.910e+01   3.536e-11   0.000e+00
       12  1e-12   2.236e+00   1.910e+01   3.536e-12   0.000e+00
     -------------------------------------------------------------

     End of the "ADJOINTTEST" verification by the "ScalarProduct" formula.

     ---------------------------------------------------------------------------

