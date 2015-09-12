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

"""
    Informations sur le code et la plateforme, et mise � jour des chemins

    La classe "PlatformInfo" permet de r�cup�rer les informations g�n�rales sur
    le code et la plateforme sous forme de strings, ou d'afficher directement
    les informations disponibles par les m�thodes. L'impression directe d'un
    objet de cette classe affiche les informations minimales. Par exemple :
        print PlatformInfo()
        print PlatformInfo().getVersion()
        created = PlatformInfo().getDate()

    La classe "PathManagement" permet de mettre � jour les chemins syst�me pour
    ajouter les outils num�riques, matrices... On l'utilise en instanciant
    simplement cette classe, sans meme r�cup�rer d'objet :
        PathManagement()
"""
__author__ = "Jean-Philippe ARGAUD"
__all__ = []

import os

# ==============================================================================
class PlatformInfo:
    """
    Rassemblement des informations sur le code et la plateforme
    """
    def getName(self):
        "Retourne le nom de l'application"
        import version
        return version.name

    def getVersion(self):
        "Retourne le num�ro de la version"
        import version
        return version.version

    def getDate(self):
        "Retourne la date de cr�ation de la version"
        import version
        return version.date
    
    def getPythonVersion(self):
        "Retourne la version de python disponible"
        import sys
        return ".".join(map(str,sys.version_info[0:3]))

    def getNumpyVersion(self):
        "Retourne la version de numpy disponible"
        import numpy.version
        return numpy.version.version

    def getScipyVersion(self):
        "Retourne la version de scipy disponible"
        import scipy.version
        return scipy.version.version

    def getMatplotlibVersion(self):
        "Retourne la version de matplotlib disponible"
        try:
            import matplotlib
            return matplotlib.__version__
        except:
            return "0.0.0"

    def getGnuplotVersion(self):
        "Retourne la version de gnuplotpy disponible"
        try:
            import Gnuplot
            return Gnuplot.__version__
        except:
            return "0.0"

    def getSphinxVersion(self):
        "Retourne la version de sphinx disponible"
        try:
            import sphinx
            return sphinx.__version__
        except:
            return "0.0.0"

    def getCurrentMemorySize(self):
        "Retourne la taille m�moire courante utilis�e"
        return 1

    def __str__(self):
        import version
        return "%s %s (%s)"%(version.name,version.version,version.date)

# ==============================================================================
def uniq(sequence):
    """
    Fonction pour rendre unique chaque �l�ment d'une liste, en pr�servant l'ordre
    """
    __seen = set()
    return [x for x in sequence if x not in __seen and not __seen.add(x)]

# ==============================================================================
class PathManagement:
    """
    Mise � jour du path syst�me pour les r�pertoires d'outils
    """
    def __init__(self):
        import sys
        parent = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
        self.__paths = {}
        self.__paths["daExternals"] = os.path.join(parent,"daExternals")
        self.__paths["daMatrices"]  = os.path.join(parent,"daMatrices")
        self.__paths["daNumerics"]  = os.path.join(parent,"daNumerics")
        #
        for v in self.__paths.values():
            sys.path.insert(0, v )
        #
        # Conserve en unique exemplaire chaque chemin
        sys.path = uniq( sys.path )
        del parent

    def getpaths(self):
        """
        Renvoie le dictionnaire des chemins ajout�s
        """
        return self.__paths

# ==============================================================================
class SystemUsage:
    """
    Permet de r�cup�rer les diff�rentes tailles m�moires du process courant
    """
    #
    # Le module resource renvoie 0 pour les tailles m�moire. On utilise donc
    # plut�t : http://code.activestate.com/recipes/286222/ et Wikipedia
    #
    _proc_status = '/proc/%d/status' % os.getpid()
    _memo_status = '/proc/meminfo'
    _scale = {
        'o':     1.0, 'ko' : 1.e3,   'Mo' : 1.e6,          'Go' : 1.e9,                 # Multiples SI de l'octet
                      'kio': 1024.0, 'Mio': 1024.0*1024.0, 'Gio': 1024.0*1024.0*1024.0, # Multiples binaires de l'octet
        'B':     1.0, 'kB' : 1024.0, 'MB' : 1024.0*1024.0, 'GB' : 1024.0*1024.0*1024.0, # Multiples binaires du byte=octet
             }
    #
    def _VmA(self, VmKey, unit):
        try:
            t = open(self._memo_status)
            v = t.read()
            t.close()
        except:
            return 0.0           # non-Linux?
        i = v.index(VmKey)       # get VmKey line e.g. 'VmRSS:  9999  kB\n ...'
        v = v[i:].split(None, 3) # whitespace
        if len(v) < 3:
            return 0.0           # invalid format?
        # convert Vm value to bytes
        mem = float(v[1]) * self._scale[v[2]]
        return mem / self._scale[unit]
    #
    def getAvailablePhysicalMemory(self, unit="o"):
        "Renvoie la m�moire physique utilisable en octets"
        return self._VmA('MemTotal:', unit)
    #
    def getAvailableSwapMemory(self, unit="o"):
        "Renvoie la m�moire swap utilisable en octets"
        return self._VmA('SwapTotal:', unit)
    #
    def getAvailableMemory(self, unit="o"):
        "Renvoie la m�moire totale (physique+swap) utilisable en octets"
        return self._VmA('MemTotal:', unit) + self._VmA('SwapTotal:', unit)
    #
    def getUsableMemory(self, unit="o"):
        """Renvoie la m�moire utilisable en octets
        Rq : il n'est pas s�r que ce d�compte soit juste...
        """
        return self._VmA('MemFree:', unit) + self._VmA('SwapFree:', unit) + \
               self._VmA('Cached:', unit) + self._VmA('SwapCached:', unit)
    #
    def _VmB(self, VmKey, unit):
        try:
            t = open(self._proc_status)
            v = t.read()
            t.close()
        except:
            return 0.0           # non-Linux?
        i = v.index(VmKey)       # get VmKey line e.g. 'VmRSS:  9999  kB\n ...'
        v = v[i:].split(None, 3) # whitespace
        if len(v) < 3:
            return 0.0           # invalid format?
        # convert Vm value to bytes
        mem = float(v[1]) * self._scale[v[2]]
        return mem / self._scale[unit]
    #
    def getUsedMemory(self, unit="o"):
        "Renvoie la m�moire r�sidente utilis�e en octets"
        return self._VmB('VmRSS:', unit)
    #
    def getVirtualMemory(self, unit="o"):
        "Renvoie la m�moire totale utilis�e en octets"
        return self._VmB('VmSize:', unit)
    #
    def getUsedStacksize(self, unit="o"):
        "Renvoie la taille du stack utilis� en octets"
        return self._VmB('VmStk:', unit)
    #
    def getMaxUsedMemory(self, unit="o"):
        "Renvoie la m�moire r�sidente maximale mesur�e"
        return self._VmB('VmHWM:', unit)
    #
    def getMaxVirtualMemory(self, unit="o"):
        "Renvoie la m�moire totale maximale mesur�e"
        return self._VmB('VmPeak:', unit)

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
