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
import numpy, scipy.optimize

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "3DVAR")
        self.defineRequiredParameter(
            name     = "Minimizer",
            default  = "LBFGSB",
            typecast = str,
            message  = "Minimiseur utilisé",
            listval  = ["LBFGSB","TNC", "CG", "NCG", "BFGS"],
            )
        self.defineRequiredParameter(
            name     = "MaximumNumberOfSteps",
            default  = 15000,
            typecast = int,
            message  = "Nombre maximal de pas d'optimisation",
            minval   = -1,
            )
        self.defineRequiredParameter(
            name     = "CostDecrementTolerance",
            default  = 1.e-7,
            typecast = float,
            message  = "Diminution relative minimale du cout lors de l'arrêt",
            )
        self.defineRequiredParameter(
            name     = "ProjectedGradientTolerance",
            default  = -1,
            typecast = float,
            message  = "Maximum des composantes du gradient projeté lors de l'arrêt",
            minval   = -1,
            )
        self.defineRequiredParameter(
            name     = "GradientNormTolerance",
            default  = 1.e-05,
            typecast = float,
            message  = "Maximum des composantes du gradient lors de l'arrêt",
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
            listval  = ["APosterioriCorrelations", "APosterioriCovariance", "APosterioriStandardDeviations", "APosterioriVariances", "BMA", "OMA", "OMB", "CostFunctionJ", "CurrentState", "CurrentOptimum", "IndexOfOptimum", "Innovation", "InnovationAtCurrentState", "SigmaObs2", "MahalanobisConsistency", "SimulationQuantiles", "SimulatedObservationAtBackground", "SimulatedObservationAtCurrentState", "SimulatedObservationAtOptimum", "SimulatedObservationAtCurrentOptimum"]
            )
        self.defineRequiredParameter(
            name     = "Quantiles",
            default  = [],
            typecast = tuple,
            message  = "Liste des valeurs de quantiles",
            minval   = 0.,
            maxval   = 1.,
            )
        self.defineRequiredParameter(
            name     = "SetSeed",
            typecast = numpy.random.seed,
            message  = "Graine fixée pour le générateur aléatoire",
            )
        self.defineRequiredParameter(
            name     = "NumberOfSamplesForQuantiles",
            default  = 100,
            typecast = int,
            message  = "Nombre d'échantillons simulés pour le calcul des quantiles",
            minval   = 1,
            )
        self.defineRequiredParameter(
            name     = "SimulationForQuantiles",
            default  = "Linear",
            typecast = str,
            message  = "Type de simulation pour l'estimation des quantiles",
            listval  = ["Linear", "NonLinear"]
            )
        self.defineRequiredParameter( # Pas de type
            name     = "Bounds",
            message  = "Liste des valeurs de bornes",
            )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run()
        if logging.getLogger().level < logging.WARNING:
            self.__iprint, self.__disp = 1, 1
            self.__message = scipy.optimize.tnc.MSG_ALL
        else:
            self.__iprint, self.__disp = -1, 0
            self.__message = scipy.optimize.tnc.MSG_NONE
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
        #
        # Correction pour pallier a un bug de TNC sur le retour du Minimum
        if self._parameters.has_key("Minimizer") == "TNC":
            self.setParameterValue("StoreInternalVariables",True)
        #
        # Opérateurs
        # ----------
        Hm = HO["Direct"].appliedTo
        Ha = HO["Adjoint"].appliedInXTo
        #
        # Utilisation éventuelle d'un vecteur H(Xb) précalculé
        # ----------------------------------------------------
        if HO["AppliedToX"] is not None and HO["AppliedToX"].has_key("HXb"):
            HXb = HO["AppliedToX"]["HXb"]
        else:
            HXb = Hm( Xb )
        HXb = numpy.asmatrix(numpy.ravel( HXb )).T
        #
        # Calcul de l'innovation
        # ----------------------
        if Y.size != HXb.size:
            raise ValueError("The size %i of observations Y and %i of observed calculation H(X) are different, they have to be identical."%(Y.size,HXb.size))
        if max(Y.shape) != max(HXb.shape):
            raise ValueError("The shapes %s of observations Y and %s of observed calculation H(X) are different, they have to be identical."%(Y.shape,HXb.shape))
        d  = Y - HXb
        #
        # Précalcul des inversions de B et R
        # ----------------------------------
        BI = B.getI()
        RI = R.getI()
        #
        # Définition de la fonction-coût
        # ------------------------------
        def CostFunction(x):
            _X  = numpy.asmatrix(numpy.ravel( x )).T
            if self._parameters["StoreInternalVariables"] or \
                "CurrentState" in self._parameters["StoreSupplementaryCalculations"] or \
                "CurrentOptimum" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["CurrentState"].store( _X )
            _HX = Hm( _X )
            _HX = numpy.asmatrix(numpy.ravel( _HX )).T
            _Innovation = Y - _HX
            if "SimulatedObservationAtCurrentState" in self._parameters["StoreSupplementaryCalculations"] or \
               "SimulatedObservationAtCurrentOptimum" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["SimulatedObservationAtCurrentState"].store( _HX )
            if "InnovationAtCurrentState" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["InnovationAtCurrentState"].store( _HX )
            Jb  = 0.5 * (_X - Xb).T * BI * (_X - Xb)
            Jo  = 0.5 * _Innovation.T * RI * _Innovation
            J   = float( Jb ) + float( Jo )
            self.StoredVariables["CostFunctionJb"].store( Jb )
            self.StoredVariables["CostFunctionJo"].store( Jo )
            self.StoredVariables["CostFunctionJ" ].store( J )
            if "IndexOfOptimum" in self._parameters["StoreSupplementaryCalculations"] or \
               "CurrentOptimum" in self._parameters["StoreSupplementaryCalculations"] or \
               "SimulatedObservationAtCurrentOptimum" in self._parameters["StoreSupplementaryCalculations"]:
                IndexMin = numpy.argmin( self.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
            if "IndexOfOptimum" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["IndexOfOptimum"].store( IndexMin )
            if "CurrentOptimum" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["CurrentOptimum"].store( self.StoredVariables["CurrentState"][IndexMin] )
            if "SimulatedObservationAtCurrentOptimum" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( self.StoredVariables["SimulatedObservationAtCurrentState"][IndexMin] )
            return J
        #
        def GradientOfCostFunction(x):
            _X      = numpy.asmatrix(numpy.ravel( x )).T
            _HX     = Hm( _X )
            _HX     = numpy.asmatrix(numpy.ravel( _HX )).T
            GradJb  = BI * (_X - Xb)
            GradJo  = - Ha( (_X, RI * (Y - _HX)) )
            GradJ   = numpy.asmatrix( numpy.ravel( GradJb ) + numpy.ravel( GradJo ) ).T
            return GradJ.A1
        #
        # Point de démarrage de l'optimisation : Xini = Xb
        # ------------------------------------
        if type(Xb) is type(numpy.matrix([])):
            Xini = Xb.A1.tolist()
        else:
            Xini = list(Xb)
        #
        # Minimisation de la fonctionnelle
        # --------------------------------
        nbPreviousSteps = self.StoredVariables["CostFunctionJ"].stepnumber()
        #
        if self._parameters["Minimizer"] == "LBFGSB":
            Minimum, J_optimal, Informations = scipy.optimize.fmin_l_bfgs_b(
                func        = CostFunction,
                x0          = Xini,
                fprime      = GradientOfCostFunction,
                args        = (),
                bounds      = Bounds,
                maxfun      = self._parameters["MaximumNumberOfSteps"]-1,
                factr       = self._parameters["CostDecrementTolerance"]*1.e14,
                pgtol       = self._parameters["ProjectedGradientTolerance"],
                iprint      = self.__iprint,
                )
            nfeval = Informations['funcalls']
            rc     = Informations['warnflag']
        elif self._parameters["Minimizer"] == "TNC":
            Minimum, nfeval, rc = scipy.optimize.fmin_tnc(
                func        = CostFunction,
                x0          = Xini,
                fprime      = GradientOfCostFunction,
                args        = (),
                bounds      = Bounds,
                maxfun      = self._parameters["MaximumNumberOfSteps"],
                pgtol       = self._parameters["ProjectedGradientTolerance"],
                ftol        = self._parameters["CostDecrementTolerance"],
                messages    = self.__message,
                )
        elif self._parameters["Minimizer"] == "CG":
            Minimum, fopt, nfeval, grad_calls, rc = scipy.optimize.fmin_cg(
                f           = CostFunction,
                x0          = Xini,
                fprime      = GradientOfCostFunction,
                args        = (),
                maxiter     = self._parameters["MaximumNumberOfSteps"],
                gtol        = self._parameters["GradientNormTolerance"],
                disp        = self.__disp,
                full_output = True,
                )
        elif self._parameters["Minimizer"] == "NCG":
            Minimum, fopt, nfeval, grad_calls, hcalls, rc = scipy.optimize.fmin_ncg(
                f           = CostFunction,
                x0          = Xini,
                fprime      = GradientOfCostFunction,
                args        = (),
                maxiter     = self._parameters["MaximumNumberOfSteps"],
                avextol     = self._parameters["CostDecrementTolerance"],
                disp        = self.__disp,
                full_output = True,
                )
        elif self._parameters["Minimizer"] == "BFGS":
            Minimum, fopt, gopt, Hopt, nfeval, grad_calls, rc = scipy.optimize.fmin_bfgs(
                f           = CostFunction,
                x0          = Xini,
                fprime      = GradientOfCostFunction,
                args        = (),
                maxiter     = self._parameters["MaximumNumberOfSteps"],
                gtol        = self._parameters["GradientNormTolerance"],
                disp        = self.__disp,
                full_output = True,
                )
        else:
            raise ValueError("Error in Minimizer name: %s"%self._parameters["Minimizer"])
        #
        IndexMin = numpy.argmin( self.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
        MinJ     = self.StoredVariables["CostFunctionJ"][IndexMin]
        #
        # Correction pour pallier a un bug de TNC sur le retour du Minimum
        # ----------------------------------------------------------------
        if self._parameters["StoreInternalVariables"] or "CurrentState" in self._parameters["StoreSupplementaryCalculations"]:
            Minimum = self.StoredVariables["CurrentState"][IndexMin]
        #
        # Obtention de l'analyse
        # ----------------------
        Xa = numpy.asmatrix(numpy.ravel( Minimum )).T
        #
        self.StoredVariables["Analysis"].store( Xa.A1 )
        #
        if "OMA"                           in self._parameters["StoreSupplementaryCalculations"] or \
           "SigmaObs2"                     in self._parameters["StoreSupplementaryCalculations"] or \
           "SimulatedObservationAtOptimum" in self._parameters["StoreSupplementaryCalculations"] or \
           "SimulationQuantiles"           in self._parameters["StoreSupplementaryCalculations"]:
            if "SimulatedObservationAtCurrentState" in self._parameters["StoreSupplementaryCalculations"]:
                HXa = self.StoredVariables["SimulatedObservationAtCurrentState"][IndexMin]
            elif "SimulatedObservationAtCurrentOptimum" in self._parameters["StoreSupplementaryCalculations"]:
                HXa = self.StoredVariables["SimulatedObservationAtCurrentOptimum"][-1]
            else:
                HXa = Hm(Xa)
        #
        # Calcul de la covariance d'analyse
        # ---------------------------------
        if "APosterioriCovariance" in self._parameters["StoreSupplementaryCalculations"] or \
           "SimulationQuantiles" in self._parameters["StoreSupplementaryCalculations"]:
            HtM = HO["Tangent"].asMatrix(ValueForMethodForm = Xa)
            HtM = HtM.reshape(Y.size,Xa.size) # ADAO & check shape
            HaM = HO["Adjoint"].asMatrix(ValueForMethodForm = Xa)
            HaM = HaM.reshape(Xa.size,Y.size) # ADAO & check shape
            HessienneI = []
            nb = Xa.size
            for i in range(nb):
                _ee    = numpy.matrix(numpy.zeros(nb)).T
                _ee[i] = 1.
                _HtEE  = numpy.dot(HtM,_ee)
                _HtEE  = numpy.asmatrix(numpy.ravel( _HtEE )).T
                HessienneI.append( numpy.ravel( BI*_ee + HaM * (RI * _HtEE) ) )
            HessienneI = numpy.matrix( HessienneI )
            A = HessienneI.I
            if min(A.shape) != max(A.shape):
                raise ValueError("The %s a posteriori covariance matrix A is of shape %s, despites it has to be a squared matrix. There is an error in the observation operator, please check it."%(self._name,str(A.shape)))
            if (numpy.diag(A) < 0).any():
                raise ValueError("The %s a posteriori covariance matrix A has at least one negative value on its diagonal. There is an error in the observation operator, please check it."%(self._name,))
            if logging.getLogger().level < logging.WARNING: # La verification n'a lieu qu'en debug
                try:
                    L = numpy.linalg.cholesky( A )
                except:
                    raise ValueError("The %s a posteriori covariance matrix A is not symmetric positive-definite. Please check your a priori covariances and your observation operator."%(self._name,))
            self.StoredVariables["APosterioriCovariance"].store( A )
        #
        # Calculs et/ou stockages supplémentaires
        # ---------------------------------------
        if "Innovation" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["Innovation"].store( numpy.ravel(d) )
        if "BMA" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(Xa) )
        if "OMA" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["OMA"].store( numpy.ravel(Y) - numpy.ravel(HXa) )
        if "OMB" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["OMB"].store( numpy.ravel(d) )
        if "SigmaObs2" in self._parameters["StoreSupplementaryCalculations"]:
            TraceR = R.trace(Y.size)
            self.StoredVariables["SigmaObs2"].store( float( (d.T * (numpy.asmatrix(numpy.ravel(Y)).T-numpy.asmatrix(numpy.ravel(HXa)).T)) ) / TraceR )
        if "MahalanobisConsistency" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["MahalanobisConsistency"].store( float( 2.*MinJ/d.size ) )
        if "SimulationQuantiles" in self._parameters["StoreSupplementaryCalculations"]:
            Qtls = map(float, self._parameters["Quantiles"])
            nech = self._parameters["NumberOfSamplesForQuantiles"]
            HXa  = numpy.matrix(numpy.ravel( HXa )).T
            YfQ  = None
            for i in range(nech):
                if self._parameters["SimulationForQuantiles"] == "Linear":
                    dXr = numpy.matrix(numpy.random.multivariate_normal(Xa.A1,A) - Xa.A1).T
                    dYr = numpy.matrix(numpy.ravel( HtM * dXr )).T
                    Yr = HXa + dYr
                elif self._parameters["SimulationForQuantiles"] == "NonLinear":
                    Xr = numpy.matrix(numpy.random.multivariate_normal(Xa.A1,A)).T
                    Yr = numpy.matrix(numpy.ravel( Hm( Xr ) )).T
                if YfQ is None:
                    YfQ = Yr
                else:
                    YfQ = numpy.hstack((YfQ,Yr))
            YfQ.sort(axis=-1)
            YQ = None
            for quantile in Qtls:
                if not (0. <= quantile <= 1.): continue
                indice = int(nech * quantile - 1./nech)
                if YQ is None: YQ = YfQ[:,indice]
                else:          YQ = numpy.hstack((YQ,YfQ[:,indice]))
            self.StoredVariables["SimulationQuantiles"].store( YQ )
        if "SimulatedObservationAtBackground" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["SimulatedObservationAtBackground"].store( numpy.ravel(HXb) )
        if "SimulatedObservationAtOptimum" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["SimulatedObservationAtOptimum"].store( numpy.ravel(HXa) )
        #
        self._post_run(HO)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
