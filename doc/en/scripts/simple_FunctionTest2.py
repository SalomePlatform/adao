# -*- coding: utf-8 -*-
#
from numpy import array, ravel
def QuadFunction( coefficients ):
    """
    Quadratic simulation in x: y = a x^2 + b x + c
    """
    a, b, c = list(ravel(coefficients))
    x_points = (-5, 0, 1, 3, 10)
    y_points = []
    for x in x_points:
        y_points.append( a*x*x + b*x + c )
    return array(y_points)
#
# (Re)naming statement for the simulation function
DirectOperator = QuadFunction
#
from adao import adaoBuilder
case = adaoBuilder.New()
case.set( 'CheckingPoint', Vector = array([1., 1., 1.]), Stored=True )
case.set( 'ObservationOperator', OneFunction = DirectOperator )
case.setAlgorithmParameters(
    Algorithm='FunctionTest',
    Parameters={
        'NumberOfRepetition' : 15,
        'NumberOfPrintedDigits' : 3,
        'ShowElementarySummary':False,
        },
    )
case.execute()
