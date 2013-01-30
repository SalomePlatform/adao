#-*-coding:iso-8859-1-*-
#
# Copyright (C) 2008-2013 EDF R&D
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

__doc__ = """
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
        "Retourne le numéro de la version"
        import version
        return version.version

    def getDate(self):
        "Retourne la date de création de la version"
        import version
        return version.date
    
    def getPythonVersion(self):
        "Retourne la version de python utilisée"
        import sys
        return ".".join(map(str,sys.version_info[0:3]))

    def getNumpyVersion(self):
        "Retourne la version de numpy utilisée"
        import numpy.version
        return numpy.version.version

    def getScipyVersion(self):
        "Retourne la version de scipy utilisée"
        import scipy.version
        return scipy.version.version

    def getCurrentMemorySize(self):
        "Retourne la taille mémoire courante utilisée"
        return 1

    def __str__(self):
        import version
        return "%s %s (%s)"%(version.name,version.version,version.date)

# ==============================================================================
def uniq(sequence):
    """
    Fonction pour rendre unique chaque élément d'une liste, en préservant l'ordre
    """
    __seen = set()
    return [x for x in sequence if x not in __seen and not __seen.add(x)]

# ==============================================================================
class PathManagement:
    """
    Mise à jour du path système pour les répertoires d'outils
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
        Renvoie le dictionnaire des chemins ajoutés
        """
        return self.__paths

# ==============================================================================
class SystemUsage:
    """
    Permet de récupérer les différentes tailles mémoires du process courant
    """
    #
    # Le module resource renvoie 0 pour les tailles mémoire. On utilise donc
    # plutôt : http://code.activestate.com/recipes/286222/ et les infos de
    # http://www.redhat.com/docs/manuals/enterprise/RHEL-4-Manual/en-US/Reference_Guide/s2-proc-meminfo.html
    #
    _proc_status = '/proc/%d/status' % os.getpid()
    _memo_status = '/proc/meminfo'
    _scale = {
                      'K' : 1024.0, 'M' : 1024.0*1024.0,
        'o':     1.0, 'ko': 1024.0, 'mo': 1024.0*1024.0,
                      'Ko': 1024.0, 'Mo': 1024.0*1024.0,
        'B':     1.0, 'kB': 1024.0, 'mB': 1024.0*1024.0,
                      'KB': 1024.0, 'MB': 1024.0*1024.0,
             }
    _max_mem = 0
    _max_rss = 0
    _max_sta = 0
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
        "Renvoie la mémoire totale utilisée en octets"
        mem = self._VmB('VmSize:', unit)
        self._max_mem = max(self._max_mem, mem)
        return mem
    #
    def getUsedResident(self, unit="o"):
        "Renvoie la mémoire résidente utilisée en octets"
        mem = self._VmB('VmRSS:', unit)
        self._max_rss = max(self._max_rss, mem)
        return mem
    #
    def getUsedStacksize(self, unit="o"):
        "Renvoie la taille du stack utilisé en octets"
        mem = self._VmB('VmStk:', unit)
        self._max_sta = max(self._max_sta, mem)
        return mem
    #
    def getMaxUsedMemory(self):
        "Renvoie la mémoire totale maximale mesurée"
        return self._max_mem
    #
    def getMaxUsedResident(self):
        "Renvoie la mémoire résidente maximale mesurée"
        return self._max_rss
    #
    def getMaxUsedStacksize(self):
        "Renvoie la mémoire du stack maximale mesurée"
        return self._max_sta

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'

    print PlatformInfo()
    print
    p = PlatformInfo()
    print "Les caractéristiques détaillées des applications et outils sont :"
    print "  - Application.......:",p.getName()
    print "  - Version...........:",p.getVersion()
    print "  - Date Application..:",p.getDate()
    print "  - Python............:",p.getPythonVersion()
    print "  - Numpy.............:",p.getNumpyVersion()
    print "  - Scipy.............:",p.getScipyVersion()
    print
    
    p = PathManagement()
    print "Les chemins ajoutés au système pour des outils :"
    for k,v in p.getpaths().items():
        print "  %12s : %s"%(k,os.path.basename(v))
    print

    m = SystemUsage()
    print "La mémoire disponible est la suivante :"
    print "  - mémoire totale....: %4.1f Mo"%m.getAvailableMemory("Mo")
    print "  - mémoire physique..: %4.1f Mo"%m.getAvailablePhysicalMemory("Mo")
    print "  - mémoire swap......: %4.1f Mo"%m.getAvailableSwapMemory("Mo")
    print "  - utilisable........: %4.1f Mo"%m.getUsableMemory("Mo")
    print "L'usage mémoire de cette exécution est le suivant :"
    print "  - mémoire totale....: %4.1f Mo"%m.getUsedMemory("Mo")
    print "  - mémoire résidente.: %4.1f Mo"%m.getUsedResident("Mo")
    print "  - taille de stack...: %4.1f Mo"%m.getUsedStacksize("Mo")
    print "Création d'un objet range(1000000) et mesure mémoire"
    x = range(1000000)
    print "  - mémoire totale....: %4.1f Mo"%m.getUsedMemory("Mo")
    print "Destruction de l'objet et mesure mémoire"
    del x
    print "  - mémoire totale....: %4.1f Mo"%m.getUsedMemory("Mo")
    print "L'usage mémoire maximal de cette exécution est le suivant :"
    print "  - mémoire totale....: %4.1f Mo"%m.getMaxUsedMemory()
    print "  - mémoire résidente.: %4.1f Mo"%m.getMaxUsedResident()
    print "  - taille de stack...: %4.1f Mo"%m.getMaxUsedStacksize()
    print
