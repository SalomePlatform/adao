#-*-coding:iso-8859-1-*-
#
#  Copyright (C) 2008-2013 EDF R&D
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

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "ADJOINTTEST")
        self.defineRequiredParameter(
            name     = "ResiduFormula",
            default  = "ScalarProduct",
            typecast = str,
            message  = "Formule de résidu utilisée",
            listval  = ["ScalarProduct"],
            )
        self.defineRequiredParameter(
            name     = "EpsilonMinimumExponent",
            default  = -8,
            typecast = int,
            message  = "Exposant minimal en puissance de 10 pour le multiplicateur d'incrément",
            minval   = -20,
            maxval   = 0,
            )
        self.defineRequiredParameter(
            name     = "InitialDirection",
            default  = [],
            typecast = list,
            message  = "Direction initiale de la dérivée directionnelle autour du point nominal",
            )
        self.defineRequiredParameter(
            name     = "AmplitudeOfInitialDirection",
            default  = 1.,
            typecast = float,
            message  = "Amplitude de la direction initiale de la dérivée directionnelle autour du point nominal",
            )
        self.defineRequiredParameter(
            name     = "SetSeed",
            typecast = numpy.random.seed,
            message  = "Graine fixée pour le générateur aléatoire",
            )
        self.defineRequiredParameter(
            name     = "ResultTitle",
            default  = "",
            typecast = str,
            message  = "Titre du tableau et de la figure",
            )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        logging.debug("%s Lancement"%self._name)
        logging.debug("%s Taille mémoire utilisée de %.1f Mo"%(self._name, m.getUsedMemory("M")))
        #
        self.setParameters(Parameters)
        #
        Hm = HO["Direct"].appliedTo
        Ht = HO["Tangent"].appliedInXTo
        Ha = HO["Adjoint"].appliedInXTo
        #
        # ----------
        Perturbations = [ 10**i for i in xrange(self._parameters["EpsilonMinimumExponent"],1) ]
        Perturbations.reverse()
        #
        X       = numpy.asmatrix(numpy.ravel( Xb )).T
        NormeX  = numpy.linalg.norm( X )
        if Y is None:
            Y = numpy.asmatrix(numpy.ravel( Hm( X ) )).T
        Y = numpy.asmatrix(numpy.ravel( Y )).T
        NormeY = numpy.linalg.norm( Y )
        #
        if len(self._parameters["InitialDirection"]) == 0:
            dX0 = []
            for v in X.A1:
                if abs(v) > 1.e-8:
                    dX0.append( numpy.random.normal(0.,abs(v)) )
                else:
                    dX0.append( numpy.random.normal(0.,X.mean()) )
        else:
            dX0 = numpy.asmatrix(numpy.ravel( self._parameters["InitialDirection"] ))
        #
        dX0 = float(self._parameters["AmplitudeOfInitialDirection"]) * numpy.matrix( dX0 ).T
        #
        # Entete des resultats
        # --------------------
        __marge =  12*" "
        if self._parameters["ResiduFormula"] == "ScalarProduct":
            __entete = "  i   Alpha     ||X||       ||Y||       ||dX||        R(Alpha)  "
            __msgdoc = """
            On observe le residu qui est la difference de deux produits scalaires :

              R(Alpha) = | < TangentF_X(dX) , Y > - < dX , AdjointF_X(Y) > |

            qui doit rester constamment egal zero a la precision du calcul.
            On prend dX0 = Normal(0,X) et dX = Alpha*dX0. F est le code de calcul.
            Y doit etre dans l'image de F. S'il n'est pas donne, on prend Y = F(X).
            """
        #
        if len(self._parameters["ResultTitle"]) > 0:
            msgs  = "\n"
            msgs += __marge + "====" + "="*len(self._parameters["ResultTitle"]) + "====\n"
            msgs += __marge + "    " + self._parameters["ResultTitle"] + "\n"
            msgs += __marge + "====" + "="*len(self._parameters["ResultTitle"]) + "====\n"
        else:
            msgs  = ""
        msgs += __msgdoc
        #
        __nbtirets = len(__entete)
        msgs += "\n" + __marge + "-"*__nbtirets
        msgs += "\n" + __marge + __entete
        msgs += "\n" + __marge + "-"*__nbtirets
        #
        Normalisation= -1
        #
        # ----------
        for i,amplitude in enumerate(Perturbations):
            dX          = amplitude * dX0
            NormedX     = numpy.linalg.norm( dX )
            #
            TangentFXdX = numpy.asmatrix( Ht( (X,dX) ) )
            AdjointFXY  = numpy.asmatrix( Ha( (X,Y)  ) )
            #
            Residu = abs(float(numpy.dot( TangentFXdX.A1 , Y.A1 ) - numpy.dot( dX.A1 , AdjointFXY.A1 )))
            #
            msg = "  %2i  %5.0e   %9.3e   %9.3e   %9.3e   |  %9.3e"%(i,amplitude,NormeX,NormeY,NormedX,Residu)
            msgs += "\n" + __marge + msg
            #
            self.StoredVariables["CostFunctionJ"].store( Residu )
        #
        msgs += "\n" + __marge + "-"*__nbtirets
        msgs += "\n"
        #
        # Sorties eventuelles
        # -------------------
        print
        print "Results of adjoint check by \"%s\" formula:"%self._parameters["ResiduFormula"]
        print msgs
        #
        logging.debug("%s Nombre d'évaluation(s) de l'opérateur d'observation direct/tangent/adjoint : %i/%i/%i"%(self._name, HO["Direct"].nbcalls()[0],HO["Tangent"].nbcalls()[0],HO["Adjoint"].nbcalls()[0]))
        logging.debug("%s Taille mémoire utilisée de %.1f Mo"%(self._name, m.getUsedMemory("M")))
        logging.debug("%s Terminé"%self._name)
        #
        return 0

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
