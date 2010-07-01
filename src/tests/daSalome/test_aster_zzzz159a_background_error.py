#-*-coding:iso-8859-1-*-
import numpy
parametres = init_data["parametres"]

xb = []
for parametre in parametres:
    xb.append( parametre[1] )

B  = numpy.matrix(numpy.core.identity(len(xb)))
alpha  = 1.e14
B[0,0] = alpha * 100
B[1,1] = alpha * 10
B[2,2] = alpha * 1
dimensionXb = len( xb )
B = numpy.matrix( B, numpy.float ).reshape((dimensionXb,dimensionXb))

BackgroundError = B
