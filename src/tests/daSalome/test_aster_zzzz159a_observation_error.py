#-*-coding:iso-8859-1-*-
import numpy
experience = init_data["experience"]
nbmesures = 11 # De 0 à 1 par pas de 0.1
instants = numpy.array([0.1*i for i in range(nbmesures)])
yo = []
for reponse in experience:
    for t,v in list(reponse):
        if min(abs(t - instants)) < 1.e-8:
            yo.append(v)

R  = numpy.matrix(numpy.core.identity(len(yo)))
dimensionYo = len( yo )
R = numpy.matrix( R, numpy.float ).reshape((dimensionYo,dimensionYo))

ObservationError = R
