# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2024 EDF R&D
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

#===============================================================================
import numpy
# donnees numeriques du modele
xdeb = 0.
xfin = 1.

nx = 500
dx=(xfin-xdeb)/nx
dim = nx+1
p = 10 # nb de mesures

class EqChaleur(object):

    def __init__(self,alpha):

        self.alpha = float(alpha)

        idx2 = 1./dx**2
        self.A=2*idx2*numpy.identity(dim)
        for i in range(1,dim-2):
            self.A[i,i+1]=-idx2
            self.A[i+1,i]=-idx2

    def solve(self,S):
        return numpy.linalg.solve(self.alpha*self.A,S)

    def get2ndMbre(self):

        S = numpy.zeros((dim,))
        c = numpy.pi*dx
        pi2 = numpy.pi**2

        for i in range(dim):
            S[i] = pi2*numpy.sin(i*c)
        return S

    def extract(self,champs,nbobs):

        incr = int(nx/nbobs)
        return champs[::incr]

    def obs(self,nbobs):

        X = numpy.linspace(xdeb,xfin,dim)
        S = self.get2ndMbre()
        T = self.solve(S)
        return self.extract(T,nbobs)

    def disp(self):

        X = numpy.linspace(xdeb,xfin,dim)
        S = self.get2ndMbre()
        T = self.solve(S)

        from matplotlib import pylab
        pylab.plot(X,T)
        pylab.show()

class ExempleOperateurChaleur:
    """
    Modelisation d'operateur non lineaire pour la diffusion de la chaleur dans
    un mur d'epaisseur e, avec une production de chaleur r, pour un
    environnement a temperature Ts. Les equations sont :

        T = Ts - r/2k x^2 + r e /2k  x
    """
    def __init__(self, e = 10., Ts = 100., nbpt = 1000, nbobs = 10):
        self.e     = float(e)
        self.Ts    = float(Ts)
        self.nbpt  = int(nbpt)
        self.dx    = self.e/(self.nbpt-1)
        self.nbobs = min(int(nbobs),self.nbpt)

    def Direct(self, XX ):
        if type(XX) is type(numpy.matrix([])):  alpha = XX.A1
        elif type(XX) is type(numpy.array([])): alpha = numpy.matrix(XX).A1
        else:                                alpha = XX
        #
        eq=EqChaleur(alpha)
        HX = eq.obs(self.nbobs)
        #
        return numpy.array( HX )

    def DirectExp(self, XX ): # Version en Log/Exp
        if type(XX) is type(numpy.matrix([])):  alpha = XX.A1
        elif type(XX) is type(numpy.array([])): alpha = numpy.matrix(XX).A1
        else:                                   alpha = XX
        alpha = numpy.exp(alpha)
        #
        eq=EqChaleur(alpha)
        HX = eq.obs(self.nbobs)
        #
        return numpy.array( HX )


    def Analytique(self, XX ):
        amort = float(XX)
        listresult = []
        for i in range(self.nbobs+1) :
            ex = i * self.e/(self.nbobs)
            eT = self.Ts - amort * ex**2 + self.e*amort*ex
            listresult.append(eT)
        return numpy.array(listresult)

    def Tangent(self, paire ):
        (X, dX) = paire
        pass

    def Adjoint(self, paire ):
        (X, Y) = paire
        pass

#===============================================================================

CheckingPoint = [2.]

AlgorithmParameters = {
    "EpsilonMinimumExponent" : -10,
    # "PlotAndSave" : True,
    "SetSeed" : 1000,
    "InitialDirection":CheckingPoint,
    "AmplitudeOfInitialDirection":0.5,
    }

taille = 1000
OP = ExempleOperateurChaleur(nbpt = taille)

DirectOperator = OP.Direct

# JPA : probleme : il faut que le nom d'origine, qui est une méthode de classe,
# existe explicitement pour permettre le parallelisme !
Direct = DirectOperator
