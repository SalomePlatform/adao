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
    Modèles généraux pour les observers, le post-processing
"""
__author__ = "Jean-Philippe ARGAUD"
__all__ = ["ObserverTemplates"]

import numpy

# ==============================================================================
class TemplateStorage(object):
    """
    Classe générale de stockage de type dictionnaire étendu
    (Template)
    """
    def __init__( self, language = "fr_FR" ):
        self.__preferedLanguage = language
        self.__values           = {}
        self.__order            = -1

    def store( self, name = None, content = None, fr_FR = "", en_EN = "", order = "next" ):
        "D.store(k, c,  fr_FR, en_EN, o) -> Store template k and its main characteristics"
        if name is None or content is None:
            raise ValueError("To be consistent, the storage of a template must provide a name and a content.")
        if order == "next":
            self.__order += 1
        else:
            self.__order = int(order)
        self.__values[str(name)] = {
            'content': str(content),
            'fr_FR'  : str(fr_FR),
            'en_EN'  : str(en_EN),
            'order'  : int(self.__order),
            }

    def keys(self):
        "D.keys() -> list of D's keys"
        __keys = sorted(self.__values.keys())
        return __keys

    # def has_key(self, name):
    #     "D.has_key(k) -> True if D has a key k, else False"
    #     return name in self.__values

    def __contains__(self, name):
        "D.__contains__(k) -> True if D has a key k, else False"
        return name in self.__values

    def __len__(self):
        "x.__len__() <==> len(x)"
        return len(self.__values)

    def __getitem__(self, name=None ):
        "x.__getitem__(y) <==> x[y]"
        return self.__values[name]['content']

    def getdoc(self, name = None, lang = "fr_FR"):
        "D.getdoc(k, l) -> Return documentation of key k in language l"
        if lang not in self.__values[name]: lang = self.__preferedLanguage
        return self.__values[name][lang]

    def keys_in_presentation_order(self):
        "D.keys_in_presentation_order() -> list of D's keys in presentation order"
        __orders = []
        for k in self.keys():
            __orders.append( self.__values[k]['order'] )
        __reorder = numpy.array(__orders).argsort()
        return list(numpy.array(self.keys())[__reorder])

# ==============================================================================
ObserverTemplates = TemplateStorage()

ObserverTemplates.store(
    name    = "ValuePrinter",
    content = """print(str(info)+" "+str(var[-1]))""",
    fr_FR   = "Imprime sur la sortie standard la valeur courante de la variable",
    en_EN   = "Print on standard output the current value of the variable",
    order   = "next",
    )
ObserverTemplates.store(
    name    = "ValueAndIndexPrinter",
    content = """print(str(info)+(" index %i:"%(len(var)-1))+" "+str(var[-1]))""",
    fr_FR   = "Imprime sur la sortie standard la valeur courante de la variable, en ajoutant son index",
    en_EN   = "Print on standard output the current value of the variable, adding its index",
    order   = "next",
    )
ObserverTemplates.store(
    name    = "ValueSeriePrinter",
    content = """print(str(info)+" "+str(var[:]))""",
    fr_FR   = "Imprime sur la sortie standard la série des valeurs de la variable",
    en_EN   = "Print on standard output the value series of the variable",
    order   = "next",
    )
ObserverTemplates.store(
    name    = "ValueSaver",
    content = """import numpy, re\nv=numpy.array(var[-1], ndmin=1)\nglobal istep\ntry:\n    istep += 1\nexcept:\n    istep = 0\nf='/tmp/value_%s_%05i.txt'%(info,istep)\nf=re.sub('\\s','_',f)\nprint('Value saved in \"%s\"'%f)\nnumpy.savetxt(f,v)""",
    fr_FR   = "Enregistre la valeur courante de la variable dans un fichier du répertoire '/tmp' nommé 'value...txt' selon le nom de la variable et l'étape d'enregistrement",
    en_EN   = "Save the current value of the variable in a file of the '/tmp' directory named 'value...txt' from the variable name and the saving step",
    order   = "next",
    )
ObserverTemplates.store(
    name    = "ValueSerieSaver",
    content = """import numpy, re\nv=numpy.array(var[:],  ndmin=1)\nglobal istep\ntry:\n    istep += 1\nexcept:\n    istep = 0\nf='/tmp/value_%s_%05i.txt'%(info,istep)\nf=re.sub('\\s','_',f)\nprint('Value saved in \"%s\"'%f)\nnumpy.savetxt(f,v)""",
    fr_FR   = "Enregistre la série des valeurs de la variable dans un fichier du répertoire '/tmp' nommé 'value...txt' selon le nom de la variable et l'étape",
    en_EN   = "Save the value series of the variable in a file of the '/tmp' directory named 'value...txt' from the variable name and the saving step",
    order   = "next",
    )
ObserverTemplates.store(
    name    = "ValuePrinterAndSaver",
    content = """import numpy, re\nv=numpy.array(var[-1], ndmin=1)\nprint(str(info)+" "+str(v))\nglobal istep\ntry:\n    istep += 1\nexcept:\n    istep = 0\nf='/tmp/value_%s_%05i.txt'%(info,istep)\nf=re.sub('\\s','_',f)\nprint('Value saved in \"%s\"'%f)\nnumpy.savetxt(f,v)""",
    fr_FR   = "Imprime sur la sortie standard et, en même temps enregistre dans un fichier du répertoire '/tmp', la valeur courante de la variable",
    en_EN   = "Print on standard output and, in the same time save in a file of the '/tmp' directory, the current value of the variable",
    order   = "next",
    )
ObserverTemplates.store(
    name    = "ValueIndexPrinterAndSaver",
    content = """import numpy, re\nv=numpy.array(var[-1], ndmin=1)\nprint(str(info)+(" index %i:"%(len(var)-1))+" "+str(v))\nglobal istep\ntry:\n    istep += 1\nexcept:\n    istep = 0\nf='/tmp/value_%s_%05i.txt'%(info,istep)\nf=re.sub('\\s','_',f)\nprint('Value saved in \"%s\"'%f)\nnumpy.savetxt(f,v)""",
    fr_FR   = "Imprime sur la sortie standard et, en même temps enregistre dans un fichier du répertoire '/tmp', la valeur courante de la variable, en ajoutant son index",
    en_EN   = "Print on standard output and, in the same time save in a file of the '/tmp' directory, the current value of the variable, adding its index",
    order   = "next",
    )
ObserverTemplates.store(
    name    = "ValueSeriePrinterAndSaver",
    content = """import numpy, re\nv=numpy.array(var[:],  ndmin=1)\nprint(str(info)+" "+str(v))\nglobal istep\ntry:\n    istep += 1\nexcept:\n    istep = 0\nf='/tmp/value_%s_%05i.txt'%(info,istep)\nf=re.sub('\\s','_',f)\nprint('Value saved in \"%s\"'%f)\nnumpy.savetxt(f,v)""",
    fr_FR   = "Imprime sur la sortie standard et, en même temps, enregistre dans un fichier du répertoire '/tmp', la série des valeurs de la variable",
    en_EN   = "Print on standard output and, in the same time, save in a file of the '/tmp' directory, the value series of the variable",
    order   = "next",
    )
ObserverTemplates.store(
    name    = "ValueGnuPlotter",
    content = """import numpy, Gnuplot\nv=numpy.array(var[-1], ndmin=1)\nglobal ifig, gp\ntry:\n    ifig += 1\n    gp(' set style data lines')\nexcept:\n    ifig = 0\n    gp = Gnuplot.Gnuplot(persist=1)\n    gp(' set style data lines')\ngp('set title  \"%s (Figure %i)\"'%(info,ifig))\ngp.plot( Gnuplot.Data( v, with_='lines lw 2' ) )""",
    fr_FR   = "Affiche graphiquement avec Gnuplot la valeur courante de la variable",
    en_EN   = "Graphically plot with Gnuplot the current value of the variable",
    order   = "next",
    )
ObserverTemplates.store(
    name    = "ValueSerieGnuPlotter",
    content = """import numpy, Gnuplot\nv=numpy.array(var[:],  ndmin=1)\nglobal ifig, gp\ntry:\n    ifig += 1\n    gp(' set style data lines')\nexcept:\n    ifig = 0\n    gp = Gnuplot.Gnuplot(persist=1)\n    gp(' set style data lines')\ngp('set title  \"%s (Figure %i)\"'%(info,ifig))\ngp.plot( Gnuplot.Data( v, with_='lines lw 2' ) )""",
    fr_FR   = "Affiche graphiquement avec Gnuplot la série des valeurs de la variable",
    en_EN   = "Graphically plot with Gnuplot the value series of the variable",
    order   = "next",
    )
ObserverTemplates.store(
    name    = "ValuePrinterAndGnuPlotter",
    content = """print(str(info)+" "+str(var[-1]))\nimport numpy, Gnuplot\nv=numpy.array(var[-1], ndmin=1)\nglobal ifig,gp\ntry:\n    ifig += 1\n    gp(' set style data lines')\nexcept:\n    ifig = 0\n    gp = Gnuplot.Gnuplot(persist=1)\n    gp(' set style data lines')\ngp('set title  \"%s (Figure %i)\"'%(info,ifig))\ngp.plot( Gnuplot.Data( v, with_='lines lw 2' ) )""",
    fr_FR   = "Imprime sur la sortie standard et, en même temps, affiche graphiquement avec Gnuplot la valeur courante de la variable",
    en_EN   = "Print on standard output and, in the same time, graphically plot with Gnuplot the current value of the variable",
    order   = "next",
    )
ObserverTemplates.store(
    name    = "ValueSeriePrinterAndGnuPlotter",
    content = """print(str(info)+" "+str(var[:]))\nimport numpy, Gnuplot\nv=numpy.array(var[:],  ndmin=1)\nglobal ifig,gp\ntry:\n    ifig += 1\n    gp(' set style data lines')\nexcept:\n    ifig = 0\n    gp = Gnuplot.Gnuplot(persist=1)\n    gp(' set style data lines')\ngp('set title  \"%s (Figure %i)\"'%(info,ifig))\ngp.plot( Gnuplot.Data( v, with_='lines lw 2' ) )""",
    fr_FR   = "Imprime sur la sortie standard et, en même temps, affiche graphiquement avec Gnuplot la série des valeurs de la variable",
    en_EN   = "Print on standard output and, in the same time, graphically plot with Gnuplot the value series of the variable",
    order   = "next",
    )
ObserverTemplates.store(
    name    = "ValuePrinterSaverAndGnuPlotter",
    content = """print(str(info)+" "+str(var[-1]))\nimport numpy, re\nv=numpy.array(var[-1], ndmin=1)\nglobal istep\ntry:\n    istep += 1\nexcept:\n    istep = 0\nf='/tmp/value_%s_%05i.txt'%(info,istep)\nf=re.sub('\\s','_',f)\nprint('Value saved in \"%s\"'%f)\nnumpy.savetxt(f,v)\nimport Gnuplot\nglobal ifig,gp\ntry:\n    ifig += 1\n    gp(' set style data lines')\nexcept:\n    ifig = 0\n    gp = Gnuplot.Gnuplot(persist=1)\n    gp(' set style data lines')\ngp('set title  \"%s (Figure %i)\"'%(info,ifig))\ngp.plot( Gnuplot.Data( v, with_='lines lw 2' ) )""",
    fr_FR   = "Imprime sur la sortie standard et, en même temps, enregistre dans un fichier du répertoire '/tmp' et affiche graphiquement la valeur courante de la variable",
    en_EN   = "Print on standard output and, in the same, time save in a file of the '/tmp' directory and graphically plot the current value of the variable",
    order   = "next",
    )
ObserverTemplates.store(
    name    = "ValueSeriePrinterSaverAndGnuPlotter",
    content = """print(str(info)+" "+str(var[:]))\nimport numpy, re\nv=numpy.array(var[:],  ndmin=1)\nglobal istep\ntry:\n    istep += 1\nexcept:\n    istep = 0\nf='/tmp/value_%s_%05i.txt'%(info,istep)\nf=re.sub('\\s','_',f)\nprint('Value saved in \"%s\"'%f)\nnumpy.savetxt(f,v)\nimport Gnuplot\nglobal ifig,gp\ntry:\n    ifig += 1\n    gp(' set style data lines')\nexcept:\n    ifig = 0\n    gp = Gnuplot.Gnuplot(persist=1)\n    gp(' set style data lines')\ngp('set title  \"%s (Figure %i)\"'%(info,ifig))\ngp.plot( Gnuplot.Data( v, with_='lines lw 2' ) )""",
    fr_FR   = "Imprime sur la sortie standard et, en même temps, enregistre dans un fichier du répertoire '/tmp' et affiche graphiquement la série des valeurs de la variable",
    en_EN   = "Print on standard output and, in the same, time save in a file of the '/tmp' directory and graphically plot the value series of the variable",
    order   = "next",
    )
ObserverTemplates.store(
    name    = "ValueMean",
    content = """import numpy\nprint(str(info)+" "+str(numpy.nanmean(var[-1])))""",
    fr_FR   = "Imprime sur la sortie standard la moyenne de la valeur courante de la variable",
    en_EN   = "Print on standard output the mean of the current value of the variable",
    order   = "next",
    )
ObserverTemplates.store(
    name    = "ValueStandardError",
    content = """import numpy\nprint(str(info)+" "+str(numpy.nanstd(var[-1])))""",
    fr_FR   = "Imprime sur la sortie standard l'écart-type de la valeur courante de la variable",
    en_EN   = "Print on standard output the standard error of the current value of the variable",
    order   = "next",
    )
ObserverTemplates.store(
    name    = "ValueVariance",
    content = """import numpy\nprint(str(info)+" "+str(numpy.nanvar(var[-1])))""",
    fr_FR   = "Imprime sur la sortie standard la variance de la valeur courante de la variable",
    en_EN   = "Print on standard output the variance of the current value of the variable",
    order   = "next",
    )
ObserverTemplates.store(
    name    = "ValueL2Norm",
    content = """import numpy\nv = numpy.ravel( var[-1] )\nprint(str(info)+" "+str(float( numpy.linalg.norm(v) )))""",
    fr_FR   = "Imprime sur la sortie standard la norme L2 de la valeur courante de la variable",
    en_EN   = "Print on standard output the L2 norm of the current value of the variable",
    order   = "next",
    )
ObserverTemplates.store(
    name    = "ValueRMS",
    content = """import numpy\nv = numpy.ravel( var[-1] )\nprint(str(info)+" "+str(float( numpy.sqrt((1./v.size)*numpy.dot(v,v)) )))""",
    fr_FR   = "Imprime sur la sortie standard la racine de la moyenne des carrés (RMS), ou moyenne quadratique, de la valeur courante de la variable",
    en_EN   = "Print on standard output the root mean square (RMS), or quadratic mean, of the current value of the variable",
    order   = "next",
    )

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
