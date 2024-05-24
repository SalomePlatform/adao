# -*- coding: utf-8 -*-
#
import numpy
from adao import adaoBuilder
numpy.random.seed(123456789)
#
dimension = 100
nbsnapshots = 15
Ensemble = numpy.empty((dimension,2*nbsnapshots))
for i in range(nbsnapshots):
    Ensemble[:,i] = numpy.sin((i+1)*numpy.arange(dimension))
Ensemble[:,nbsnapshots:2*nbsnapshots] = Ensemble[:,:nbsnapshots]
#
case = adaoBuilder.New()
case.setAlgorithmParameters(
    Algorithm = 'ReducedModelingTest',
    Parameters = {
        "EnsembleOfSnapshots":Ensemble,
        "StoreSupplementaryCalculations":["Residus","SingularValues"],
        "PlotAndSave":True,
        "ResultFile":"simple_ReducedModelingTest1.png",
        }
    )
case.execute()
