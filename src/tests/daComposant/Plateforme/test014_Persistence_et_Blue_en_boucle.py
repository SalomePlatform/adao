#-*-coding:iso-8859-1-*-
__doc__ = """
    Cas-test vérifiant que la Persistence ou le BLUE en boucle donnent bien
    les résultats attendus.
"""
__author__ = "Jean-Philippe ARGAUD - Janvier 2009"

execfile("context.py")

import numpy
from AssimilationStudy import AssimilationStudy
from Persistence import Persistence

#===============================================================================
def test(precision = 1.e-13, dimension = 3, nbsteps = 4):
    """
    Cas-test vérifiant que la Persistence ou le BLUE en boucle donnent bien
    les résultats attendus.
    """
    vect1 = [1, 2, 1, 2, 1]
    vect2 = [-3, -3, 0, -3, -3]
    vect3 = [-1, 1, -5, 1, -1]
    vect4 = 2*[0.29, 0.97, 0.73, 0.01, 0.20]

    print
    print "    TEST DE LA PERSISTENCE"
    print "    ----------------------"
    OBJET_DE_TEST = Persistence("My object", unit="", basetype=numpy.array)
    print "    Stockage de 3 vecteurs de longueur identique"
    OBJET_DE_TEST.store(vect1)
    OBJET_DE_TEST.store(vect2)
    OBJET_DE_TEST.store(vect3)
    print "    Stockage d'un quatrième vecteur de longueur différente"
    OBJET_DE_TEST.store(vect4)
    print "    Taille \"shape\" du dernier objet stocké",OBJET_DE_TEST.shape()
    print "    Taille \"len\" du dernier objet stocké",len(OBJET_DE_TEST)

    print "    Affichage des objets avec leur type"
    for k in range(4):
        xa = OBJET_DE_TEST.valueserie(k)
        print "     %2i ==> %s, taille %2i, 3ème valeur : %s, objet : %s"%(k,type(xa),len(xa),xa[2],xa)

    del OBJET_DE_TEST

    print
    print "    TEST DE BOUCLE AUTOUR D'UN BLUE"
    print "    -------------------------------"
    yo = 0.5 + numpy.arange(dimension)
    B  = numpy.matrix(numpy.core.identity(dimension))
    R  = numpy.matrix(numpy.core.identity(dimension))
    H  = numpy.matrix(numpy.core.identity(dimension))

    ADD = AssimilationStudy("Ma premiere etude BLUE")
    ADD.setBackgroundError    (asCovariance = B  )
    ADD.setObservation        (asVector     = yo )
    ADD.setObservationError   (asCovariance = R  )
    ADD.setObservationOperator(asMatrix     = H  )
    ADD.setAlgorithm(choice="Blue")

    calculs1 = []
    for i in range(nbsteps):
        xb = numpy.arange(dimension)
        xb[min(dimension-1,2)] = i
        #
        ADD.setBackground(asVector = xb)
        ADD.analyze()

        print
        print "    Nombre d'analyses  :", ADD.get("Analysis").stepnumber()
        print "    Observation        :", yo
        print "    Ebauche            :", xb
        xa = ADD.get("Analysis").valueserie(i)
        d  = ADD.get("Innovation").valueserie(i)
        print "    Analyse résultante :", xa
        print "    so                 :", float( numpy.dot(d,(yo-numpy.dot(H,xa)).A1) / R.trace() )
        print "    sb                 :", float( numpy.dot(d,numpy.dot(H,(xa - xb)).A1) /(H * B * H.T).trace() )
        print "    Innovation         :", d
        print "    Détails de xa      :", type(xa), len(xa), xa[2]
        calculs1.append(xa[2])
    del ADD, yo, B, R, H, xb

    print
    print "    TEST DE BOUCLE AUTOUR D'UN BLUE AVEC appliedToX"
    print "    -----------------------------------------------"
    yo = 0.5 + numpy.arange(dimension)
    B  = numpy.matrix(numpy.core.identity(dimension))
    R  = numpy.matrix(numpy.core.identity(dimension))
    H  = numpy.matrix(numpy.core.identity(dimension))

    ADD = AssimilationStudy("Ma premiere etude BLUE")
    ADD.setBackgroundError    (asCovariance = B  )
    ADD.setObservation        (asVector     = yo )
    ADD.setObservationError   (asCovariance = R  )
    ADD.setObservationOperator(asMatrix     = H  )
    ADD.setAlgorithm(choice="Blue")

    calculs2 = []
    for i in range(nbsteps):
        xb = numpy.arange(dimension)
        xb[min(dimension-1,2)] = i
        HXb = numpy.dot(H,xb)
        #
        ADD.setObservationOperator(asMatrix     = H,
                                   appliedToX   = {"HXb":HXb})
        ADD.setBackground(asVector = xb)
        ADD.analyze()

        print
        print "    Nombre d'analyses  :", ADD.get("Analysis").stepnumber()
        print "    Observation        :", yo
        print "    Ebauche            :", xb
        print "    HXb                :", HXb
        xa = ADD.get("Analysis").valueserie(i)
        d  = ADD.get("Innovation").valueserie(i)
        print "    Analyse résultante :", xa
        print "    so                 :", float( numpy.dot(d,(yo-numpy.dot(H,xa)).A1) / R.trace() )
        print "    sb                 :", float( numpy.dot(d,numpy.dot(H,(xa - xb)).A1) /(H * B * H.T).trace() )
        print "    Innovation         :", d
        print "    Détails de xa      :", type(xa), len(xa), xa[2]
        calculs2.append(xa[2])
    del ADD, yo, B, R, H, xb

    #
    # Vérification du résultat
    # ------------------------
    resultats = ( 2.5 + numpy.arange(nbsteps) )/2.
    calculs1   = numpy.array(calculs1)
    calculs2   = numpy.array(calculs2)
    if   max(abs(calculs1 - resultats)) > precision:
        raise ValueError("Résultat du test erroné (1)")
    elif max(abs(calculs2 - resultats)) > precision:
        raise ValueError("Résultat du test erroné (2)")
    else:
        print test.__doc__
        print "    Test correct, erreur maximale inférieure à %s"%precision
        print

#===============================================================================
if __name__ == "__main__":

    print
    print "AUTODIAGNOSTIC"
    print "=============="
    # numpy.random.seed(1000)
    
    test(dimension=10)
