#-*-coding:iso-8859-1-*-
#
#  Copyright (C) 2008-2014 EDF R&D
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

__doc__ = """
    Ce module permet de mettre en place un logging utilisable partout dans
    l'application, par d�faut � la console, et si n�cessaire dans un fichier.
    
    Il doit �tre appel� en premier dans AssimilationStudy (mais pas directement
    dans les applications utilisateurs), en l'important et en instanciant un
    objet :
        import ExtendedLogging ; ExtendedLogging.ExtendedLogging()

    Par d�faut, seuls les messages du niveau WARNING ou au-del� sont disponibles
    (donc les simples messages d'info ne sont pas disponibles), ce que l'on peut
    changer � l'instanciation avec le mot-cl� "level" :
        import ExtendedLogging ; ExtendedLogging.ExtendedLogging(level=20)

    On peut �ventuellement demander � l'objet de sortir aussi les messages dans
    un fichier (noms par d�faut : AssimilationStudy.log, niveau NOTSET) :
        import ExtendedLogging ; ExtendedLogging.ExtendedLogging().setLogfile()

    Si on veut changer le nom du fichier ou le niveau global de message, il faut
    r�cup�rer l'instance et appliquer les m�thodes :
        import ExtendedLogging
        log = ExtendedLogging.ExtendedLogging()
        import logging
        log.setLevel(logging.DEBUG)
        log.setLogfile(filename="toto.log", filemode="a", level=logging.WARNING)
    et on change �ventuellement le niveau avec :
        log.setLogfileLevel(logging.INFO)
    
    Ensuite, n'importe o� dans les applications, il suffit d'utiliser le module
    "logging" (avec un petit "l") :
        import logging
        log = logging.getLogger(NAME) # Avec rien (recommand�) ou un nom NAME
        log.critical("...")
        log.error("...")
        log.warning("...")
        log.info("...")
        log.debug("...")
    ou encore plus simplement :
        import logging
        logging.info("...")

    Dans une application, � n'importe quel endroit et autant de fois qu'on veut,
    on peut changer le niveau global de message en utilisant par exemple :
        import logging
        log = logging.getLogger(NAME) # Avec rien (recommand�) ou un nom NAME
        log.setLevel(logging.DEBUG)
    
    On rappelle les niveaux (attributs de "logging") et leur ordre :
        NOTSET=0 < DEBUG=10 < INFO=20 < WARNING=30 < ERROR=40 < CRITICAL=50
"""
__author__ = "Jean-Philippe ARGAUD"

import os
import sys
import logging
from PlatformInfo import PlatformInfo

LOGFILE = os.path.join(os.path.abspath(os.curdir),"AssimilationStudy.log")

# ==============================================================================
class ExtendedLogging:
    def __init__(self, level=logging.WARNING):
        """
        Initialise un logging � la console pour TOUS les niveaux de messages.
        """
        logging.basicConfig(
            format = '%(levelname)-8s %(message)s',
            level  = level,
            stream = sys.stdout,
            )
        self.__logfile = None
        #
        # Initialise l'affichage de logging
        # ---------------------------------
        p = PlatformInfo()
        #
        logging.info( "--------------------------------------------------" )
        logging.info( "Lancement de "+p.getName()+" "+p.getVersion() )
        logging.info( "--------------------------------------------------" )
        logging.info( "Versions logicielles :" )
        logging.info( "- Python "+p.getPythonVersion() )
        logging.info( "- Numpy "+p.getNumpyVersion() )
        logging.info( "- Scipy "+p.getScipyVersion() )
        logging.info( "" )

#     def setLogfileLevel(self, level=logging.NOTSET ):
#         """
#         Permet de changer globalement le niveau des messages disponibles.
#         """
#         logging.getLogger().setLevel(level)
# 
    def setLogfile(self, filename=LOGFILE, filemode="w", level=logging.NOTSET):
        """
        Permet de disposer des messages dans un fichier EN PLUS de la console.
        """
        if self.__logfile is not None:
            # Supprime le pr�c�dent mode de stockage fichier s'il exsitait
            logging.getLogger().removeHandler(self.__logfile)
        self.__logfile = logging.FileHandler(filename, filemode)
        self.__logfile.setLevel(level)
        self.__logfile.setFormatter(
            logging.Formatter('%(asctime)s %(levelname)-8s %(message)s',
                              '%d %b %Y %H:%M:%S'))
        logging.getLogger().addHandler(self.__logfile)

    def setLogfileLevel(self, level=logging.NOTSET ):
        """
        Permet de changer le niveau des messages stock�s en fichier. Il ne sera
        pris en compte que s'il est sup�rieur au niveau global.
        """
        self.__logfile.setLevel(level)
    
    def getLevel(self):
        """
        Renvoie le niveau de logging sous forme texte
        """
        return logging.getLevelName( logging.getLogger().getEffectiveLevel() )

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'