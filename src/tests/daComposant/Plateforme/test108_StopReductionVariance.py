#-*-coding:iso-8859-1-*-
__doc__ = """
    Recherche de l'arrêt de la réduction de la variance (VAR(OMB)-VAR(OMA)) 
    lors d'itérations sur une analyse Blue avec R = alpha*B et H = Id.
    - avec remise à jour de l'ébauche xb = xa (updatexb = True)
    - avec correction de R et B par so et sb (sosb = True)
"""
__author__ = "Sophie RICCI - Septembre 2008"

execfile("context.py")

import numpy
from AssimilationStudy import AssimilationStudy
from scipy import asarray

#===============================================================================
def test(dimension = 3, alpha = 1., N = 10, updatexb = True, sosb = False) :
    #
    # Définition des données "théoriques" vraies
    # ------------------------------------------
    xt = numpy.arange(dimension)
    Eo = numpy.random.normal(0.,1.,size=(dimension,))
    Eb = numpy.zeros((dimension,))
    H  = numpy.identity(dimension)
    xb = xt + Eb
    yo = numpy.dot(H,xt) + Eo
    # Définition des matrices de covariances d'erreurs
    # ------------------------------------------------
    B  = numpy.identity(dimension)
    R  = alpha * B
    # Analyse BLUE
    # ------------
    ADD = AssimilationStudy()
    ADD.setObservation        (asVector     = yo )
    ADD.setObservationOperator(asMatrix     = H )
    ADD.setControls()
    ADD.setAlgorithm(choice="Blue")
    SigmaBck2 = 1.
    SigmaObs2 = 1. 
    VectSigmaObs2, VectSigmaBck2 = [],[]
    vectd , vectOMA = [],[]

    # Iterations du Blue
    for i in range (0, N) :
        ADD.setBackground         (asVector     = xb )
        # Mise a jour de R et B par so et sb
        if sosb :    
            newB = SigmaBck2*B
            newR = SigmaObs2*R
            ADD.setBackgroundError (asCovariance = newB )
            ADD.setObservationError(asCovariance = newR )
        else :
            newB = B
            newR = R
            ADD.setBackgroundError (asCovariance = newB )
            ADD.setObservationError(asCovariance = newR )
        ADD.analyze()
        xa = ADD.get("Analysis").valueserie(i)
        d = ADD.get("Innovation").valueserie(i)
        # Construit le vecteur des so et sb
        SigmaObs2 = ADD.get("SigmaObs2").valueserie(i)
        SigmaBck2 = ADD.get("SigmaBck2").valueserie(i)
        VectSigmaObs2.append(SigmaObs2)
        VectSigmaBck2.append(SigmaBck2)

        # Calcul de la variance de OMB et OMA 
        OMB = yo -xb
        var_OMB = OMB.var()
        vectd.append(var_OMB)

        OMA = yo-xa
        var_OMA = OMA.var()
        vectOMA.append(var_OMA)

        # Update de l ebauche par l analyse
        if updatexb : 
            xb = xa
       
    # Construction du vecteur de difference VAR(OMB)-VAR(0MA)
    vectd =  asarray(vectd)
    vectOMA =  asarray(vectOMA)
    vector = asarray(vectd) - asarray(vectOMA)

    # Plot de  VAR(d) - VAR(OMA) au cours des iterations
    # --------------------------------------------------
    ADD.setDiagnostic("PlotVector", "Affichage multi-pas Gnuplot d'un vecteur")
    MonPlot = ADD.get("Affichage multi-pas Gnuplot d'un vecteur")
#    MonPlot.calculate(vector, title = " VAR(d) - VAR(OMA) ", xlabel = "Axe X", ylabel = "Axe Y", filename = "Plot_StopReductionVariance_VAROMB-VAROMA.ps", pause = True)
#    MonPlot.calculate(VectSigmaObs2, title = " SigmaObs2 ", xlabel = "Axe X", ylabel = "Axe Y", filename = "testiter_so.ps", pause = True)
#    MonPlot.calculate(VectSigmaBck2, title = " SigmaBck2 ", xlabel = "Axe X", ylabel = "Axe Y", filename = "testiter_sb.ps", pause = True)


    # Application du diagnostic sur l arret de la reduction de la variance
    # ----------------------------------------------------------------------
    ADD.setDiagnostic("StopReductionVariance",
        name = "Arret de la reduction de la variance entre OMB et OMA")
    #
    D = ADD.get("Arret de la reduction de la variance entre OMB et OMA")
    D.calculate( vector = vector,  CutOffSlope = 0.005, MultiSlope0 = None)

    # Verification du resultat
    # ------------------------
    print __doc__
    print "    La variance n'est plus significativement réduite après l'itération", D.valueserie(0)
    print "    Test correct"
    print

#===============================================================================
if __name__ == "__main__":

    print
    print "AUTODIAGNOSTIC"
    print "=============="
    numpy.random.seed(1000)

    test()

