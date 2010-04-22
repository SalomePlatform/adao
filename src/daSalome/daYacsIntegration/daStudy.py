#-*-coding:iso-8859-1-*-

from daCore.AssimilationStudy import AssimilationStudy

class daError(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

class daStudy:

  def __init__(self, name, algorithm):

    self.ADD = AssimilationStudy(name)
    self.ADD.setControls()
    self.ADD.setAlgorithm(choice="Blue")

  def getAssimilationStudy(self):

    return self.ADD

  # Methods to initialize AssimilationStudy

  def setBackgroundType(self, Type):

    if Type == "Vector":
      self.BackgroundType = Type
    else:
      raise daError("[daStudy::setBackgroundType] Type is unkown : " + Type + " Types are : Vector")

  def setBackground(self, Background):

    try:
      self.BackgroundType
    except AttributeError:
      raise daError("[daStudy::setBackground] Type is not defined !")

    if self.BackgroundType == "Vector":
      self.ADD.setBackground(asVector = Background)

  def setBackgroundError(self, BackgroundError):

    self.ADD.setBackgroundError(asCovariance = BackgroundError)

  def setObservationType(self, Type):

    if Type == "Vector":
      self.ObservationType = Type
    else:
      raise daError("[daStudy::setObservationType] Type is unkown : " + Type + " Types are : Vector")

  def setObservation(self, Observation):

    try:
      self.ObservationType
    except AttributeError:
      raise daError("[daStudy::setObservation] Type is not defined !")

    if self.ObservationType == "Vector":
      self.ADD.setObservation(asVector = Observation)

  def setObservationError(self, ObservationError):

    self.ADD.setObservationError(asCovariance = ObservationError)

  def setObservationOperatorType(self, Type):

    if Type == "Matrix":
      self.ObservationOperatorType = Type
    else:
      raise daError("[daStudy::setObservationOperatorType] Type is unkown : " + Type + " Types are : Matrix")

  def setObservationOperator(self, ObservationOperator):

    try:
      self.ObservationOperatorType
    except AttributeError:
      raise daError("[daStudy::setObservationOperator] Type is not defined !")

    if self.ObservationOperatorType == "Matrix":
      self.ADD.setObservationOperator(asMatrix = ObservationOperator)

