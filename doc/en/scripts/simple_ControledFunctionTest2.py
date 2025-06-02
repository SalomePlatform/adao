# -*- coding: utf-8 -*-
#
from numpy import array, ravel
def ControledQuadFunction( pair ):
    """
    Controlled quadratic simulation
    """
    coefficients, control = pair
    #
    u, v    = list(ravel(control))
    a, b, c = list(ravel(coefficients))
    x_points = (-5, 0, 1, 3, 10)
    y_points = []
    for x in x_points:
        y_points.append( (a*x*x + b*x + c + v) * u )
    return array(y_points)
#
from adao import adaoBuilder
case = adaoBuilder.New()
case.set( "CheckingPoint", Vector = array([1., 1., 1.]), Stored=True )
case.set( "ObservationOperator", ThreeFunctions = {
    "Direct" :ControledQuadFunction,
    "Tangent":0, # Empty operator (not None) as not used
    "Adjoint":0, # Empty operator (not None) as not used
    } )
case.set( "ControlInput", Vector = (1, 0) )
case.setAlgorithmParameters(
    Algorithm="ControledFunctionTest",
    Parameters={
        "NumberOfRepetition" : 15,
        "NumberOfPrintedDigits" : 3,
        "ShowElementarySummary":False,
        },
    )
case.execute()
