# -*- coding: utf-8 -*-
#
# Python script using ADAO TUI
#
from numpy import array, matrix
from adao import adaoBuilder
case = adaoBuilder.New('')
case.set( Algorithm='Blue', Concept='AlgorithmParameters' )
case.set( Concept='Background', Vector='0 0 0' )
case.set( Concept='BackgroundError', Matrix='1 0 0 ; 0 1 0 ; 0 0 1' )
case.set( Concept='Name', String='Elementary algoritmic test' )
case.set( Concept='Observation', Vector='1 1 1' )
case.set( Concept='ObservationError', Matrix='1 0 0 ; 0 1 0 ; 0 0 1' )
case.set( Concept='ObservationOperator', Matrix='1 0 0 ; 0 1 0 ; 0 0 1' )
case.set( Concept='SupplementaryParameters', Parameters={'StudyType': 'ASSIMILATION_STUDY'} )
case.set( Concept='UserPostAnalysis', String='import numpy\nnumpy.set_printoptions(precision=3)\nprint("Analysis [0.5,0.5,0.5]:",numpy.ravel(case.get("Analysis")[-1]))' )
case.execute()
import numpy
numpy.set_printoptions(precision=3)
print("Analysis [0.5,0.5,0.5]:",numpy.ravel(case.get("Analysis")[-1]))
