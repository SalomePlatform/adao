#-*-coding:iso-8859-1-*-
#
# Copyright (C) 2008-2016 EDF R&D
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

import optparse
import sys
import re

import Traducteur.log as log
from Traducteur.load         import getJDC, getJDCFromTexte
from Traducteur.mocles       import parseKeywords
from Traducteur.dictErreurs  import GenereErreurPourCommande
from Traducteur.inseremocle  import *
from Traducteur.movemocle    import *
from Traducteur.renamemocle  import *

version_out = "V7_8_0"

usage="""Usage: python %prog [options]

Typical use is:
  python %prog --infile=xxxx.comm --outfile=yyyy.comm"""

atraiter = (
    )

dict_erreurs = {
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
    # ==========================================================================


    # ==========================================================================
    fsrc = jdc.getSource()
    fsrc = re.sub( "#VERSION_CATALOGUE:.*:FIN VERSION_CATALOGUE", "#VERSION_CATALOGUE:%s:FIN VERSION_CATALOGUE"%version_out, fsrc)
    fsrc = re.sub( "#CHECKSUM.*FIN CHECKSUM", "", fsrc )
    #
    log.ferme(hdlr)
    if outfile is not None:
        f=open(outfile,'w')
        f.write( fsrc )
        f.close()
    else:
        return fsrc

class MonTraducteur:
    def __init__(self,texte):
        self.__texte = str(texte)
    def traduit(self):
        return traduc(infile=None,outfile=None,texte=self.__texte,flog=None)

def main():
    parser = optparse.OptionParser(usage=usage)

    parser.add_option('-i','--infile', dest="infile",
        help="Le fichier COMM en entree, a traduire")
    parser.add_option('-o','--outfile', dest="outfile", default='out.comm',
        help="Le fichier COMM en sortie, traduit")

    options, args = parser.parse_args()
    if len(options.infile) == 0:
        print
        parser.print_help()
        print
        sys.exit(1)

    traduc(options.infile,options.outfile)

if __name__ == '__main__':
    main()
