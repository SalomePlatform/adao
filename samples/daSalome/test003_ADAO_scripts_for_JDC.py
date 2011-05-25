#-*-coding:iso-8859-1-*-
import numpy
#
# Definition of the Background as a vector
# ----------------------------------------
Background = [0, 0, 0]
#
# Definition of the Observation as a vector
# -----------------------------------------
Observation = "1 1 1"
#
# Definition of the Background Error covariance as a matrix
# ---------------------------------------------------------
BackgroundError = numpy.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])
#
# Definition of the Observation Error covariance as a matrix
# ----------------------------------------------------------
ObservationError = numpy.matrix("1 0 0 ; 0 1 0 ; 0 0 1")
#
# Definition of the Observation Operator as a matrix
# --------------------------------------------------
ObservationOperator = numpy.identity(3)
