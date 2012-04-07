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

import logging
from daCore import BasicObjects, PlatformInfo
m = PlatformInfo.SystemUsage()

import numpy

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self)
        self._name = "QUANTILEREGRESSION"
        logging.debug("%s Initialisation"%self._name)

    def run(self, Xb=None, Y=None, H=None, M=None, R=None, B=None, Q=None, Parameters=None):
        """
        Calcul des parametres definissant le quantile
        """
        logging.debug("%s Lancement"%self._name)
        logging.debug("%s Taille mémoire utilisée de %.1f Mo"%(self._name, m.getUsedMemory("Mo")))
        #
        # Opérateur d'observation
        # -----------------------
        Hm = H["Direct"].appliedTo
        Ht = H["Adjoint"].appliedInXTo
        #
        # Utilisation éventuelle d'un vecteur H(Xb) précalculé
        # ----------------------------------------------------
        if H["AppliedToX"] is not None and H["AppliedToX"].has_key("HXb"):
            logging.debug("%s Utilisation de HXb"%self._name)
            HXb = H["AppliedToX"]["HXb"]
        else:
            logging.debug("%s Calcul de Hm(Xb)"%self._name)
            HXb = Hm( Xb )
        HXb = numpy.asmatrix(HXb).flatten().T
        #
        # Calcul de l'innovation
        # ----------------------
        if Y.size != HXb.size:
            raise ValueError("The size %i of observations Y and %i of observed calculation H(X) are different, they have to be identical."%(Y.size,HXb.size))
        if max(Y.shape) != max(HXb.shape):
            raise ValueError("The shapes %s of observations Y and %s of observed calculation H(X) are different, they have to be identical."%(Y.shape,HXb.shape))
        d  = Y - HXb
        logging.debug("%s Innovation d = %s"%(self._name, d))
        #
        # Définition de la fonction-coût
        # ------------------------------
        def CostFunction(x):
            _X  = numpy.asmatrix(x).flatten().T
            logging.debug("%s CostFunction X  = %s"%(self._name, numpy.asmatrix( _X ).flatten()))
            _HX = Hm( _X )
            _HX = numpy.asmatrix(_HX).flatten().T
            Jb  = 0.
            Jo  = 0.
            J   = Jb + Jo
            logging.debug("%s CostFunction Jb = %s"%(self._name, Jb))
            logging.debug("%s CostFunction Jo = %s"%(self._name, Jo))
            logging.debug("%s CostFunction J  = %s"%(self._name, J))
            self.StoredVariables["CurrentState"].store( _X.A1 )
            self.StoredVariables["CostFunctionJb"].store( Jb )
            self.StoredVariables["CostFunctionJo"].store( Jo )
            self.StoredVariables["CostFunctionJ" ].store( J )
            return _HX
        #
        def GradientOfCostFunction(x):
            _X      = numpy.asmatrix(x).flatten().T
            logging.debug("%s GradientOfCostFunction X      = %s"%(self._name, numpy.asmatrix( _X ).flatten()))
            Hg = H["Tangent"].asMatrix( _X )
            return Hg
        #
        # Point de démarrage de l'optimisation : Xini = Xb
        # ------------------------------------
        if type(Xb) is type(numpy.matrix([])):
            Xini = Xb.A1.tolist()
        else:
            Xini = list(Xb)
        logging.debug("%s Point de démarrage Xini = %s"%(self._name, Xini))
        #
        # Paramètres de pilotage
        # ----------------------
        # Potentiels : "Quantile", "Minimizer", "MaximumNumberOfSteps", "CostDecrementTolerance"
        if Parameters.has_key("Quantile") and (0. <= Parameters["Quantile"] <= 1.):
            quantile = float(Parameters["Quantile"])
        else:
            quantile = 0.5
        logging.debug("%s Quantile pour la regression de quantile = %s"%(self._name, str(quantile)))
        MinimizerList = ["MMQR",]
        if Parameters.has_key("Minimizer") and (Parameters["Minimizer"] in MinimizerList):
            Minimizer = str( Parameters["Minimizer"] )
        else:
            Minimizer = "MMQR"
            logging.warning("%s Unknown or undefined minimizer, replaced by the default one \"%s\""%(self._name,Minimizer))
        logging.debug("%s Minimiseur utilisé = %s"%(self._name, Minimizer))
        if Parameters.has_key("MaximumNumberOfSteps") and (Parameters["MaximumNumberOfSteps"] > -1):
            maxiter = int( Parameters["MaximumNumberOfSteps"] )
        else:
            maxiter = 15000
        logging.debug("%s Nombre maximal de pas d'optimisation = %s"%(self._name, str(maxiter)))
        if Parameters.has_key("CostDecrementTolerance") and (Parameters["CostDecrementTolerance"] > 0):
            ftol = float(Parameters["CostDecrementTolerance"])
        else:
            ftol = 1.e-06
        logging.debug("%s Maximum de variation de la fonction d'estimation lors de l'arrêt = %s"%(self._name, str(ftol)))
        #
        # Minimisation de la fonctionnelle
        # --------------------------------
        if Minimizer == "MMQR":
            import mmqr
            Minimum, J_optimal, Informations = mmqr.mmqr(
                func        = CostFunction,
                x0          = Xini,
                fprime      = GradientOfCostFunction,
                quantile    = quantile,
                maxfun      = maxiter,
                toler       = ftol,
                y           = Y,
                )
            nfeval = Informations[2]
            rc     = Informations[4]
        else:
            raise ValueError("Error in Minimizer name: %s"%Minimizer)
        #
        logging.debug("%s %s Step of min cost  = %s"%(self._name, Minimizer, nfeval))
        logging.debug("%s %s Minimum cost      = %s"%(self._name, Minimizer, J_optimal))
        logging.debug("%s %s Minimum state     = %s"%(self._name, Minimizer, Minimum))
        logging.debug("%s %s Nb of F           = %s"%(self._name, Minimizer, nfeval))
        logging.debug("%s %s RetCode           = %s"%(self._name, Minimizer, rc))
        #
        # Obtention de l'analyse
        # ----------------------
        Xa = numpy.asmatrix(Minimum).T
        logging.debug("%s Analyse Xa = %s"%(self._name, Xa))
        #
        self.StoredVariables["Analysis"].store( Xa.A1 )
        self.StoredVariables["Innovation"].store( d.A1 )
        #
        logging.debug("%s Taille mémoire utilisée de %.1f Mo"%(self._name, m.getUsedMemory("MB")))
        logging.debug("%s Terminé"%self._name)
        #
        return 0

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
