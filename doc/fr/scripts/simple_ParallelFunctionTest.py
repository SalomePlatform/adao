# -*- coding: utf-8 -*-
#
import numpy
from adao import adaoBuilder
#
def SomeOperator( x ):
    return numpy.dot(numpy.eye(x.size), numpy.ravel(x))
#
case = adaoBuilder.New('')
case.setAlgorithmParameters(
    Algorithm='ParallelFunctionTest',
    Parameters={
        'NumberOfRepetition' : 50,
        'NumberOfPrintedDigits' : 2,
        "ShowElementarySummary":False,
        },
    )
case.setCheckingPoint( Vector = range(30) )
case.setObservationOperator(
    OneFunction = SomeOperator,
    Parameters  = {
        "EnableMultiProcessingInEvaluation":True,
        "NumberOfProcesses":5,
        },
    )
case.execute()
