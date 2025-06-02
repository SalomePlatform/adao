# -*- coding: utf-8 -*-
#
from numpy import array
from adao import adaoBuilder
case = adaoBuilder.New()
case.set( "AlgorithmParameters", Algorithm="3DVAR" )
case.set( "Background",          Vector=[0, 1, 2] )
#
print(case)
