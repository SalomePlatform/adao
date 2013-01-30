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
        "Retourne la version de python utilis�e"
        import sys
        return ".".join(map(str,sys.version_info[0:3]))

    def getNumpyVersion(self):
        "Retourne la version de numpy utilis�e"
        import numpy.version
        return numpy.version.version

    def getScipyVersion(self):
        "Retourne la version de scipy utilis�e"
        import scipy.version
        return scipy.version.version

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
    # plut�t : http://code.activestate.com/recipes/286222/ et les infos de
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
        "Renvoie la m�moire totale utilis�e en octets"
        mem = self._VmB('VmSize:', unit)
        self._max_mem = max(self._max_mem, mem)
        return mem
    #
    def getUsedResident(self, unit="o"):
        "Renvoie la m�moire r�sidente utilis�e en octets"
        mem = self._VmB('VmRSS:', unit)
        self._max_rss = max(self._max_rss, mem)
        return mem
    #
    def getUsedStacksize(self, unit="o"):
        "Renvoie la taille du stack utilis� en octets"
        mem = self._VmB('VmStk:', unit)
        self._max_sta = max(self._max_sta, mem)
        return mem
    #
    def getMaxUsedMemory(self):
        "Renvoie la m�moire totale maximale mesur�e"
        return self._max_mem
    #
    def getMaxUsedResident(self):
        "Renvoie la m�moire r�sidente maximale mesur�e"
        return self._max_rss
    #
    def getMaxUsedStacksize(self):
        "Renvoie la m�moire du stack maximale mesur�e"
        return self._max_sta

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'

    print PlatformInfo()
    print
    p = PlatformInfo()
    print "Les caract�ristiques d�taill�es des applications et outils sont :"
    print "  - Application.......:",p.getName()
    print "  - Version...........:",p.getVersion()
    print "  - Date Application..:",p.getDate()
    print "  - Python............:",p.getPythonVersion()
    print "  - Numpy.............:",p.getNumpyVersion()
    print "  - Scipy.............:",p.getScipyVersion()
    print
    
    p = PathManagement()
    print "Les chemins ajout�s au syst�me pour des outils :"
    for k,v in p.getpaths().items():
        print "  %12s : %s"%(k,os.path.basename(v))
    print

    m = SystemUsage()
    print "La m�moire disponible est la suivante :"
    print "  - m�moire totale....: %4.1f Mo"%m.getAvailableMemory("Mo")
    print "  - m�moire physique..: %4.1f Mo"%m.getAvailablePhysicalMemory("Mo")
    print "  - m�moire swap......: %4.1f Mo"%m.getAvailableSwapMemory("Mo")
    print "  - utilisable........: %4.1f Mo"%m.getUsableMemory("Mo")
    print "L'usage m�moire de cette ex�cution est le suivant :"
    print "  - m�moire totale....: %4.1f Mo"%m.getUsedMemory("Mo")
    print "  - m�moire r�sidente.: %4.1f Mo"%m.getUsedResident("Mo")
    print "  - taille de stack...: %4.1f Mo"%m.getUsedStacksize("Mo")
    print "Cr�ation d'un objet range(1000000) et mesure m�moire"
    x = range(1000000)
    print "  - m�moire totale....: %4.1f Mo"%m.getUsedMemory("Mo")
    print "Destruction de l'objet et mesure m�moire"
    del x
    print "  - m�moire totale....: %4.1f Mo"%m.getUsedMemory("Mo")
    print "L'usage m�moire maximal de cette ex�cution est le suivant :"
    print "  - m�moire totale....: %4.1f Mo"%m.getMaxUsedMemory()
    print "  - m�moire r�sidente.: %4.1f Mo"%m.getMaxUsedResident()
    print "  - taille de stack...: %4.1f Mo"%m.getMaxUsedStacksize()
    print
