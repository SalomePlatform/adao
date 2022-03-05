# -*- coding: utf-8 -*-
#
from numpy import array
from adao import adaoBuilder
case = adaoBuilder.New()
case.set( 'AlgorithmParameters', Algorithm='3DVAR' )
case.set( 'Background',          Vector=[0, 1, 2] )
case.set( 'BackgroundError',     ScalarSparseMatrix=1.0 )
case.set( 'Observation',         Vector=array([0.5, 1.5, 2.5]) )
case.set( 'ObservationError',    DiagonalSparseMatrix='1 1 1' )
case.set( 'ObservationOperator', Matrix='1 0 0;0 2 0;0 0 3' )
case.set( 'Observer',            Variable="Analysis", Template="ValuePrinter" )
case.execute()
