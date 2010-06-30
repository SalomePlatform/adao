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
    self.algorithm = algorithm
    self.algorithm_dict = None
    self.Background = None

    # Observation Management
    self.ObservationOperatorType = {}
    self.FunctionObservationOperator = {}

  def setAlgorithmParameters(self, parameters):
    self.algorithm_dict = parameters

  def initAlgorithm(self):

    self.ADD.setAlgorithm(choice=self.algorithm)
    if self.algorithm_dict != None:
      self.ADD.setAlgorithmParameters(asDico=self.algorithm_dict)

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

    self.Background = Background

    if self.BackgroundType == "Vector":
      self.ADD.setBackground(asVector = Background)

  def getBackground(self):
    return self.Background

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


  def getObservationOperatorType(self, Name):
    rtn = None
    try:
      rtn = self.ObservationOperatorType[Name]
    except:
      pass
    return rtn

  def setObservationOperatorType(self, Name, Type):
    if Type == "Matrix":
      self.ObservationOperatorType[Name] = Type
    elif Type == "Function":
      self.ObservationOperatorType[Name] = Type
    else:
      raise daError("[daStudy::setObservationOperatorType] Type is unkown : " + Type + " Types are : Matrix")

  def setObservationOperator(self, Name, ObservationOperator):
    try:
      self.ObservationOperatorType[Name]
    except AttributeError:
      raise daError("[daStudy::setObservationOperator] Type is not defined !")

    if self.ObservationOperatorType[Name] == "Matrix":
      self.ADD.setObservationOperator(asMatrix = ObservationOperator)
    elif self.ObservationOperatorType[Name] == "Function":
      self.FunctionObservationOperator[Name] = ObservationOperator

