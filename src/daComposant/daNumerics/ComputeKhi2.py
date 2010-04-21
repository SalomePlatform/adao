#-*-coding:iso-8859-1-*-
#
#  Copyright (C) 2008-2009  EDF R&D
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
__doc__ = """
    Outil numerique de calcul de la variable Khi2

    On peut realiser deux types de test du Khi2 :
        - test d'adequation : comparer la distribution d'un echantillon a une
          distribution theorique,
        - test d'homogeneite : comparer les distributions de 2 vecteurs.

    Pour le test d'adequation, on travaille sur une gaussienne 
    dont la moyenne et l'ecart type sont calcules sur 
    l'echantillon, soit donnes.

    Ce fichier contient une classe "StatspourTests" de methodes qui realisent 
    differentes etapes utiles aux calculs des tests du Khi2.

    Ce fichier contient de plus 3  methodes : ComputeKhi2_testGauss, 
    ComputeKhi2_Gauss et ComputeKhi2_Homogen.
    - ComputeKhi2_testGauss : calcul la distance du Khi2 entre un vecteur 
      aleatoire issu d un gaussienne et une distribution theorique gaussienne
      dont on specifie la moyenne et l ecart type
    - ComputeKhi2_Gauss : calcul la distance du Khi2 entre un vecteur donne et 
      une distribution theorique gaussienne dont la moyenne et l ecart type sont 
      calcules sur l echantillon
    - ComputeKhi2_Homogen : calcul la distance du Khi2 entre deux vecteurs donnes

    Ces methodes necessitent et fournissent :
        - en input :
            - le ou les vecteurs dont on etudie la distribution,
            - la distribution theorique et eventuellement la moyenne et ecart type, 
            - la largeur des classes, 
            - un booleen traduisant la suppression des classes vides
        - en output :
            - le vecteur des classes, 
            - les pdf theorique et donnee, 
            - la valeur du Khi2, 
            - la p-value qui represent l'aire de la queue de la distribution du
              Khi2 et
            - le message qui interprete le test.
"""
__author__ = "Sophie RICCI - Mars 2010"

import numpy
from numpy import random
from scipy import arange, asarray, stats
from scipy.stats import histogram2, chisquare, chisqprob, norm
import logging

# ==============================================================================
class StatspourTests :
    """
    Classe de methodes pour la preparation du test de Khi2
    """
    def __init__(self, cdftheo=None, meantheo = None, stdtheo = None, pdftest=None,obs=None,use_mean_std_exp=True, dxmin=0.01, obsHomogen = None, nbclasses = None) :


        if (pdftest is None and obs is None) :
           raise ValueError('Donner soit une pdf de test soit un vecteur obs')
        if not obs is None :
            if pdftest is None : 
              self.__obs=asarray(obs)
        if not pdftest is None :
            if obs is None :
               if len(pdftest) == 3:
                  niter=eval(pdftest[2])
                  obs=[eval(" ".join(pdftest[:2])) for z in range(niter)]
                  self.__obs=asarray(obs)
               else : 
                  self.__obs=asarray(eval(" ".join(pdftest[:2])))
        if not (obsHomogen is None) :
          self.__obsHomogen = asarray(obsHomogen)
          self.__testHomogen =  True
        else :
          self.__testHomogen =  False


        self.__mean_exp = self.__obs.mean()
        self.__std_exp = self.__obs.std()

        if cdftheo is None : raiseValueError(" ... Definir le parametre cdftheo ...")
        if  use_mean_std_exp : 
          self.__cdf=cdftheo( self.__mean_exp, self.__std_exp).cdf
        else : 
          self.__cdf=cdftheo( meantheo, stdtheo).cdf

        self.__min=min(self.__obs)
        self.__max=max(self.__obs)
        self.__N=len(self.__obs)
        self.__use_mean_std_exp=use_mean_std_exp
        self.__dxmin=dxmin
        self.__nbclasses = nbclasses
        if not (dxmin is None) and  not (nbclasses is None) :
           raise ValueError("... Specifier soit le nombre de classes, soit la largeur des classes")
        if  (dxmin is None) and   (nbclasses is None) :
           raise ValueError("... Specifier soit le nombre de classes, soit la largeur des classes")
        if not (nbclasses is None) and (dxmin is None) :
          self.__dxmin = (self.__max - self.__min ) / float(self.__nbclasses)
        return None

    def MakeClasses(self) :
        """
        Classification en classes
        """
        self.__subdiv=arange(self.__min,self.__max+self.__dxmin,self.__dxmin)
        self.__modalites=len(self.__subdiv)
        return None

    def ComputeObs(self):
        """
        Calcul de la probabilite observee de chaque classe
        """
        self.__kobs=histogram2(self.__obs,self.__subdiv)[1:]
        return self.__kobs

    def ComputeObsHomogen(self):
        """
        Calcul de la probabilite observee pour le test homogeneite de chaque classe
        """
        self.__kobsHomogen=histogram2(self.__obsHomogen,self.__subdiv)[1:]
        return self.__kobsHomogen

    def ComputeTheo(self):
        """
        Calcul de la probabilite theorique de chaque classe
        """
        self.__ktheo=[self.__cdf(self.__subdiv[i+1])-self.__cdf(self.__subdiv[i]) for i in range(self.__modalites-1)]
        self.__ktheo=asarray(self.__ktheo)
        self.__ktheo=(sum(self.__kobs)/sum(self.__ktheo))*self.__ktheo

    def Computepdfs(self) :

        self.__subdiv=self.__subdiv[1:]
        self.__pdfobs=[self.__kobs[i+1]/(self.__subdiv[i+1]-self.__subdiv[i]) for i in range(self.__modalites-2)]

        if self.__testHomogen : 
            self.__pdftheo=[self.__kobsHomogen[i+1]/(self.__subdiv[i+1]-self.__subdiv[i]) for i in range(self.__modalites-2)]
        else :
            self.__pdftheo=[self.__ktheo[i+1]/(self.__subdiv[i+1]-self.__subdiv[i]) for i in range(self.__modalites-2)]

        return self.__subdiv, self.__pdftheo, self.__pdfobs

    def Computeddl(self):
        """
        Calcul du nombre de degres de liberte
        """
        self.__ddl = self.__modalites - 1.
        if self.__use_mean_std_exp :
            self.__ddl = self.__ddl - 2.
        if (self.__ddl < 1.):
            raise ValueError("The ddl is 0, you must increase the number of classes nbclasse ")
        logging.debug("Nombre de degres de liberte=%s"%self.__ddl)

    def ComputeValue(self) : 
        """
        Calcul de la variable Q qui suit une loi Khi-2
        """
        if self.__testHomogen :
          kobs,ktheo=self.__kobs.tolist(),self.__kobsHomogen.tolist()
        else :
          kobs,ktheo=self.__kobs.tolist(),self.__ktheo.tolist()

        # on supprime les classes theoriques qui ont moins d'un element (sinon la distance khi2 tendrait vers l'infini)
        ko,kt=[],[]
        self.__count0 = 0.
        for k,val in enumerate(ktheo):
            if val > 1.0:
                kt.append(val)
                ko.append(kobs[k])
            else : 
                self.__count0 = self.__count0 +1.
        logging.debug("WARNING : nombre de classes vides supprimees (effectif theorique inferieur a 1.) pour le calcul de la valeur du Khi2 = %s"%self.__count0)
        ef1,ef2=asarray(ko),asarray(kt)
        count  = 0.
        for el in ef1.tolist() : 
           if el < 5. : 
              count = count +1.
        for el in ef2.tolist() :
           if el < 5. :
              count = count +1.
        pourcent_nbclasse_effecinf = count /(2.*len(ef1.tolist())) *100.
        if (pourcent_nbclasse_effecinf > 20.) :
           logging.debug("WARNING : nombre de classes dont l effectif est inferieur a 5 elements %s"%pourcent_nbclasse_effecinf)
        k,p = chisquare(ef1, ef2)
        k2, p2 = [k],[p]
        for shift in range(1,6):
            k,p=chisquare(ef1[shift:],ef2[:-shift])
            k2.append(k)
            p2.append(p)
            k,p=chisquare(ef1[:-shift],ef2[shift:])
            k2.append(k)
            p2.append(p)
        logging.debug("Liste des valeurs du Khi2 = %s"%k2)
        self.__khi2=min(k2)
        self.__Q=self.__khi2

        logging.debug("Valeur du Khi2=%s"%self.__Q)
        return self.__Q

    def ComputeArea(self):
        """
        Calcul de la p-value
        """
        self.__areakhi2 = 100 * chisqprob(self.__Q, self.__ddl)
        return self.__areakhi2  

    def WriteMessage(self):
        """
        Interpretation du test
        """
        message = "Il y a %.2f%s de chance de se tromper en refusant l'adequation"%(self.__areakhi2,"%")
        return message
  
    def WriteMessageHomogen(self):
        """
        Interpretation du test
        """
        message = "Il y a %.2f%s de chance de se tromper en refusant l'homogeneite"%(self.__areakhi2,"%")
        return message

# ==============================================================================
def ComputeKhi2_testGauss(
        meantheo = 0., 
        stdtheo = 1., 
        nech = 10,
        dx = 0.1,
        nbclasses = None,
        SuppressEmptyClasses = True,
        ):
    """
    Test du Khi2 d adequation entre tirage aleatoire dans gaussienne et une gaussienne theo
    """
    essai = StatspourTests( cdftheo=norm, meantheo = meantheo, stdtheo = stdtheo, pdftest = ["random.normal","(%.3f,%.2f,%d)"%(meantheo,stdtheo,nech)], obs = None, use_mean_std_exp=False,dxmin=dx, obsHomogen = None, nbclasses = nbclasses)
    essai.MakeClasses()
    essai.ComputeObs()
    essai.ComputeTheo()
    classes,eftheo, efobs = essai.Computepdfs()
    essai.Computeddl()
    valeurKhi2= essai.ComputeValue()
    areaKhi2 = essai.ComputeArea()
    message = essai.WriteMessage()
    logging.debug("message %s"%message)
    return classes, eftheo, efobs, valeurKhi2, areaKhi2, message

def ComputeKhi2_Gauss(
        vectorV = None,
        dx = 0.1,
        SuppressEmptyClasses = True, 
        nbclasses = None
        ):
    """
    Test du Khi2 d adequation entre un vecteur donne et une gaussienne theo de mean et std celles du vecteur
    """
    essai = StatspourTests( cdftheo=norm, pdftest = None, obs = vectorV, use_mean_std_exp=True,dxmin=dx, obsHomogen = None, nbclasses = nbclasses)
    essai.MakeClasses()
    essai.ComputeObs()
    essai.ComputeTheo()
    classes,eftheo, efobs = essai.Computepdfs()
    essai.Computeddl()
    valeurKhi2= essai.ComputeValue()
    areaKhi2 = essai.ComputeArea()
    message = essai.WriteMessage()
    logging.debug("message %s"%message)
    return classes, eftheo, efobs, valeurKhi2, areaKhi2, message

def ComputeKhi2_Homogen(
        vectorV1 = None,
        vectorV2 = None,
        dx = 0.1,
        SuppressEmptyClasses = True,
        nbclasses = None
        ):
    """
    Test du Khi2 d homogeniete entre 2 vecteurs 
    """
    essai = StatspourTests( cdftheo=norm, pdftest = None, obs = vectorV1, use_mean_std_exp=True,dxmin=dx, obsHomogen = vectorV2, nbclasses = nbclasses)
    essai.MakeClasses()
    essai.ComputeObs()
    essai.ComputeObsHomogen()
    classes,eftheo, efobs = essai.Computepdfs()
    essai.Computeddl()
    valeurKhi2= essai.ComputeValue()
    areaKhi2 = essai.ComputeArea()
    message = essai.WriteMessageHomogen()
    logging.debug("message %s"%message)
    return classes, eftheo, efobs, valeurKhi2, areaKhi2, message

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
    #
    numpy.random.seed(100)

    # Test de verification d adequation entre une gaussienne et un tirage gaussien
    print ''
    print 'Test de verification d adequation entre une gaussienne centree normale et un tirage gaussien'
    classes, eftheo, efobs, valeurKhi2, areaKhi2, message = ComputeKhi2_testGauss(meantheo = 0., stdtheo = 1., nech = 1000., dx = 0.1, SuppressEmptyClasses = True, nbclasses = None)
    print '  valeurKhi2=',valeurKhi2
    print '  areaKhi2=',areaKhi2
    print ' ',message

    if (numpy.abs(areaKhi2 - 99.91)< 1.e-2) :
       print "The computation of the khisquare value is OK"
    else :
       raise ValueError("The computation of the khisquare value is WRONG")

    numpy.random.seed(2490)

    # Test de verification d adequation entre une gaussienne et un vecteur donne
    print ''
    print 'Test de verification d adequation entre une gaussienne et un vecteur donne'
    V = random.normal(50.,1.5,1000)
    classes, eftheo, efobs, valeurKhi2, areaKhi2, message = ComputeKhi2_Gauss(dx = 0.1, vectorV = V, SuppressEmptyClasses = True, nbclasses = None)
    print '  valeurKhi2=',valeurKhi2
    print '  areaKhi2=',areaKhi2
    print ' ',message

    if (numpy.abs(areaKhi2 - 99.60)< 1.e-2) :
       print "The computation of the khisquare value is OK"
    else :
       raise ValueError("The computation of the khisquare value is WRONG")

    # Test de d homogeneite entre 2 vecteurs donnes
    print ''
    print 'Test d homogeneite entre 2 vecteurs donnes'
    V1 = random.normal(50.,1.5,10000)
    numpy.random.seed(2490)
    V2 = random.normal(50.,1.5,10000)
    classes, eftheo, efobs, valeurKhi2, areaKhi2, message = ComputeKhi2_Homogen(dx = 0.5, vectorV1 = V1, vectorV2 = V2, SuppressEmptyClasses = True, nbclasses = None)
    print '  valeurKhi2=',valeurKhi2
    print '  areaKhi2=',areaKhi2
    print ' ',message

    if (numpy.abs(areaKhi2 - 99.98)< 1.e-2) :
       print "The computation of the khisquare value is OK"
    else :
       raise ValueError("The computation of the khisquare value is WRONG")

    # Test de verification d adequation entre une gaussienne et un tirage gaussien en faisant varier le nombre de classes, echantillon de taille 10000
    print ''
    print 'Test de verification d adequation entre une gaussienne et un vecteur aleatoire gaussien de taille 10000'
#    file = 'ComputeKhi2_adequationGauss_fctnbclasses_nech10000.gnu'
#    fid = open(file, "w")
#    lines = '%s\n' % ('# dx , nbclasses, valeurKhi2, ProbKhi2' )
    numpy.random.seed(4000)
    V = random.normal(0., 1.,10000)
    aire = []
    for dx in arange(0.01, 1., 0.001) :
      classes, eftheo, efobs, valeurKhi2, areaKhi2, message = ComputeKhi2_Gauss(dx = dx, vectorV = V, SuppressEmptyClasses = True, nbclasses = None)
#      lines += '%f %f %f %f\n' % (dx, numpy.size(classes), valeurKhi2, areaKhi2)
      aire.append(areaKhi2)
    meanaire = numpy.asarray(aire)
#    fid.writelines(lines)

    print  "  En moyenne, il y a ", meanaire.mean(),"% de chance de se tromper en refusant l adequation a une loi gaussienne  pour un echantillon de taille 10000"
    print
    if (numpy.abs( meanaire.mean() - 71.79)< 1.e-2) :
       print "The computation of the khisquare value is OK"
    else :
       raise ValueError("The computation of the khisquare value is WRONG")

    # Test de verification d adequation entre une gaussienne et un tirage gaussien en faisant varier le nombre de classes, echantillon de taille 1000
    print ''
    print 'Test de verification d adequation entre une gaussienne et un vecteur aleatoire gaussien de taille 1000'
#    file = 'ComputeKhi2_adequationGauss_fctnbclasses_nech1000.gnu'
#    fid = open(file, "w")
#    lines = '%s\n' % ('# dx , nbclasses, valeurKhi2, ProbKhi2' )
    numpy.random.seed(4000)
    V = random.normal(0., 1.,1000)
    aire = []
    for dx in arange(0.05, 1., 0.001) :
      classes, eftheo, efobs, valeurKhi2, areaKhi2, message = ComputeKhi2_Gauss(dx = dx, vectorV = V, SuppressEmptyClasses = True, nbclasses = None)
#      lines += '%f %f %f %f\n' % (dx, numpy.size(classes), valeurKhi2, areaKhi2)
      aire.append(areaKhi2)
    meanaire = numpy.asarray(aire)
#    fid.writelines(lines)

    print  "  En moyenne, il y a ", meanaire.mean(),"% de chance de se tromper en refusant l adequation a une loi gaussienne  pour un echantillon de taille 1000"
    print
    if (numpy.abs( meanaire.mean() - 90.60)< 1.e-2) :
       print "The computation of the khisquare value is OK"
    else :
       raise ValueError("The computation of the khisquare value is WRONG")

   # Test de verification d adequation entre une gaussienne et un tirage gaussien en faisant varier le nombre de classes, echantillon de taille 100
    print ''
    print 'Test de verification d adequation entre une gaussienne et un vecteur aleatoire gaussien de taille 100'
#    file = 'ComputeKhi2_adequationGauss_fctnbclasses_nech100.gnu'
#    fid = open(file, "w")
#    lines = '%s\n' % ('# dx , nbclasses, valeurKhi2, ProbKhi2' )
    numpy.random.seed(4000)
    V = random.normal(0., 1.,100)
    aire = []
    for dx in arange(0.1, 1., 0.01) :
      classes, eftheo, efobs, valeurKhi2, areaKhi2, message = ComputeKhi2_Gauss(dx = dx, vectorV = V, SuppressEmptyClasses = True, nbclasses = None)
#      lines += '%f %f %f %f\n' % (dx, numpy.size(classes), valeurKhi2, areaKhi2)
      aire.append(areaKhi2)
    meanaire = numpy.asarray(aire)
#    fid.writelines(lines)

    print  "  En moyenne, il y a ", meanaire.mean(),"% de chance de se tromper en refusant l adequation a une loi gaussienne  pour un echantillon de taille 100"
    print
