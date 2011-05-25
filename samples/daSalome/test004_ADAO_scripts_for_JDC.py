#-*-coding:iso-8859-1-*-
import numpy
#
n = 100
#
# Definition of the Background as a vector
# ----------------------------------------
Background = n * [0]
#
# Definition of the Observation as a vector
# -----------------------------------------
Observation = n * "1 "
Observation = Observation.strip()
#
# Definition of the Background Error covariance as a matrix
# ---------------------------------------------------------
BackgroundError = numpy.identity(n)
#
# Definition of the Observation Error covariance as a matrix
# ----------------------------------------------------------
ObservationError = numpy.identity(n)
#
# Definition of the Observation Operator as a matrix
# --------------------------------------------------
ObservationOperator = numpy.identity(n)
