# -*- coding: utf-8 -*-
#
# Python script using ADAO TUI
#
from numpy import array, matrix
from adao import adaoBuilder
case = adaoBuilder.New('')
case.set( Algorithm='GradientTest', Concept='AlgorithmParameters', Script='test914_Xternal_4_Variables.py' )
case.set( Concept='CheckingPoint', Script='test914_Xternal_4_Variables.py', Vector=True )
case.set( Concept='Directory', String='/home/test/ADAO' )
case.set( Concept='Name', String='Elementary gradient test' )
case.set( Concept='ObservationOperator', OneFunction=True, Parameters={'DifferentialIncrement': 1e-06, 'CenteredFiniteDifference': 0}, Script='test914_Xternal_4_Variables.py' )
case.set( Concept='SupplementaryParameters', Parameters={'StudyType': 'CHECKING_STUDY', 'ExecuteInContainer': 'Mono'} )
case.execute()
