import numpy

numpy.random.seed(1000)
dimension = 300

xt = numpy.matrix(numpy.arange(dimension)).T
Eo = numpy.matrix(numpy.zeros((dimension,))).T
Eb = numpy.matrix(numpy.random.normal(0.,1.,size=(dimension,))).T
H  = numpy.matrix(numpy.core.identity(dimension))
B = numpy.matrix(numpy.core.identity(dimension)).T
R = numpy.matrix(numpy.core.identity(dimension)).T

def FunctionH( X ):
    return H * X

xb = xt + Eb
xb = xb.A1
yo = FunctionH( xt ) + Eo
yo = yo.A1

Background = xb
BackgroundError = B
Observation = yo
ObservationError = R
