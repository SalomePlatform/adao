# -*- coding: utf-8 -*-
#
# Python script using ADAO TUI
#
from numpy import array, matrix
from adao import adaoBuilder
case = adaoBuilder.New('')
case.set( Algorithm='3DVAR', Concept='AlgorithmParameters', Script='test914_Xternal_3_Variables.py' )
case.set( Concept='Background', Script='test914_Xternal_3_Variables.py', Vector=True )
case.set( Concept='BackgroundError', Matrix=True, Script='test914_Xternal_3_Variables.py' )
case.set( Concept='Directory', String='/home/test/ADAO' )
case.set( Concept='Name', String='Elementary algoritmic test' )
case.set( Concept='Observation', Script='test914_Xternal_3_Variables.py', Vector=True )
case.set( Concept='ObservationError', Matrix=True, Script='test914_Xternal_3_Variables.py' )
case.set( Concept='ObservationOperator', Matrix=True, Script='test914_Xternal_3_Variables.py' )
case.set( Concept='SupplementaryParameters', Parameters={'StudyType': 'ASSIMILATION_STUDY'} )
case.set( Concept='UserPostAnalysis', String='print("Analysis [1.0,1.0,1.0]:",case.get("Analysis")[-1])' )
case.execute()
print("Analysis [1.0,1.0,1.0]:",case.get("Analysis")[-1])
