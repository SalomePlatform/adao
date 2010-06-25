#-*-coding:iso-8859-1-*-
__doc__ = """
    Cas-test vérifiant les relations d'ordre attendues sur les écarts RMS entre
    les valeurs analysees et la valeur vraie, pour 3 analyses BLUE réalisées
    avec des poids extrêmes dans R et B
"""
__author__ = "Sophie RICCI, Jean-Philippe ARGAUD - Septembre 2008"

import numpy
from daCore.AssimilationStudy import AssimilationStudy

#===============================================================================
def test(dimension = 3):
    """
    Cas-test vérifiant les relations d'ordre attendues sur les écarts RMS entre
    les valeurs analysees et la valeur vraie, pour 3 analyses BLUE réalisées
    avec des poids extrêmes dans R et B
    """
    print test.__doc__
    #
    # Définition des données
    # ----------------------
    xt = numpy.matrix(numpy.random.normal(0.,1.,size=(dimension,))).T
    Eb = numpy.matrix(numpy.random.normal(0.,1.,size=(dimension,))).T
    H  = numpy.matrix(numpy.core.identity(dimension))
    B  = numpy.matrix(numpy.core.identity(dimension)).T
    xb = xt + Eb
    yo = H * xt
    xt = xt.A1
    xb = xb.A1
    yo = yo.A1
    #
    # Analyse BLUE
    # ------------
    ADD = AssimilationStudy()
    ADD.setBackground         (asVector     = xb )
    ADD.setObservation        (asVector     = yo )
    ADD.setBackgroundError    (asCovariance = B )
    ADD.setObservationOperator(asMatrix     = H )
    ADD.setControls()
    ADD.setAlgorithm(choice="Blue")
    #
    # Définition des matrices de covariances d'erreur : ébauche parfaite
    # ------------------------------------------------------------------
    alpha1 = 10000.0
    R  = alpha1 * B
    ADD.setObservationError   (asCovariance = R )
    ADD.analyze()
    x1 = ADD.get("Analysis").valueserie(0)
    #
    # Définition des matrices de covariances d'erreurs : poids identiques
    # -------------------------------------------------------------------
    alpha2 = 1.0
    R  = alpha2 * B
    ADD.setObservationError   (asCovariance = R )
    ADD.analyze()
    x2 = ADD.get("Analysis").valueserie(1)
    #
    # Définition des matrices de covariances d'erreurs : observations parfaites
    # -------------------------------------------------------------------------
    alpha3 = 0.0001
    R  = alpha3 * B
    ADD.setObservationError   (asCovariance = R )
    ADD.analyze()
    x3 = ADD.get("Analysis").valueserie(2)
    #
    # Calcul des écarts RMS
    # ---------------------
    ADD.setDiagnostic("RMS", "Calcul de la RMS entre analyse et yo")
    RMS = ADD.get("Calcul de la RMS entre analyse et yo")
    #
    RMS.calculate(x1,yo)
    RMS.calculate(x2,yo)
    RMS.calculate(x3,yo)
    RMS_yo_x1 = RMS.valueserie(0)
    RMS_yo_x2 = RMS.valueserie(1)
    RMS_yo_x3 = RMS.valueserie(2)
    #
    print "    Cas ébauche parfaite       : R/B = %.1e"%alpha1,"RMS = %.7f"%RMS_yo_x1
    print "    Cas poids identiques       : R/B = %.1e"%alpha2,"RMS = %.7f"%RMS_yo_x2
    print "    Cas observations parfaites : R/B = %.1e"%alpha3,"RMS = %.7f"%RMS_yo_x3
    if ( (RMS_yo_x3 <= RMS_yo_x2) and  (RMS_yo_x2 <= RMS_yo_x1) ) :
        print "    La reponse de l'assimilation est cohérente avec la modification du rapport B/R."
        print
        print "    Test correct"
        print
    else :
        raise ValueError("Résultat du test erroné")

#===============================================================================
if __name__ == "__main__":

    print
    print "AUTODIAGNOSTIC"
    print "=============="
    numpy.random.seed(1000)
    
    test(dimension = 100)
