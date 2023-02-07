# -*- coding: utf-8 -*-
#
from numpy import array, ravel
def ControledQuadFunction( paire ):
    """
    Simulation quadratique contrôlée
    """
    coefficients, controle = paire
    #
    u, v    = list(ravel(controle))
    a, b, c = list(ravel(coefficients))
    x_points = (-5, 0, 1, 3, 10)
    y_points = []
    for x in x_points:
        y_points.append( (a*x*x + b*x + c + v) * u )
    return array(y_points)
#
from adao import adaoBuilder
case = adaoBuilder.New()
case.set( 'CheckingPoint', Vector = array([1., 1., 1.]), Stored=True )
case.set( 'ObservationOperator', ThreeFunctions = {
    "Direct" :ControledQuadFunction,
    "Tangent":0, # Opérateur vide (et pas None) car non utilisé
    "Adjoint":0, # Opérateur vide (et pas None) car non utilisé
    } )
case.set( "ControlInput", Vector = (1, 0) )
case.setAlgorithmParameters(
    Algorithm='ControledFunctionTest',
    Parameters={
        'NumberOfRepetition' : 15,
        'NumberOfPrintedDigits' : 3,
        'ShowElementarySummary':False,
        },
    )
case.execute()
