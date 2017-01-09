#-*-coding:iso-8859-1-*-
#
# Copyright (C) 2008-2017 EDF R&D
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#
# Author: Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D

import logging
from daCore import BasicObjects
import numpy, math

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "UNSCENTEDKALMANFILTER")
        self.defineRequiredParameter(
            name     = "ConstrainedBy",
            default  = "EstimateProjection",
            typecast = str,
            message  = "Prise en compte des contraintes",
            listval  = ["EstimateProjection"],
            )
        self.defineRequiredParameter(
            name     = "EstimationOf",
            default  = "State",
            typecast = str,
            message  = "Estimation d'etat ou de parametres",
            listval  = ["State", "Parameters"],
            )
        self.defineRequiredParameter(
            name     = "Alpha",
            default  = 1.,
            typecast = float,
            message  = "",
            minval   = 1.e-4,
            maxval   = 1.,
            )
        self.defineRequiredParameter(
            name     = "Beta",
            default  = 2,
            typecast = float,
            message  = "",
            )
        self.defineRequiredParameter(
            name     = "Kappa",
            default  = 0,
            typecast = int,
            message  = "",
            maxval   = 2,
            )
        self.defineRequiredParameter(
            name     = "Reconditioner",
            default  = 1.,
            typecast = float,
            message  = "",
            minval   = 1.e-3,
            maxval   = 1.e+1,
            )
        self.defineRequiredParameter(
            name     = "StoreInternalVariables",
            default  = False,
            typecast = bool,
            message  = "Stockage des variables internes ou intermédiaires du calcul",
            )
        self.defineRequiredParameter(
            name     = "StoreSupplementaryCalculations",
            default  = [],
            typecast = tuple,
            message  = "Liste de calculs supplémentaires à stocker et/ou effectuer",
            listval  = ["APosterioriCorrelations", "APosterioriCovariance", "APosterioriStandardDeviations", "APosterioriVariances", "BMA", "CurrentState", "CostFunctionJ", "CostFunctionJb", "CostFunctionJo", "Innovation"]
            )
        self.defineRequiredParameter( # Pas de type
            name     = "Bounds",
            message  = "Liste des valeurs de bornes",
            )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run()
        #
        # Paramètres de pilotage
        # ----------------------
        self.setParameters(Parameters)
        #
        if self._parameters.has_key("Bounds") and (type(self._parameters["Bounds"]) is type([]) or type(self._parameters["Bounds"]) is type(())) and (len(self._parameters["Bounds"]) > 0):
            Bounds = self._parameters["Bounds"]
            logging.debug("%s Prise en compte des bornes effectuee"%(self._name,))
        else:
            Bounds = None
        if self._parameters["EstimationOf"] == "Parameters":
            self._parameters["StoreInternalVariables"] = True
        #
        L     = Xb.size
        Alpha = self._parameters["Alpha"]
        Beta  = self._parameters["Beta"]
        if self._parameters["Kappa"] == 0:
            if self._parameters["EstimationOf"] == "State":
                Kappa = 0
            elif self._parameters["EstimationOf"] == "Parameters":
                Kappa = 3 - L
        else:
            Kappa = self._parameters["Kappa"]
        Lambda = float( Alpha**2 ) * ( L + Kappa ) - L
        Gamma  = math.sqrt( L + Lambda )
        #
        Ww = []
        Ww.append( 0. )
        for i in range(2*L):
            Ww.append( 1. / (2.*(L + Lambda)) )
        #
        Wm = numpy.array( Ww )
        Wm[0] = Lambda / (L + Lambda)
        Wc = numpy.array( Ww )
        Wc[0] = Lambda / (L + Lambda) + (1. - Alpha**2 + Beta)
        #
        # Opérateurs
        # ----------
        if B is None:
            raise ValueError("Background error covariance matrix has to be properly defined!")
        if R is None:
            raise ValueError("Observation error covariance matrix has to be properly defined!")
        #
        H = HO["Direct"].appliedControledFormTo
        #
        if self._parameters["EstimationOf"] == "State":
            M = EM["Direct"].appliedControledFormTo
        #
        if CM is not None and CM.has_key("Tangent") and U is not None:
            Cm = CM["Tangent"].asMatrix(Xb)
        else:
            Cm = None
        #
        # Nombre de pas identique au nombre de pas d'observations
        # -------------------------------------------------------
        if hasattr(Y,"stepnumber"):
            duration = Y.stepnumber()
        else:
            duration = 2
        #
        # Précalcul des inversions de B et R
        # ----------------------------------
        if self._parameters["StoreInternalVariables"]:
            BI = B.getI()
            RI = R.getI()
        #
        # Initialisation
        # --------------
        Xn = Xb
        if hasattr(B,"asfullmatrix"):
            Pn = B.asfullmatrix(Xn.size)
        else:
            Pn = B
        #
        self.StoredVariables["Analysis"].store( Xn.A1 )
        if "APosterioriCovariance" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["APosterioriCovariance"].store( Pn )
            covarianceXa = Pn
        Xa               = Xn
        previousJMinimum = numpy.finfo(float).max
        #
        for step in range(duration-1):
            if hasattr(Y,"store"):
                Ynpu = numpy.asmatrix(numpy.ravel( Y[step+1] )).T
            else:
                Ynpu = numpy.asmatrix(numpy.ravel( Y )).T
            #
            if U is not None:
                if hasattr(U,"store") and len(U)>1:
                    Un = numpy.asmatrix(numpy.ravel( U[step] )).T
                elif hasattr(U,"store") and len(U)==1:
                    Un = numpy.asmatrix(numpy.ravel( U[0] )).T
                else:
                    Un = numpy.asmatrix(numpy.ravel( U )).T
            else:
                Un = None
            #
            Pndemi = numpy.linalg.cholesky(Pn)
            Xnp = numpy.hstack([Xn, Xn+Gamma*Pndemi, Xn-Gamma*Pndemi])
            nbSpts = 2*Xn.size+1
            #
            if Bounds is not None and self._parameters["ConstrainedBy"] == "EstimateProjection":
                for point in range(nbSpts):
                    Xnp[:,point] = numpy.max(numpy.hstack((Xnp[:,point],numpy.asmatrix(Bounds)[:,0])),axis=1)
                    Xnp[:,point] = numpy.min(numpy.hstack((Xnp[:,point],numpy.asmatrix(Bounds)[:,1])),axis=1)
            #
            XEtnnp = []
            for point in range(nbSpts):
                if self._parameters["EstimationOf"] == "State":
                    XEtnnpi = numpy.asmatrix(numpy.ravel( M( (Xnp[:,point], Un) ) )).T
                    if Cm is not None and Un is not None: # Attention : si Cm est aussi dans M, doublon !
                        Cm = Cm.reshape(Xn.size,Un.size) # ADAO & check shape
                        XEtnnpi = XEtnnpi + Cm * Un
                    if Bounds is not None and self._parameters["ConstrainedBy"] == "EstimateProjection":
                        XEtnnpi = numpy.max(numpy.hstack((XEtnnpi,numpy.asmatrix(Bounds)[:,0])),axis=1)
                        XEtnnpi = numpy.min(numpy.hstack((XEtnnpi,numpy.asmatrix(Bounds)[:,1])),axis=1)
                elif self._parameters["EstimationOf"] == "Parameters":
                    # --- > Par principe, M = Id, Q = 0
                    XEtnnpi = Xnp[:,point]
                XEtnnp.append( XEtnnpi )
            XEtnnp = numpy.hstack( XEtnnp )
            #
            Xncm = numpy.matrix( XEtnnp.getA()*numpy.array(Wm) ).sum(axis=1)
            #
            if Bounds is not None and self._parameters["ConstrainedBy"] == "EstimateProjection":
                Xncm = numpy.max(numpy.hstack((Xncm,numpy.asmatrix(Bounds)[:,0])),axis=1)
                Xncm = numpy.min(numpy.hstack((Xncm,numpy.asmatrix(Bounds)[:,1])),axis=1)
            #
            if self._parameters["EstimationOf"] == "State":        Pnm = Q
            elif self._parameters["EstimationOf"] == "Parameters": Pnm = 0.
            for point in range(nbSpts):
                Pnm += Wc[i] * (XEtnnp[:,point]-Xncm) * (XEtnnp[:,point]-Xncm).T
            #
            if self._parameters["EstimationOf"] == "Parameters" and Bounds is not None:
                Pnmdemi = self._parameters["Reconditioner"] * numpy.linalg.cholesky(Pnm)
            else:
                Pnmdemi = numpy.linalg.cholesky(Pnm)
            #
            Xnnp = numpy.hstack([Xncm, Xncm+Gamma*Pnmdemi, Xncm-Gamma*Pnmdemi])
            #
            if Bounds is not None and self._parameters["ConstrainedBy"] == "EstimateProjection":
                for point in range(nbSpts):
                    Xnnp[:,point] = numpy.max(numpy.hstack((Xnnp[:,point],numpy.asmatrix(Bounds)[:,0])),axis=1)
                    Xnnp[:,point] = numpy.min(numpy.hstack((Xnnp[:,point],numpy.asmatrix(Bounds)[:,1])),axis=1)
            #
            Ynnp = []
            for point in range(nbSpts):
                if self._parameters["EstimationOf"] == "State":
                    Ynnpi = numpy.asmatrix(numpy.ravel( H( (Xnnp[:,point], None) ) )).T
                elif self._parameters["EstimationOf"] == "Parameters":
                    Ynnpi = numpy.asmatrix(numpy.ravel( H( (Xnnp[:,point], Un) ) )).T
                Ynnp.append( Ynnpi )
            Ynnp = numpy.hstack( Ynnp )
            #
            Yncm = numpy.matrix( Ynnp.getA()*numpy.array(Wm) ).sum(axis=1)
            #
            Pyyn = R
            Pxyn = 0.
            for point in range(nbSpts):
                Pyyn += Wc[i] * (Ynnp[:,point]-Yncm) * (Ynnp[:,point]-Yncm).T
                Pxyn += Wc[i] * (Xnnp[:,point]-Xncm) * (Ynnp[:,point]-Yncm).T
            #
            d  = Ynpu - Yncm
            if self._parameters["EstimationOf"] == "Parameters":
                if Cm is not None and Un is not None: # Attention : si Cm est aussi dans H, doublon !
                    d = d - Cm * Un
            #
            Kn = Pxyn * Pyyn.I
            Xn = Xncm + Kn * d
            Pn = Pnm - Kn * Pyyn * Kn.T
            #
            if Bounds is not None and self._parameters["ConstrainedBy"] == "EstimateProjection":
                Xn = numpy.max(numpy.hstack((Xn,numpy.asmatrix(Bounds)[:,0])),axis=1)
                Xn = numpy.min(numpy.hstack((Xn,numpy.asmatrix(Bounds)[:,1])),axis=1)
            #
            self.StoredVariables["Analysis"].store( Xn.A1 )
            if "APosterioriCovariance" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["APosterioriCovariance"].store( Pn )
            if "Innovation" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["Innovation"].store( numpy.ravel( d.A1 ) )
            if self._parameters["StoreInternalVariables"]:
                Jb  = 0.5 * (Xn - Xb).T * BI * (Xn - Xb)
                Jo  = 0.5 * d.T * RI * d
                J   = float( Jb ) + float( Jo )
                if self._parameters["StoreInternalVariables"] or "CurrentState" in self._parameters["StoreSupplementaryCalculations"]:
                    self.StoredVariables["CurrentState"].store( Xn )
                self.StoredVariables["CostFunctionJb"].store( Jb )
                self.StoredVariables["CostFunctionJo"].store( Jo )
                self.StoredVariables["CostFunctionJ" ].store( J )
                if J < previousJMinimum:
                    previousJMinimum  = J
                    Xa                = Xn
                    if "APosterioriCovariance" in self._parameters["StoreSupplementaryCalculations"]:
                        covarianceXa  = Pn
            else:
                Xa = Xn
            #
        #
        # Stockage supplementaire de l'optimum en estimation de parametres
        # ----------------------------------------------------------------
        if self._parameters["EstimationOf"] == "Parameters":
            self.StoredVariables["Analysis"].store( Xa.A1 )
            if "APosterioriCovariance" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["APosterioriCovariance"].store( covarianceXa )
        #
        if "BMA" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(Xa) )
        #
        self._post_run(HO)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
