# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2020 EDF R&D
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
        print(PlatformInfo())
        print(PlatformInfo().getVersion())
        created = PlatformInfo().getDate()

    La classe "PathManagement" permet de mettre à jour les chemins système pour
    ajouter les outils numériques, matrices... On l'utilise en instanciant
    simplement cette classe, sans meme récupérer d'objet :
        PathManagement()

    La classe "SystemUsage" permet de  sous Unix les différentes tailles
    mémoires du process courant. Ces tailles peuvent être assez variables et
    dépendent de la fiabilité des informations du système dans le suivi des
    process.
"""
__author__ = "Jean-Philippe ARGAUD"
__all__ = []

import os
import sys
import platform
import locale
import logging

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
        import daCore.version as dav
        return dav.name

    def getVersion(self):
        "Retourne le numéro de la version"
        import daCore.version as dav
        return dav.version

    def getDate(self):
        "Retourne la date de création de la version"
        import daCore.version as dav
        return dav.date

    def getYear(self):
        "Retourne l'année de création de la version"
        import daCore.version as dav
        return dav.year

    def getSystemInformation(self, __prefix=""):
        __msg  = ""
        __msg += "\n%s%30s : %s" %(__prefix,"platform.system",platform.system())
        __msg += "\n%s%30s : %s" %(__prefix,"sys.platform",sys.platform)
        __msg += "\n%s%30s : %s" %(__prefix,"platform.version",platform.version())
        __msg += "\n%s%30s : %s" %(__prefix,"platform.platform",platform.platform())
        __msg += "\n%s%30s : %s" %(__prefix,"platform.machine",platform.machine())
        if len(platform.processor())>0:
            __msg += "\n%s%30s : %s" %(__prefix,"platform.processor",platform.processor())
        #
        if sys.platform.startswith('linux'):
            if hasattr(platform, 'linux_distribution'):
                __msg += "\n%s%30s : %s" %(__prefix,
                    "platform.linux_distribution",str(platform.linux_distribution()))
            else:
                __msg += "\n%s%30s : %s" %(__prefix,"platform.dist",str(platform.dist()))
        elif sys.platform.startswith('darwin'):
            if hasattr(platform, 'mac_ver'):
                __macosxv = {'5': 'Leopard',       '6': 'Snow Leopard', '7': 'Lion',
                             '8': 'Mountain Lion', '9': 'Mavericks',   '10': 'Yosemite',
                             '11': 'El Capitan',  '12': 'Sierra'}
                for key in __macosxv:
                    if (platform.mac_ver()[0].split('.')[1] == key):
                        __msg += "\n%s%30s : %s" %(__prefix,
                            "platform.mac_ver",str(platform.mac_ver()[0]+"(" + macosx_dict[key]+")"))
            else:
                __msg += "\n%s%30s : %s" %(__prefix,"platform.dist",str(platform.dist()))
        elif os.name == 'nt':
            __msg += "\n%s%30s : %s" %(__prefix,"platform.win32_ver",platform.win32_ver()[1])
        #
        __msg += "\n"
        __msg += "\n%s%30s : %s" %(__prefix,"platform.python_implementation",platform.python_implementation())
        __msg += "\n%s%30s : %s" %(__prefix,"sys.executable",sys.executable)
        __msg += "\n%s%30s : %s" %(__prefix,"sys.version",sys.version.replace('\n',''))
        __msg += "\n%s%30s : %s" %(__prefix,"sys.getfilesystemencoding",str(sys.getfilesystemencoding()))
        __msg += "\n%s%30s : %s" %(__prefix,"locale.getdefaultlocale",str(locale.getdefaultlocale()))
        __msg += "\n"
        __msg += "\n%s%30s : %s" %(__prefix,"platform.node",platform.node())
        __msg += "\n%s%30s : %s" %(__prefix,"os.path.expanduser",os.path.expanduser('~'))
        return __msg

    def getPythonVersion(self):
        "Retourne la version de python disponible"
        return ".".join([str(x) for x in sys.version_info[0:3]]) # map(str,sys.version_info[0:3]))

    def getNumpyVersion(self):
        "Retourne la version de numpy disponible"
        import numpy.version
        return numpy.version.version

    def getScipyVersion(self):
        "Retourne la version de scipy disponible"
        if has_scipy:
            __version = scipy.version.version
        else:
            __version = "0.0.0"
        return __version

    def getMatplotlibVersion(self):
        "Retourne la version de matplotlib disponible"
        if has_matplotlib:
            __version = matplotlib.__version__
        else:
            __version = "0.0.0"
        return __version

    def getGnuplotVersion(self):
        "Retourne la version de gnuplotpy disponible"
        if has_gnuplot:
            __version = Gnuplot.__version__
        else:
            __version = "0.0"
        return __version

    def getSphinxVersion(self):
        "Retourne la version de sphinx disponible"
        if has_sphinx:
            __version = sphinx.__version__
        else:
            __version = "0.0.0"
        return __version

    def getNloptVersion(self):
        "Retourne la version de nlopt disponible"
        if has_nlopt:
            __version = "%s.%s.%s"%(
                nlopt.version_major(),
                nlopt.version_minor(),
                nlopt.version_bugfix(),
                )
        else:
            __version = "0.0.0"
        return __version

    def getCurrentMemorySize(self):
        "Retourne la taille mémoire courante utilisée"
        return 1

    def MaximumPrecision(self):
        "Retourne la precision maximale flottante pour Numpy"
        import numpy
        try:
            numpy.array([1.,], dtype='float128')
            mfp = 'float128'
        except Exception:
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
        import daCore.version as dav
        return "%s %s (%s)"%(dav.name,dav.version,dav.date)

# ==============================================================================
try:
    import scipy
    import scipy.version
    import scipy.optimize
    has_scipy = True
except ImportError:
    has_scipy = False

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

try:
    import sdf
    has_sdf = True
except ImportError:
    has_sdf = False

has_salome = bool( "ROOT_SALOME"   in os.environ )
has_yacs   = bool( "YACS_ROOT_DIR" in os.environ )
has_adao   = bool( "ADAO_ROOT_DIR" in os.environ )
has_eficas = bool( "EFICAS_ROOT_DIR" in os.environ )

# ==============================================================================
def uniq( __sequence ):
    """
    Fonction pour rendre unique chaque élément d'une liste, en préservant l'ordre
    """
    __seen = set()
    return [x for x in __sequence if x not in __seen and not __seen.add(x)]

def isIterable( __sequence, __check = False, __header = "" ):
    """
    Vérification que l'argument est un itérable
    """
    if  isinstance( __sequence, (list, tuple, map) ):
        __isOk = True
    elif type(__sequence).__name__ in ('generator','range'):
        __isOk = True
    elif "_iterator" in type(__sequence).__name__:
        __isOk = True
    else:
        __isOk = False
    if __check and not __isOk:
        raise TypeError("Not iterable or unkown input type%s: %s"%(__header, type(__sequence),))
    return __isOk

def date2int( __date, __lang="FR" ):
    """
    Fonction de secours, conversion pure : dd/mm/yy hh:mm ---> int(yyyymmddhhmm)
    """
    __date = __date.strip()
    if __date.count('/') == 2 and __date.count(':') == 0 and __date.count(' ') == 0:
        d,m,y = __date.split("/")
        __number = (10**4)*int(y)+(10**2)*int(m)+int(d)
    elif __date.count('/') == 2 and __date.count(':') == 1 and __date.count(' ') > 0:
        part1, part2 = __date.split()
        d,m,y = part1.strip().split("/")
        h,n   = part2.strip().split(":")
        __number = (10**8)*int(y)+(10**6)*int(m)+(10**4)*int(d)+(10**2)*int(h)+int(n)
    else:
        raise ValueError("Cannot convert \"%s\" as a D/M/Y H:M date"%d)
    return __number

def checkFileNameConformity( __filename, __warnInsteadOfPrint=True ):
    if sys.platform.startswith("win") and len(__filename) > 256:
        __conform = False
        __msg = (" For some shared or older file systems on Windows, a file "+\
            "name longer than 256 characters can lead to access problems."+\
            "\n  The name of the file in question is the following:"+\
            "\n  %s")%(__filename,)
        if __warnInsteadOfPrint: logging.warning(__msg)
        else:                    print(__msg)
    else:
        __conform = True
    #
    return __conform

def checkFileNameImportability( __filename, __warnInsteadOfPrint=True ):
    if str(__filename).count(".") > 1:
        __conform = False
        __msg = (" The file name contains %i point(s) before the extension "+\
            "separator, which can potentially lead to problems when "+\
            "importing this file into Python, as it can then be recognized "+\
            "as a sub-module (generating a \"ModuleNotFoundError\"). If it "+\
            "is intentional, make sure that there is no module with the "+\
            "same name as the part before the first point, and that there is "+\
            "no \"__init__.py\" file in the same directory."+\
            "\n  The name of the file in question is the following:"+\
            "\n  %s")%(int(str(__filename).count(".")-1), __filename)
        if __warnInsteadOfPrint: logging.warning(__msg)
        else:                    print(__msg)
    else:
        __conform = True
    #
    return __conform

# ==============================================================================
class PathManagement(object):
    """
    Mise à jour du path système pour les répertoires d'outils
    """
    def __init__(self):
        "Déclaration des répertoires statiques"
        parent = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
        self.__paths = {}
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
    print('\n AUTODIAGNOSTIC\n')
