# -*- coding: utf-8 -*-
#
# Python script using ADAO TUI
#
import numpy as np
from numpy import array, matrix
from adao import adaoBuilder
case = adaoBuilder.New('')
case.set( Algorithm='Blue', Concept='AlgorithmParameters', Script='test914_Xternal_3_Variables.py' )
case.set( Concept='Background', Script='test914_Xternal_3_Variables.py', Vector=True )
case.set( Concept='BackgroundError', Matrix=True, Script='test914_Xternal_3_Variables.py' )
case.set( Concept='Directory', String='/home/test/ADAO' )
case.set( Concept='Name', String='Elementary algoritmic test' )
case.set( Concept='Observation', Script='test914_Xternal_3_Variables.py', Vector=True )
case.set( Concept='ObservationError', Matrix=True, Script='test914_Xternal_3_Variables.py' )
case.set( Concept='ObservationOperator', Matrix=True, Script='test914_Xternal_3_Variables.py' )
case.set( Concept='SupplementaryParameters', Parameters={'StudyType': 'ASSIMILATION_STUDY'} )
case.set( Concept='UserPostAnalysis', String='import numpy\nnumpy.set_printoptions(precision=3)\nprint("Analysis..............:",numpy.ravel(case.get("Analysis")[-1]))' )
case.execute()
import numpy
numpy.set_printoptions(precision=3)
print("Analysis..............:",numpy.ravel(case.get("Analysis")[-1]))
