#-*-coding:iso-8859-1-*-

from daCore.AssimilationStudy import AssimilationStudy

class daStudy:

  def __init__(self, name, algorithm):

    self.ADD = AssimilationStudy(name)
    self.ADD.setControls()
    self.ADD.setAlgorithm(choice="Blue")

  def getAssimilationStudy():
    return self.ADD
