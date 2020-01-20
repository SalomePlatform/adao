#-*- coding: utf-8 -*-
#
# Copyright (C) 2008-2018 EDF R&D
#
# This file is part of SALOME ADAO module
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
# Author: Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D

import argparse
import sys
import re

import Traducteur.log as log
from Traducteur.load         import getJDC, getJDCFromTexte
from Traducteur.mocles       import parseKeywords
from Traducteur.dictErreurs  import GenereErreurPourCommande
from Traducteur.inseremocle  import *
from Traducteur.movemocle    import *
from Traducteur.renamemocle  import *

version_out = "V9_5_0"

usage="""Usage: python %(prog)s [args]

Typical use is:
  python %(prog)s --infile=xxxx.comm --outfile=yyyy.comm"""

atraiter = (
    "ASSIMILATION_STUDY",
    "CHECKING_STUDY",
    )

dict_erreurs = {
    "ASSIMILATION_STUDY":"Changements dans l'arbre et dans les noms",
    "CHECKING_STUDY":"Changements dans l'arbre et dans les noms",
    }

sys.dict_erreurs=dict_erreurs

def traduc(infile=None,outfile=None,texte=None,flog=None):
    hdlr = log.initialise(flog)
    if infile is not None:
        jdc  = getJDC(infile,atraiter)
    elif texte is not None:
        jdc  = getJDCFromTexte(texte,atraiter)
    else:
        raise ValueError("Traduction du JDC impossible")

    #Parse les mocles des commandes
    parseKeywords(jdc.root)
    GenereErreurPourCommande(jdc,('Algorithm','AlgorithmParameters','FunctionDict'))
    # ==========================================================================

    for command in atraiter:
        # Insere le MC s'il n'existe pas
        chercheOperInsereFacteurSiRegle(jdc, command, "AlgorithmParameters",((("AlgorithmParameters",),"nexistepasMCFParmi"),))
        # Deplace le MC
        moveMotClefInOperToFact(jdc, command, "Algorithm", "AlgorithmParameters", plusieursFois=False)
        # Renomme le MC
        renameMotCleInFact(jdc, command, "AlgorithmParameters", "INPUT_TYPE", "Parameters")
        # Renomme le MC
        renameMotCle(jdc, command, "Study_name", "StudyName")
        renameMotCle(jdc, command, "Study_repertory", "StudyRepertory")

    # ==========================================================================
    fsrc = jdc.getSource()
    fsrc = re.sub( "FunctionDict", "ScriptWithSwitch", fsrc )
    fsrc = re.sub( "FUNCTIONDICT_FILE", "SCRIPTWITHSWITCH_FILE", fsrc )
    fsrc = re.sub( "#VERSION_CATALOGUE:.*:FIN VERSION_CATALOGUE", "#VERSION_CATALOGUE:%s:FIN VERSION_CATALOGUE"%version_out, fsrc)
    fsrc = re.sub( "#CHECKSUM.*FIN CHECKSUM", "", fsrc )
    #
    log.ferme(hdlr)
    if outfile is not None:
        with open(outfile,'w') as f:
            f.write( fsrc )
    else:
        return fsrc

class MonTraducteur:
    def __init__(self,texte):
        self.__texte = str(texte)
    def traduit(self):
        return traduc(infile=None,outfile=None,texte=self.__texte,flog=None)

def main():
    parser = argparse.ArgumentParser(usage=usage)

    parser.add_argument('-i','--infile', dest="infile",
        help="Le fichier COMM en entree, a traduire")
    parser.add_argument('-o','--outfile', dest="outfile", default='out.comm',
        help="Le fichier COMM en sortie, traduit")

    args = parser.parse_args()
    if len(args.infile) == 0:
        print("")
        parser.print_help()
        print("")
        sys.exit(1)

    traduc(args.infile,args.outfile)

if __name__ == '__main__':
    main()
