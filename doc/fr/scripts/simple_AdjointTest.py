# -*- coding: utf-8 -*-
#
from numpy import array, eye
from adao import adaoBuilder
case = adaoBuilder.New('')
case.setCheckingPoint( Vector = array([0., 1., 2.]), Stored=True )
case.setObservation( Vector = [10., 11., 12.] )
case.setObservationOperator( Matrix = eye(3), )
case.setAlgorithmParameters(
    Algorithm='AdjointTest',
    Parameters={
        'EpsilonMinimumExponent' :-12,
        'NumberOfPrintedDigits' : 3,
        'SetSeed' : 1234567,
        },
    )
case.execute()
