# -*- coding: utf-8 -*-
#
from numpy import array, eye, ones
from adao import adaoBuilder
case = adaoBuilder.New()
case.set("CheckingPoint",       Vector = array([0., 1., 2.]) )
case.set("Observation",         Vector = ones(3) )
case.set("ObservationOperator", Matrix = 1/3 * eye(3) )
case.setAlgorithmParameters(
    Algorithm='ObservationSimulationComparisonTest',
    Parameters={
        'NumberOfRepetition' : 5,
        'NumberOfPrintedDigits' : 2,
        'ShowElementarySummary':False,
        'StoreSupplementaryCalculations': [
            'CostFunctionJ',
            ],
        },
    )
case.execute()
