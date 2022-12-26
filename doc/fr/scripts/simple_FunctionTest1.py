# -*- coding: utf-8 -*-
#
from numpy import array, eye
from adao import adaoBuilder
case = adaoBuilder.New()
case.setCheckingPoint( Vector = array([0., 1., 2.]), Stored=True )
case.setObservationOperator( Matrix = eye(3) )
case.setAlgorithmParameters(
    Algorithm='FunctionTest',
    Parameters={
        'NumberOfRepetition' : 5,
        'NumberOfPrintedDigits' : 2,
        'ShowElementarySummary':False,
        },
    )
case.execute()
