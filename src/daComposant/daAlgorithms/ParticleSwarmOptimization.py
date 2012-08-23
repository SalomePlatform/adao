#-*-coding:iso-8859-1-*-
#
#  Copyright (C) 2008-2012 EDF R&D
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
#  See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#
#  Author: Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D

import logging
from daCore import BasicObjects, PlatformInfo
m = PlatformInfo.SystemUsage()

import numpy
import copy

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "PARTICLESWARMOPTIMIZATION")
        self.defineRequiredParameter(
            name     = "MaximumNumberOfSteps",
            default  = 50,
            typecast = int,
            message  = "Nombre maximal de pas d'optimisation",
            minval   = 1,
            )
        self.defineRequiredParameter(
            name     = "SetSeed",
            typecast = numpy.random.seed,
            message  = "Graine fixée pour le générateur aléatoire",
            )
        self.defineRequiredParameter(
            name     = "NumberOfInsects",
            default  = 100,
            typecast = int,
            message  = "Nombre d'insectes dans l'essaim",
            minval   = -1,
            )
        self.defineRequiredParameter(
            name     = "SwarmVelocity",
            default  = 1.,
            typecast = float,
            message  = "Vitesse de groupe imposée par l'essaim",
            minval   = 0.,
            )
        self.defineRequiredParameter(
            name     = "GroupRecallRate",
            default  = 0.5,
            typecast = float,
            message  = "Taux de rappel au meilleur insecte du groupe (entre 0 et 1)",
            minval   = 0.,
            maxval   = 1.,
            )
        self.defineRequiredParameter(
            name     = "QualityCriterion",
            default  = "AugmentedPonderatedLeastSquares",
            typecast = str,
            message  = "Critère de qualité utilisé",
            listval  = ["AugmentedPonderatedLeastSquares","APLS","DA",
                        "PonderatedLeastSquares","PLS",
                        "LeastSquares","LS","L2",
                        "AbsoluteValue","L1",
                        "MaximumError","ME"],
            )
        self.defineRequiredParameter(
            name     = "StoreInternalVariables",
            default  = False,
            typecast = bool,
            message  = "Stockage des variables internes ou intermédiaires du calcul",
            )

    def run(self, Xb=None, Y=None, H=None, M=None, R=None, B=None, Q=None, Parameters=None):
        """
        Calcul de l'estimateur
        """
        logging.debug("%s Lancement"%self._name)
        logging.debug("%s Taille mémoire utilisée de %.1f Mo"%(self._name, m.getUsedMemory("M")))
        #
        # Paramètres de pilotage
        # ----------------------
        self.setParameters(Parameters)
        #
        if self._parameters.has_key("BoxBounds") and (type(self._parameters["BoxBounds"]) is type([]) or type(self._parameters["BoxBounds"]) is type(())) and (len(self._parameters["BoxBounds"]) > 0):
            BoxBounds = self._parameters["BoxBounds"]
            logging.debug("%s Prise en compte des bornes d'incréments de paramètres effectuee"%(self._name,))
        else:
            raise ValueError("Particle Swarm Optimization requires bounds on all variables to be given.")
        BoxBounds   = numpy.array(BoxBounds)
        if numpy.isnan(BoxBounds).any():
            raise ValueError("Particle Swarm Optimization requires bounds on all variables increments to be truly given, \"None\" is not allowed. The actual increments bounds are:\n%s"%BoxBounds)
        #
        Phig = float( self._parameters["GroupRecallRate"] )
        Phip = 1. - Phig
        logging.debug("%s Taux de rappel au meilleur insecte du groupe (entre 0 et 1) = %s et à la meilleure position précédente (son complémentaire à 1) = %s"%(self._name, str(Phig), str(Phip)))
        #
        # Opérateur d'observation
        # -----------------------
        Hm = H["Direct"].appliedTo
        #
        # Précalcul des inversions de B et R
        # ----------------------------------
        if B is not None:
            BI = B.I
        elif self._parameters["B_scalar"] is not None:
            BI = 1.0 / self._parameters["B_scalar"]
        else:
            BI = None
        #
        if R is not None:
            RI = R.I
        elif self._parameters["R_scalar"] is not None:
            RI = 1.0 / self._parameters["R_scalar"]
        else:
            RI = None
        #
        # Définition de la fonction-coût
        # ------------------------------
        def CostFunction(x, QualityMeasure="AugmentedPonderatedLeastSquares"):
            _X  = numpy.asmatrix(x).flatten().T
            logging.debug("%s CostFunction X  = %s"%(self._name, _X.A1))
            _HX = Hm( _X )
            _HX = numpy.asmatrix(_HX).flatten().T
            #
            if QualityMeasure in ["AugmentedPonderatedLeastSquares","APLS","DA"]:
                if BI is None or RI is None:
                    raise ValueError("Background and Observation error covariance matrix has to be properly defined!")
                Jb  = 0.5 * (_X - Xb).T * BI * (_X - Xb)
                Jo  = 0.5 * (Y - _HX).T * RI * (Y - _HX)
                J   = float( Jb ) + float( Jo )
            elif QualityMeasure in ["PonderatedLeastSquares","PLS"]:
                if RI is None:
                    raise ValueError("Observation error covariance matrix has to be properly defined!")
                Jb  = 0.
                Jo  = 0.5 * (Y - _HX).T * RI * (Y - _HX)
                J   = float( Jb ) + float( Jo )
            elif QualityMeasure in ["LeastSquares","LS","L2"]:
                Jb  = 0.
                Jo  = 0.5 * (Y - _HX).T * (Y - _HX)
                J   = float( Jb ) + float( Jo )
            elif QualityMeasure in ["AbsoluteValue","L1"]:
                Jb  = 0.
                Jo  = numpy.sum( numpy.abs(Y - _HX) )
                J   = float( Jb ) + float( Jo )
            elif QualityMeasure in ["MaximumError","ME"]:
                Jb  = 0.
                Jo  = numpy.max( numpy.abs(Y - _HX) )
                J   = float( Jb ) + float( Jo )
            #
            logging.debug("%s CostFunction Jb = %s"%(self._name, Jb))
            logging.debug("%s CostFunction Jo = %s"%(self._name, Jo))
            logging.debug("%s CostFunction J  = %s"%(self._name, J))
            return J
        #
        # Point de démarrage de l'optimisation : Xini = Xb
        # ------------------------------------
        if type(Xb) is type(numpy.matrix([])):
            Xini = Xb.A1.tolist()
        elif Xb is not None:
            Xini = list(Xb)
        else:
            Xini = numpy.zeros(len(BoxBounds[:,0]))
        logging.debug("%s Point de démarrage Xini = %s"%(self._name, Xini))
        #
        # Initialisation des bornes
        # -------------------------
        SpaceUp  = BoxBounds[:,1] + Xini
        Spacelow = BoxBounds[:,0] + Xini
        nbparam  = len(SpaceUp)
        #
        # Initialisation de l'essaim
        # --------------------------
        LimitVelocity = numpy.abs(SpaceUp-Spacelow)
        #
        PosInsect = []
        VelocityInsect = []
        for i in range(nbparam) :
            PosInsect.append(numpy.random.uniform(low=Spacelow[i], high=SpaceUp[i], size=self._parameters["NumberOfInsects"]))
            VelocityInsect.append(numpy.random.uniform(low=-LimitVelocity[i], high=LimitVelocity[i], size=self._parameters["NumberOfInsects"]))
        VelocityInsect = numpy.matrix(VelocityInsect)
        PosInsect = numpy.matrix(PosInsect)
        #
        BestPosInsect = numpy.array(PosInsect)
        qBestPosInsect = []
        Best = copy.copy(Spacelow)
        qBest = CostFunction(Best,self._parameters["QualityCriterion"])
        #
        for i in range(self._parameters["NumberOfInsects"]):
            insect  = numpy.array(PosInsect[:,i].A1)
            quality = CostFunction(insect,self._parameters["QualityCriterion"])
            qBestPosInsect.append(quality)
            if quality < qBest:
                Best  = insect
                qBest = quality
        #
        # Minimisation de la fonctionnelle
        # --------------------------------
        for n in range(self._parameters["MaximumNumberOfSteps"]):
            for i in range(self._parameters["NumberOfInsects"]) :
                insect  = PosInsect[:,i]
                rp = numpy.random.uniform(size=nbparam)
                rg = numpy.random.uniform(size=nbparam)
                for j in range(nbparam) :
                    VelocityInsect[j,i] = self._parameters["SwarmVelocity"]*VelocityInsect[j,i] +  Phip*rp[j]*(BestPosInsect[j,i]-PosInsect[j,i]) +  Phig*rg[j]*(Best[j]-PosInsect[j,i])
                    PosInsect[j,i] = PosInsect[j,i]+VelocityInsect[j,i]
                quality = CostFunction(insect,self._parameters["QualityCriterion"])
                if quality < qBestPosInsect[i]:
                    BestPosInsect[:,i] = numpy.asmatrix(insect).flatten().A1
                    if quality < qBest :
                        Best  = numpy.asmatrix(insect).flatten().A1
                        qBest = quality
            logging.debug("%s Iteration %i : qBest = %.5f, Best = %s"%(self._name, n+1,qBest,Best))
            #
            if self._parameters["StoreInternalVariables"]:
                self.StoredVariables["CurrentState"].store( Best )
            self.StoredVariables["CostFunctionJb"].store( 0. )
            self.StoredVariables["CostFunctionJo"].store( 0. )
            self.StoredVariables["CostFunctionJ" ].store( qBest )
        #
        logging.debug("%s %s Step of min cost  = %s"%(self._name, self._parameters["QualityCriterion"], self._parameters["MaximumNumberOfSteps"]))
        logging.debug("%s %s Minimum cost      = %s"%(self._name, self._parameters["QualityCriterion"], qBest))
        logging.debug("%s %s Minimum state     = %s"%(self._name, self._parameters["QualityCriterion"], Best))
        logging.debug("%s %s Nb of F           = %s"%(self._name, self._parameters["QualityCriterion"], (self._parameters["MaximumNumberOfSteps"]+1)*self._parameters["NumberOfInsects"]+1))
        logging.debug("%s %s RetCode           = %s"%(self._name, self._parameters["QualityCriterion"], 0))
        #
        # Obtention de l'analyse
        # ----------------------
        Xa = numpy.asmatrix(Best).flatten().T
        logging.debug("%s Analyse Xa = %s"%(self._name, Xa))
        #
        self.StoredVariables["Analysis"].store( Xa.A1 )
        #
        logging.debug("%s Taille mémoire utilisée de %.1f Mo"%(self._name, m.getUsedMemory("M")))
        logging.debug("%s Terminé"%self._name)
        #
        return 0

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
