#-*-coding:iso-8859-1-*-
#
# Copyright (C) 2008-2017 EDF R&D
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

"""
    Informations sur le code et la plateforme, et mise à jour des chemins

    La classe "PlatformInfo" permet de récupérer les informations générales sur
    le code et la plateforme sous forme de strings, ou d'afficher directement
    les informations disponibles par les méthodes. L'impression directe d'un
    objet de cette classe affiche les informations minimales. Par exemple :
        print PlatformInfo()
        print PlatformInfo().getVersion()
        created = PlatformInfo().getDate()

    La classe "PathManagement" permet de mettre à jour les chemins système pour
    ajouter les outils numériques, matrices... On l'utilise en instanciant
    simplement cette classe, sans meme récupérer d'objet :
        PathManagement()
"""
__author__ = "Jean-Philippe ARGAUD"
__all__ = []

import os, sys

# ==============================================================================
class PlatformInfo(object):
    """
    Rassemblement des informations sur le code et la plateforme
    """
    def __init__(self):
        "Sans effet"
        pass

    def getName(self):
        "Retourne le nom de l'application"
        import version as dav
        return dav.name

    def getVersion(self):
        "Retourne le numéro de la version"
        import version as dav
        return dav.version

    def getDate(self):
        "Retourne la date de création de la version"
        import version as dav
        return dav.date

    def getPythonVersion(self):
        "Retourne la version de python disponible"
        return ".".join([str(x) for x in sys.version_info[0:3]]) # map(str,sys.version_info[0:3]))

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
        except ImportError:
            return "0.0.0"

    def getGnuplotVersion(self):
        "Retourne la version de gnuplotpy disponible"
        try:
            import Gnuplot
            return Gnuplot.__version__
        except ImportError:
            return "0.0"

    def getSphinxVersion(self):
        "Retourne la version de sphinx disponible"
        try:
            import sphinx
            return sphinx.__version__
        except ImportError:
            return "0.0.0"

    def getNloptVersion(self):
        "Retourne la version de nlopt disponible"
        try:
            import nlopt
            return "%s.%s.%s"%(
                nlopt.version_major(),
                nlopt.version_minor(),
                nlopt.version_bugfix(),
                )
        except ImportError:
            return "0.0.0"

    def getCurrentMemorySize(self):
        "Retourne la taille mémoire courante utilisée"
        return 1

    def MaximumPrecision(self):
        "Retourne la precision maximale flottante pour Numpy"
        import numpy
        try:
            x = numpy.array([1.,], dtype='float128')
            mfp = 'float128'
        except:
            mfp = 'float64'
        return mfp

    def MachinePrecision(self):
        # Alternative sans module :
        # eps = 2.38
        # while eps > 0:
        #     old_eps = eps
        #     eps = (1.0 + eps/2) - 1.0
        return sys.float_info.epsilon

    def __str__(self):
        import version as dav
        return "%s %s (%s)"%(dav.name,dav.version,dav.date)

# ==============================================================================
try:
    import matplotlib
    has_matplotlib = True
except ImportError:
    has_matplotlib = False

try:
    import Gnuplot
    has_gnuplot = True
except ImportError:
    has_gnuplot = False

try:
    import sphinx
    has_sphinx = True
except ImportError:
    has_sphinx = False

try:
    import nlopt
    has_nlopt = True
except ImportError:
    has_nlopt = False

# ==============================================================================
def uniq(sequence):
    """
    Fonction pour rendre unique chaque élément d'une liste, en préservant l'ordre
    """
    __seen = set()
    return [x for x in sequence if x not in __seen and not __seen.add(x)]

# ==============================================================================
class PathManagement(object):
    """
    Mise à jour du path système pour les répertoires d'outils
    """
    def __init__(self):
        "Déclaration des répertoires statiques"
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
        Renvoie le dictionnaire des chemins ajoutés
        """
        return self.__paths

# ==============================================================================
class SystemUsage(object):
    """
    Permet de récupérer les différentes tailles mémoires du process courant
    """
    #
    # Le module resource renvoie 0 pour les tailles mémoire. On utilise donc
    # plutôt : http://code.activestate.com/recipes/286222/ et Wikipedia
    #
    _proc_status = '/proc/%d/status' % os.getpid()
    _memo_status = '/proc/meminfo'
    _scale = {
        'o'  : 1.0,     # Multiples SI de l'octet
        'ko' : 1.e3,
        'Mo' : 1.e6,
        'Go' : 1.e9,
        'kio': 1024.0,  # Multiples binaires de l'octet
        'Mio': 1024.0*1024.0,
        'Gio': 1024.0*1024.0*1024.0,
        'B':     1.0,   # Multiples binaires du byte=octet
        'kB' : 1024.0,
        'MB' : 1024.0*1024.0,
        'GB' : 1024.0*1024.0*1024.0,
        }
    #
    def __init__(self):
        "Sans effet"
        pass
    #
    def _VmA(self, VmKey, unit):
        "Lecture des paramètres mémoire de la machine"
        try:
            t = open(self._memo_status)
            v = t.read()
            t.close()
        except IOError:
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
        "Renvoie la mémoire physique utilisable en octets"
        return self._VmA('MemTotal:', unit)
    #
    def getAvailableSwapMemory(self, unit="o"):
        "Renvoie la mémoire swap utilisable en octets"
        return self._VmA('SwapTotal:', unit)
    #
    def getAvailableMemory(self, unit="o"):
        "Renvoie la mémoire totale (physique+swap) utilisable en octets"
        return self._VmA('MemTotal:', unit) + self._VmA('SwapTotal:', unit)
    #
    def getUsableMemory(self, unit="o"):
        """Renvoie la mémoire utilisable en octets
        Rq : il n'est pas sûr que ce décompte soit juste...
        """
        return self._VmA('MemFree:', unit) + self._VmA('SwapFree:', unit) + \
               self._VmA('Cached:', unit) + self._VmA('SwapCached:', unit)
    #
    def _VmB(self, VmKey, unit):
        "Lecture des paramètres mémoire du processus"
        try:
            t = open(self._proc_status)
            v = t.read()
            t.close()
        except IOError:
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
        "Renvoie la mémoire résidente utilisée en octets"
        return self._VmB('VmRSS:', unit)
    #
    def getVirtualMemory(self, unit="o"):
        "Renvoie la mémoire totale utilisée en octets"
        return self._VmB('VmSize:', unit)
    #
    def getUsedStacksize(self, unit="o"):
        "Renvoie la taille du stack utilisé en octets"
        return self._VmB('VmStk:', unit)
    #
    def getMaxUsedMemory(self, unit="o"):
        "Renvoie la mémoire résidente maximale mesurée"
        return self._VmB('VmHWM:', unit)
    #
    def getMaxVirtualMemory(self, unit="o"):
        "Renvoie la mémoire totale maximale mesurée"
        return self._VmB('VmPeak:', unit)

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
