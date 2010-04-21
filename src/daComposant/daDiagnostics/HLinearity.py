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
    Diagnotic de test sur la validité de l'hypothèse de linéarité de l'opérateur
    H entre xp et xm
 
    Pour calculer Hlin on utilise un schéma différences finies centrées 2
    points. On définit un dxparam tel que :
        xp = xb + dxparam
    et
        xm = xb - dxparam
    On calcule Hxp et Hxm pour obtenir Hlin. Hlin est utilise dans le Blue  pour
    caler un paramêtre. La question importante est de choisir un dxparam pas
    trop grand.

    On veut vérifier ici que l'hypothèse de linéarite du modèle par rapport  au
    paramêtre est valide sur l'intervalle du paramêtre [xm, xp]. Pour cela on
    s'assure que l'on peut retrouver la valeur Hxb par les développemenents de
    Taylor en xp et xm. Ainsi on calcule 2 estimations de Hxb, l'une à partir de
    Hxp (notee Hx1) et l'autre à partir de Hxm (notee Hx2), que l'on compare à
    la valeur calculée de Hxb. On s'intèresse ensuite a la distance entre Hxb et
    ses estimés Hx1 et Hx2. Si la distance est inférieure a un seuil de
    tolerance, l hypothese est valide.
"""
__author__ = "Sophie RICCI - Septembre 2008"

import sys ; sys.path.insert(0, "../daCore") 

import numpy
import Persistence
from BasicObjects import Diagnostic
from RMS import ElementaryDiagnostic as RMS
from AssimilationStudy import AssimilationStudy

# ==============================================================================
class ElementaryDiagnostic(Diagnostic,Persistence.OneScalar):
    def __init__(self, name="", unit="", basetype = None, parameters = {} ):
        Diagnostic.__init__(self, name, parameters)
        Persistence.OneScalar.__init__( self, name, unit, basetype = bool)
        if not self.parameters.has_key("tolerance"):
            raise ValueError("A parameter named \"tolerance\" is required.")

    def formula(self, H, dxparam,  Hxp, Hxm, Hx):
        """
        Test sur la validite de l hypothese de linearite de H entre xp et xm
        """
        dimension = numpy.size(Hx)
        #
        # Reconstruit les valeurs Hx1 et Hx2 de Hx a partir de Hxm et Hxp 
        # ---------------------------------------------------------------
        Hx1 = Hxm + H.T * dxparam
        Hx2 = Hxp - H.T * dxparam
        #
        # Calcul de l'ecart entre Hx1 et Hx et entre Hx2 et Hx
        # ----------------------------------------------------
        ADD = AssimilationStudy()
        ADD.setDiagnostic("RMS",
            name = "Calcul de la RMS entre Hx1 et Hx et entre Hx2 et Hx")
        RMS = ADD.get("Calcul de la RMS entre Hx1 et Hx et entre Hx2 et Hx")
        RMS.calculate(Hx1,Hx)
        std1 = RMS.valueserie(0)
        RMS.calculate(Hx2,Hx)
        std2 = RMS.valueserie(1)
        #
        # Normalisation des écarts par Hx pour comparer a un pourcentage
        # --------------------------------------------------------------
        RMS.calculate(Hx,Hx-Hx)
        std = RMS.valueserie(2) 
        err1=std1/std
        err2=std2/std
        #
        # Comparaison
        # -----------
        if ( (err1 < self.parameters["tolerance"]) and (err2 < self.parameters["tolerance"]) ):
            reponse = True
        else:
            reponse = False
        return reponse

    def calculate(self, Hlin = None, deltaparam = None, Hxp = None,   Hxm = None, Hx = None, step = None):
        """
        Arguments :
            - Hlin : Operateur d obsevation lineaire
            - deltaparam : pas sur le parametre param
            - Hxp : calcul en xp = xb + deltaparam
            - Hxm : calcul en xm = xb - deltaparam
            - Hx : calcul en x (generalement xb)
        """
        value = self.formula(  Hlin,  deltaparam, Hxp, Hxm, Hx )
        #
        self.store( value = value,  step = step)

#===============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'

    print " Diagnotic de test sur la validité de l'hypothèse de linéarité de"
    print " l'opérateur H entre xp et xm."
    print
    #
    dimension = 3 
    #
    # Définition des données
    # ----------------------
    Hx = numpy.array(([ 2., 4., 6.]))
    Hxp = numpy.array(([ 3., 5., 7.]))
    Hxm = numpy.array(([ 1., 3., 5.]))
    H =  (Hxp - Hxm)/(2.)
    dxparam = 1. 
    #
    # Instanciation de l'objet diagnostic
    # -----------------------------------
    D = ElementaryDiagnostic("Mon TestHlin", parameters = {"tolerance": 0.1})
    #
    # Calcul 
    # ------
    D.calculate( Hlin = H, deltaparam = dxparam, Hxp = Hxp, Hxm = Hxm, Hx = Hx)

    # Validation du calcul
    # --------------------
    if not D.valueserie(0) :
        raise ValueError("La linearisation de H autour de x entre xm et xp est fausse pour ce cas test lineaire")
    else :
        print " La linéarisation de H autour de x entre xm et xp est valide pour ce cas-test linéaire."
        print
