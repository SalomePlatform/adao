#-*-coding:iso-8859-1-*-
#
#  Copyright (C) 2008-2015 EDF R&D
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
from daCore import BasicObjects
import numpy, copy

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
            message  = "Graine fix�e pour le g�n�rateur al�atoire",
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
            message  = "Vitesse de groupe impos�e par l'essaim",
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
            default  = "AugmentedWeightedLeastSquares",
            typecast = str,
            message  = "Crit�re de qualit� utilis�",
            listval  = ["AugmentedWeightedLeastSquares","AWLS","AugmentedPonderatedLeastSquares","APLS","DA",
                        "WeightedLeastSquares","WLS","PonderatedLeastSquares","PLS",
                        "LeastSquares","LS","L2",
                        "AbsoluteValue","L1",
                        "MaximumError","ME"],
            )
        self.defineRequiredParameter(
            name     = "StoreInternalVariables",
            default  = False,
            typecast = bool,
            message  = "Stockage des variables internes ou interm�diaires du calcul",
            )
        self.defineRequiredParameter(
            name     = "StoreSupplementaryCalculations",
            default  = [],
            typecast = tuple,
            message  = "Liste de calculs suppl�mentaires � stocker et/ou effectuer",
            listval  = ["BMA", "OMA", "OMB", "Innovation"]
            )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run()
        #
        # Param�tres de pilotage
        # ----------------------
        self.setParameters(Parameters)
        #
        if self._parameters.has_key("BoxBounds") and (type(self._parameters["BoxBounds"]) is type([]) or type(self._parameters["BoxBounds"]) is type(())) and (len(self._parameters["BoxBounds"]) > 0):
            BoxBounds = self._parameters["BoxBounds"]
            logging.debug("%s Prise en compte des bornes d'incr�ments de param�tres effectuee"%(self._name,))
        else:
            raise ValueError("Particle Swarm Optimization requires bounds on all variables to be given.")
        BoxBounds   = numpy.array(BoxBounds)
        if numpy.isnan(BoxBounds).any():
            raise ValueError("Particle Swarm Optimization requires bounds on all variables increments to be truly given, \"None\" is not allowed. The actual increments bounds are:\n%s"%BoxBounds)
        #
        Phig = float( self._parameters["GroupRecallRate"] )
        Phip = 1. - Phig
        logging.debug("%s Taux de rappel au meilleur insecte du groupe (entre 0 et 1) = %s et � la meilleure position pr�c�dente (son compl�mentaire � 1) = %s"%(self._name, str(Phig), str(Phip)))
        #
        # Op�rateur d'observation
        # -----------------------
        Hm = HO["Direct"].appliedTo
        #
        # Pr�calcul des inversions de B et R
        # ----------------------------------
        BI = B.getI()
        RI = R.getI()
        #
        # D�finition de la fonction-co�t
        # ------------------------------
        def CostFunction(x, QualityMeasure="AugmentedWeightedLeastSquares"):
            _X  = numpy.asmatrix(numpy.ravel( x )).T
            _HX = Hm( _X )
            _HX = numpy.asmatrix(numpy.ravel( _HX )).T
            #
            if QualityMeasure in ["AugmentedWeightedLeastSquares","AWLS","AugmentedPonderatedLeastSquares","APLS","DA"]:
                if BI is None or RI is None:
                    raise ValueError("Background and Observation error covariance matrix has to be properly defined!")
                Jb  = 0.5 * (_X - Xb).T * BI * (_X - Xb)
                Jo  = 0.5 * (Y - _HX).T * RI * (Y - _HX)
            elif QualityMeasure in ["WeightedLeastSquares","WLS","PonderatedLeastSquares","PLS"]:
                if RI is None:
                    raise ValueError("Observation error covariance matrix has to be properly defined!")
                Jb  = 0.
                Jo  = 0.5 * (Y - _HX).T * RI * (Y - _HX)
            elif QualityMeasure in ["LeastSquares","LS","L2"]:
                Jb  = 0.
                Jo  = 0.5 * (Y - _HX).T * (Y - _HX)
            elif QualityMeasure in ["AbsoluteValue","L1"]:
                Jb  = 0.
                Jo  = numpy.sum( numpy.abs(Y - _HX) )
            elif QualityMeasure in ["MaximumError","ME"]:
                Jb  = 0.
                Jo  = numpy.max( numpy.abs(Y - _HX) )
            #
            J   = float( Jb ) + float( Jo )
            #
            if self._parameters["StoreInternalVariables"]:
                self.StoredVariables["CurrentState"].store( _X )
                self.StoredVariables["CostFunctionJb"].store( Jb )
                self.StoredVariables["CostFunctionJo"].store( Jo )
                self.StoredVariables["CostFunctionJ" ].store( J )
            return J
        #
        # Point de d�marrage de l'optimisation : Xini = Xb
        # ------------------------------------
        if type(Xb) is type(numpy.matrix([])):
            Xini = Xb.A1.tolist()
        elif Xb is not None:
            Xini = list(Xb)
        else:
            Xini = numpy.zeros(len(BoxBounds[:,0]))
        #
        # Initialisation des bornes
        # -------------------------
        SpaceUp  = BoxBounds[:,1] + Xini
        SpaceLow = BoxBounds[:,0] + Xini
        nbparam  = len(SpaceUp)
        #
        # Initialisation de l'essaim
        # --------------------------
        LimitVelocity = numpy.abs(SpaceUp-SpaceLow)
        #
        PosInsect = []
        VelocityInsect = []
        for i in range(nbparam) :
            PosInsect.append(numpy.random.uniform(low=SpaceLow[i], high=SpaceUp[i], size=self._parameters["NumberOfInsects"]))
            VelocityInsect.append(numpy.random.uniform(low=-LimitVelocity[i], high=LimitVelocity[i], size=self._parameters["NumberOfInsects"]))
        VelocityInsect = numpy.matrix(VelocityInsect)
        PosInsect = numpy.matrix(PosInsect)
        #
        BestPosInsect = numpy.array(PosInsect)
        qBestPosInsect = []
        Best = copy.copy(SpaceLow)
        qBest = CostFunction(Best,self._parameters["QualityCriterion"])
        #
        for i in range(self._parameters["NumberOfInsects"]):
            insect  = numpy.ravel(PosInsect[:,i])
            quality = CostFunction(insect,self._parameters["QualityCriterion"])
            qBestPosInsect.append(quality)
            if quality < qBest:
                Best  = copy.copy( insect )
                qBest = copy.copy( quality )
        logging.debug("%s Initialisation, Insecte = %s, Qualit� = %s"%(self._name, str(Best), str(qBest)))
        #
        if self._parameters["StoreInternalVariables"]:
            self.StoredVariables["CurrentState"].store( Best )
        self.StoredVariables["CostFunctionJb"].store( 0. )
        self.StoredVariables["CostFunctionJo"].store( 0. )
        self.StoredVariables["CostFunctionJ" ].store( qBest )
        #
        # Minimisation de la fonctionnelle
        # --------------------------------
        for n in range(self._parameters["MaximumNumberOfSteps"]):
            for i in range(self._parameters["NumberOfInsects"]) :
                insect  = numpy.ravel(PosInsect[:,i])
                rp = numpy.random.uniform(size=nbparam)
                rg = numpy.random.uniform(size=nbparam)
                for j in range(nbparam) :
                    VelocityInsect[j,i] = self._parameters["SwarmVelocity"]*VelocityInsect[j,i] +  Phip*rp[j]*(BestPosInsect[j,i]-PosInsect[j,i]) +  Phig*rg[j]*(Best[j]-PosInsect[j,i])
                    PosInsect[j,i] = PosInsect[j,i]+VelocityInsect[j,i]
                quality = CostFunction(insect,self._parameters["QualityCriterion"])
                if quality < qBestPosInsect[i]:
                    BestPosInsect[:,i] = copy.copy( insect )
                    qBestPosInsect[i]  = copy.copy( quality )
                    if quality < qBest :
                        Best  = copy.copy( insect )
                        qBest = copy.copy( quality )
            logging.debug("%s Etape %i, Insecte = %s, Qualit� = %s"%(self._name, n, str(Best), str(qBest)))
            #
            if self._parameters["StoreInternalVariables"]:
                self.StoredVariables["CurrentState"].store( Best )
            self.StoredVariables["CostFunctionJb"].store( 0. )
            self.StoredVariables["CostFunctionJo"].store( 0. )
            self.StoredVariables["CostFunctionJ" ].store( qBest )
        #
        # Obtention de l'analyse
        # ----------------------
        Xa = numpy.asmatrix(numpy.ravel( Best )).T
        #
        self.StoredVariables["Analysis"].store( Xa.A1 )
        #
        # Calculs et/ou stockages suppl�mentaires
        # ---------------------------------------
        if "Innovation" in self._parameters["StoreSupplementaryCalculations"] or "OMB" in self._parameters["StoreSupplementaryCalculations"]:
            d = Y - Hm(Xb)
        if "Innovation" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["Innovation"].store( numpy.ravel(d) )
        if "BMA" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["BMA"].store( numpy.ravel(Xb - Xa) )
        if "OMA" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["OMA"].store( numpy.ravel(Y - Hm(Xa)) )
        if "OMB" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["OMB"].store( numpy.ravel(d) )
        #
        self._post_run(HO)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
