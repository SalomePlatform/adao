# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2025 EDF R&D
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
Modèles généraux pour les observers, le post-processing.
"""
__author__ = "Jean-Philippe ARGAUD"
__all__ = ["ObserverTemplates"]

# flake8: noqa

import numpy


# ==============================================================================
class TemplateStorage(object):
    """
    Classe générale de stockage de type dictionnaire étendu (Template).
    """

    __slots__ = ("__preferedLanguage", "__values", "__order")

    def __init__(self, language="fr_FR"):
        self.__preferedLanguage = language
        self.__values = {}
        self.__order = -1

    def store(self, name=None, content=None, fr_FR="", en_EN="", order="next"):
        """Store named template and its main characteristics."""
        if name is None or content is None:
            raise ValueError(
                "To be consistent, the storage of a template must provide a name and a content."
            )
        if order == "next":
            self.__order += 1
        else:
            self.__order = int(order)
        self.__values[str(name)] = {
            "content": str(content),
            "fr_FR": str(fr_FR),
            "en_EN": str(en_EN),
            "order": int(self.__order),
        }

    def keys(self):
        """Return the list of self's keys."""
        __keys = sorted(self.__values.keys())
        return __keys

    def __contains__(self, name):
        """True if the dictionary has the specified key, else False."""
        return name in self.__values

    def __len__(self):
        """Return len(self)."""
        return len(self.__values)

    def __getitem__(self, name=None):
        """Return self[name]."""
        return self.__values[name]["content"]

    def getdoc(self, name=None, lang="fr_FR"):
        """Return documentation of key name in language lang."""
        if lang not in self.__values[name]:
            lang = self.__preferedLanguage
        return self.__values[name][lang]

    def keys_in_presentation_order(self):
        """Return the list of self's keys in presentation order."""
        __orders = []
        for ik in self.keys():
            __orders.append(self.__values[ik]["order"])
        __reorder = numpy.array(__orders).argsort()
        return (numpy.array(self.keys())[__reorder]).tolist()


# ==============================================================================
ObserverTemplates = TemplateStorage()

ObserverTemplates.store(
    name="ValuePrinter",
    content="""print(str(info)+" "+str(var[-1]))""",
    fr_FR="Imprime sur la sortie standard la valeur courante de la variable",
    en_EN="Print on standard output the current value of the variable",
    order="next",
)
ObserverTemplates.store(
    name="ValueAndIndexPrinter",
    content="""print(str(info)+(" index %i:"%(len(var)-1))+" "+str(var[-1]))""",
    fr_FR="Imprime sur la sortie standard la valeur courante de la variable, en ajoutant son index",
    en_EN="Print on standard output the current value of the variable, adding its index",
    order="next",
)
ObserverTemplates.store(
    name="ValueSeriePrinter",
    content="""print(str(info)+" "+str(var[:]))""",
    fr_FR="Imprime sur la sortie standard la série des valeurs de la variable",
    en_EN="Print on standard output the value series of the variable",
    order="next",
)
ObserverTemplates.store(
    name="ValueSaver",
    content="""import os.path, numpy, re, tempfile\ntempdir=tempfile.gettempdir()\nv=numpy.array(var[-1], ndmin=1)\nglobal istep\ntry:\n    istep+=1\nexcept:\n    istep=0\nf=os.path.join(tempdir,'value_%s_%05i.txt'%(info,istep))\nf=re.sub(r'\\s','_',f)\nprint('Value saved in \"%s\"'%f)\nnumpy.savetxt(f,v)""",
    fr_FR="Enregistre la valeur courante de la variable dans un fichier situé dans le répertoire temporaire du système nommé 'value...txt' selon le nom de la variable et l'étape d'enregistrement",
    en_EN="Save the current value of the variable in a file available in the system temporary directory named 'value...txt' from the variable name and the saving step",
    order="next",
)
ObserverTemplates.store(
    name="ValueSerieSaver",
    content="""import os.path, numpy, re, tempfile\ntempdir=tempfile.gettempdir()\nv=numpy.array(var[:], ndmin=1)\nglobal istep\ntry:\n    istep+=1\nexcept:\n    istep=0\nf=os.path.join(tempdir,'value_%s_%05i.txt'%(info,istep))\nf=re.sub(r'\\s','_',f)\nprint('Value saved in \"%s\"'%f)\nnumpy.savetxt(f,v)""",
    fr_FR="Enregistre la série des valeurs de la variable dans un fichier situé dans le répertoire temporaire du système nommé 'value...txt' selon le nom de la variable et l'étape",
    en_EN="Save the value series of the variable in a file available in the system temporary directory named 'value...txt' from the variable name and the saving step",
    order="next",
)
ObserverTemplates.store(
    name="ValuePrinterAndSaver",
    content="""import os.path, numpy, re, tempfile\ntempdir=tempfile.gettempdir()\nv=numpy.array(var[-1], ndmin=1)\nprint(str(info)+" "+str(v))\nglobal istep\ntry:\n    istep+=1\nexcept:\n    istep=0\nf=os.path.join(tempdir,'value_%s_%05i.txt'%(info,istep))\nf=re.sub(r'\\s','_',f)\nprint('Value saved in \"%s\"'%f)\nnumpy.savetxt(f,v)""",
    fr_FR="Imprime sur la sortie standard et, en même temps enregistre dans un fichier situé dans le répertoire temporaire du système, la valeur courante de la variable",
    en_EN="Print on standard output and, in the same time save in a file available in the system temporary directory, the current value of the variable",
    order="next",
)
ObserverTemplates.store(
    name="ValueIndexPrinterAndSaver",
    content="""import os.path, numpy, re, tempfile\ntempdir=tempfile.gettempdir()\nv=numpy.array(var[-1], ndmin=1)\nprint(str(info)+(" index %i:"%(len(var)-1))+" "+str(v))\nglobal istep\ntry:\n    istep+=1\nexcept:\n    istep=0\nf=os.path.join(tempdir,'value_%s_%05i.txt'%(info,istep))\nf=re.sub(r'\\s','_',f)\nprint('Value saved in \"%s\"'%f)\nnumpy.savetxt(f,v)""",
    fr_FR="Imprime sur la sortie standard et, en même temps enregistre dans un fichier situé dans le répertoire temporaire du système, la valeur courante de la variable, en ajoutant son index",
    en_EN="Print on standard output and, in the same time save in a file available in the system temporary directory, the current value of the variable, adding its index",
    order="next",
)
ObserverTemplates.store(
    name="ValueSeriePrinterAndSaver",
    content="""import os.path, numpy, re, tempfile\ntempdir=tempfile.gettempdir()\nv=numpy.array(var[:], ndmin=1)\nprint(str(info)+" "+str(v))\nglobal istep\ntry:\n    istep+=1\nexcept:\n    istep=0\nf=os.path.join(tempdir,'value_%s_%05i.txt'%(info,istep))\nf=re.sub(r'\\s','_',f)\nprint('Value saved in \"%s\"'%f)\nnumpy.savetxt(f,v)""",
    fr_FR="Imprime sur la sortie standard et, en même temps, enregistre dans un fichier situé dans le répertoire temporaire du système, la série des valeurs de la variable",
    en_EN="Print on standard output and, in the same time, save in a file available in the system temporary directory, the value series of the variable",
    order="next",
)
ObserverTemplates.store(
    name="ValueGnuPlotter",
    content="""import numpy, Gnuplot\nv=numpy.array(var[-1], ndmin=1)\nglobal igfig, gp\ntry:\n    igfig+=1\n    gp('set title \"%s (Figure %i)\"'%(info,igfig))\nexcept:\n    igfig=0\n    gp=Gnuplot.Gnuplot(persist=1)\n    gp('set title \"%s (Figure %i)\"'%(info,igfig))\n    gp('set style data lines')\ngp.plot( Gnuplot.Data( v, with_='lines lw 2' ) )""",
    fr_FR="Affiche graphiquement avec Gnuplot la valeur courante de la variable (affichage persistant)",
    en_EN="Graphically plot with Gnuplot the current value of the variable (persistent plot)",
    order="next",
)
ObserverTemplates.store(
    name="ValueSerieGnuPlotter",
    content="""import numpy, Gnuplot\nv=numpy.array(var[:], ndmin=1)\nglobal igfig, gp\ntry:\n    igfig+=1\n    gp('set title \"%s (Figure %i)\"'%(info,igfig))\nexcept:\n    igfig=0\n    gp=Gnuplot.Gnuplot(persist=1)\n    gp('set title \"%s (Figure %i)\"'%(info,igfig))\n    gp('set style data lines')\n    gp('set xlabel \"Step\"')\n    gp('set ylabel \"Variable\"')\ngp.plot( Gnuplot.Data( v, with_='lines lw 2' ) )""",
    fr_FR="Affiche graphiquement avec Gnuplot la série des valeurs de la variable (affichage persistant)",
    en_EN="Graphically plot with Gnuplot the value series of the variable (persistent plot)",
    order="next",
)
ObserverTemplates.store(
    name="ValuePrinterAndGnuPlotter",
    content="""print(str(info)+' '+str(var[-1]))\nimport numpy, Gnuplot\nv=numpy.array(var[-1], ndmin=1)\nglobal igfig, gp\ntry:\n    igfig+=1\n    gp('set title \"%s (Figure %i)\"'%(info,igfig))\nexcept:\n    igfig=0\n    gp=Gnuplot.Gnuplot(persist=1)\n    gp('set title \"%s (Figure %i)\"'%(info,igfig))\n    gp('set style data lines')\ngp.plot( Gnuplot.Data( v, with_='lines lw 2' ) )""",
    fr_FR="Imprime sur la sortie standard et, en même temps, affiche graphiquement avec Gnuplot la valeur courante de la variable (affichage persistant)",
    en_EN="Print on standard output and, in the same time, graphically plot with Gnuplot the current value of the variable (persistent plot)",
    order="next",
)
ObserverTemplates.store(
    name="ValueSeriePrinterAndGnuPlotter",
    content="""print(str(info)+' '+str(var[:]))\nimport numpy, Gnuplot\nv=numpy.array(var[:], ndmin=1)\nglobal igfig, gp\ntry:\n    igfig+=1\n    gp('set title \"%s (Figure %i)\"'%(info,igfig))\nexcept:\n    igfig=0\n    gp=Gnuplot.Gnuplot(persist=1)\n    gp('set title \"%s (Figure %i)\"'%(info,igfig))\n    gp('set style data lines')\n    gp('set xlabel \"Step\"')\n    gp('set ylabel \"Variable\"')\ngp.plot( Gnuplot.Data( v, with_='lines lw 2' ) )""",
    fr_FR="Imprime sur la sortie standard et, en même temps, affiche graphiquement avec Gnuplot la série des valeurs de la variable (affichage persistant)",
    en_EN="Print on standard output and, in the same time, graphically plot with Gnuplot the value series of the variable (persistent plot)",
    order="next",
)
ObserverTemplates.store(
    name="ValuePrinterSaverAndGnuPlotter",
    content="""print(str(info)+' '+str(var[-1]))\nimport os.path, numpy, re, tempfile\ntempdir=tempfile.gettempdir()\nv=numpy.array(var[-1], ndmin=1)\nglobal istep\ntry:\n    istep+=1\nexcept:\n    istep=0\nf=os.path.join(tempdir,'value_%s_%05i.txt'%(info,istep))\nf=re.sub(r'\\s','_',f)\nprint('Value saved in \"%s\"'%f)\nnumpy.savetxt(f,v)\nimport Gnuplot\nglobal igfig, gp\ntry:\n    igfig+=1\n    gp('set title \"%s (Figure %i)\"'%(info,igfig))\nexcept:\n    igfig=0\n    gp=Gnuplot.Gnuplot(persist=1)\n    gp('set title \"%s (Figure %i)\"'%(info,igfig))\n    gp('set style data lines')\ngp.plot( Gnuplot.Data( v, with_='lines lw 2' ) )""",
    fr_FR="Imprime sur la sortie standard et, en même temps, enregistre dans un fichier situé dans le répertoire temporaire du système et affiche graphiquement avec Gnuplot la valeur courante de la variable (affichage persistant)",
    en_EN="Print on standard output and, in the same, time save in a file available in the system temporary directory and graphically plot with Gnuplot the current value of the variable (persistent plot)",
    order="next",
)
ObserverTemplates.store(
    name="ValueSeriePrinterSaverAndGnuPlotter",
    content="""print(str(info)+' '+str(var[:]))\nimport os.path, numpy, re, tempfile\ntempdir=tempfile.gettempdir()\nv=numpy.array(var[:], ndmin=1)\nglobal istep\ntry:\n    istep+=1\nexcept:\n    istep=0\nf=os.path.join(tempdir,'value_%s_%05i.txt'%(info,istep))\nf=re.sub(r'\\s','_',f)\nprint('Value saved in \"%s\"'%f)\nnumpy.savetxt(f,v)\nimport Gnuplot\nglobal igfig, gp\ntry:\n    igfig+=1\n    gp('set title \"%s (Figure %i)\"'%(info,igfig))\nexcept:\n    igfig=0\n    gp=Gnuplot.Gnuplot(persist=1)\n    gp('set title \"%s (Figure %i)\"'%(info,igfig))\n    gp('set style data lines')\n    gp('set xlabel \"Step\"')\n    gp('set ylabel \"Variable\"')\ngp.plot( Gnuplot.Data( v, with_='lines lw 2' ) )""",
    fr_FR="Imprime sur la sortie standard et, en même temps, enregistre dans un fichier situé dans le répertoire temporaire du système et affiche graphiquement avec Gnuplot la série des valeurs de la variable (affichage persistant)",
    en_EN="Print on standard output and, in the same, time save in a file available in the system temporary directory and graphically plot with Gnuplot the value series of the variable (persistent plot)",
    order="next",
)
ObserverTemplates.store(
    name="ValueMatPlotter",
    content="""import numpy\nimport matplotlib.pyplot as plt\nv=numpy.array(var[-1], ndmin=1)\nglobal imfig, mp, ax\nplt.ion()\ntry:\n    imfig+=1\n    mp.suptitle('%s (Figure %i)'%(info,imfig))\nexcept:\n    imfig=0\n    mp = plt.figure()\n    ax = mp.add_subplot(1, 1, 1)\n    mp.suptitle('%s (Figure %i)'%(info,imfig))\nax.plot(v)\nplt.show()""",
    fr_FR="Affiche graphiquement avec Matplolib la valeur courante de la variable (affichage non persistant)",
    en_EN="Graphically plot with Matplolib the current value of the variable (non persistent plot)",
    order="next",
)
ObserverTemplates.store(
    name="ValueMatPlotterSaver",
    content="""import os.path, numpy, re, tempfile\ntempdir=tempfile.gettempdir()\nimport matplotlib.pyplot as plt\nv=numpy.array(var[-1], ndmin=1)\nglobal imfig, mp, ax\nplt.ion()\ntry:\n    imfig+=1\n    mp.suptitle('%s (Figure %i)'%(info,imfig))\nexcept:\n    imfig=0\n    mp = plt.figure()\n    ax = mp.add_subplot(1, 1, 1)\n    mp.suptitle('%s (Figure %i)'%(info,imfig))\nax.plot(v)\nf=os.path.join(tempdir,'figure_%s_%05i.pdf'%(info,imfig))\nf=re.sub(r'\\s','_',f)\nplt.savefig(f)\nplt.show()""",
    fr_FR="Affiche graphiquement avec Matplolib la valeur courante de la variable, et enregistre la figure dans un fichier situé dans le répertoire temporaire du système (affichage persistant)",
    en_EN="Graphically plot with Matplolib the current value of the variable, and save the figure in a file available in the system temporary directory (persistant plot)",
    order="next",
)
ObserverTemplates.store(
    name="ValueSerieMatPlotter",
    content="""import numpy\nimport matplotlib.pyplot as plt\nv=numpy.array(var[:], ndmin=1)\nglobal imfig, mp, ax\nplt.ion()\ntry:\n    imfig+=1\n    mp.suptitle('%s (Figure %i)'%(info,imfig))\nexcept:\n    imfig=0\n    mp = plt.figure()\n    ax = mp.add_subplot(1, 1, 1)\n    mp.suptitle('%s (Figure %i)'%(info,imfig))\n    ax.set_xlabel('Step')\n    ax.set_ylabel('Variable')\nax.plot(v)\nplt.show()""",
    fr_FR="Affiche graphiquement avec Matplolib la série des valeurs de la variable (affichage non persistant)",
    en_EN="Graphically plot with Matplolib the value series of the variable (non persistent plot)",
    order="next",
)
ObserverTemplates.store(
    name="ValueSerieMatPlotterSaver",
    content="""import os.path, numpy, re, tempfile\ntempdir=tempfile.gettempdir()\nimport matplotlib.pyplot as plt\nv=numpy.array(var[:], ndmin=1)\nglobal imfig, mp, ax\nplt.ion()\ntry:\n    imfig+=1\n    mp.suptitle('%s (Figure %i)'%(info,imfig))\nexcept:\n    imfig=0\n    mp = plt.figure()\n    ax = mp.add_subplot(1, 1, 1)\n    mp.suptitle('%s (Figure %i)'%(info,imfig))\n    ax.set_xlabel('Step')\n    ax.set_ylabel('Variable')\nax.plot(v)\nf=os.path.join(tempdir,'figure_%s_%05i.pdf'%(info,imfig))\nf=re.sub(r'\\s','_',f)\nplt.savefig(f)\nplt.show()""",
    fr_FR="Affiche graphiquement avec Matplolib la série des valeurs de la variable, et enregistre la figure dans un fichier situé dans le répertoire temporaire du système (affichage persistant)",
    en_EN="Graphically plot with Matplolib the value series of the variable, and save the figure in a file available in the system temporary directory (persistant plot)",
    order="next",
)
ObserverTemplates.store(
    name="ValuePrinterAndMatPlotter",
    content="""print(str(info)+' '+str(var[-1]))\nimport numpy\nimport matplotlib.pyplot as plt\nv=numpy.array(var[-1], ndmin=1)\nglobal imfig, mp, ax\nplt.ion()\ntry:\n    imfig+=1\n    mp.suptitle('%s (Figure %i)'%(info,imfig))\nexcept:\n    imfig=0\n    mp = plt.figure()\n    ax = mp.add_subplot(1, 1, 1)\n    mp.suptitle('%s (Figure %i)'%(info,imfig))\nax.plot(v)\nplt.show()""",
    fr_FR="Affiche graphiquement avec Matplolib la valeur courante de la variable (affichage non persistant)",
    en_EN="Graphically plot with Matplolib the current value of the variable (non persistent plot)",
    order="next",
)
ObserverTemplates.store(
    name="ValuePrinterAndMatPlotterSaver",
    content="""print(str(info)+' '+str(var[-1]))\nimport os.path, numpy, re, tempfile\ntempdir=tempfile.gettempdir()\nimport matplotlib.pyplot as plt\nv=numpy.array(var[-1], ndmin=1)\nglobal imfig, mp, ax\nplt.ion()\ntry:\n    imfig+=1\n    mp.suptitle('%s (Figure %i)'%(info,imfig))\nexcept:\n    imfig=0\n    mp = plt.figure()\n    ax = mp.add_subplot(1, 1, 1)\n    mp.suptitle('%s (Figure %i)'%(info,imfig))\nax.plot(v)\nf=os.path.join(tempdir,'figure_%s_%05i.pdf'%(info,imfig))\nf=re.sub(r'\\s','_',f)\nplt.savefig(f)\nplt.show()""",
    fr_FR="Affiche graphiquement avec Matplolib la valeur courante de la variable, et enregistre la figure dans un fichier situé dans le répertoire temporaire du système (affichage persistant)",
    en_EN="Graphically plot with Matplolib the current value of the variable, and save the figure in a file available in the system temporary directory (persistant plot)",
    order="next",
)
ObserverTemplates.store(
    name="ValueSeriePrinterAndMatPlotter",
    content="""print(str(info)+' '+str(var[:]))\nimport numpy\nimport matplotlib.pyplot as plt\nv=numpy.array(var[:], ndmin=1)\nglobal imfig, mp, ax\nplt.ion()\ntry:\n    imfig+=1\n    mp.suptitle('%s (Figure %i)'%(info,imfig))\nexcept:\n    imfig=0\n    mp = plt.figure()\n    ax = mp.add_subplot(1, 1, 1)\n    mp.suptitle('%s (Figure %i)'%(info,imfig))\n    ax.set_xlabel('Step')\n    ax.set_ylabel('Variable')\nax.plot(v)\nplt.show()""",
    fr_FR="Affiche graphiquement avec Matplolib la série des valeurs de la variable (affichage non persistant)",
    en_EN="Graphically plot with Matplolib the value series of the variable (non persistent plot)",
    order="next",
)
ObserverTemplates.store(
    name="ValueSeriePrinterAndMatPlotterSaver",
    content="""print(str(info)+' '+str(var[:]))\nimport os.path, numpy, re, tempfile\ntempdir=tempfile.gettempdir()\nimport matplotlib.pyplot as plt\nv=numpy.array(var[:], ndmin=1)\nglobal imfig, mp, ax\nplt.ion()\ntry:\n    imfig+=1\n    mp.suptitle('%s (Figure %i)'%(info,imfig))\nexcept:\n    imfig=0\n    mp = plt.figure()\n    ax = mp.add_subplot(1, 1, 1)\n    mp.suptitle('%s (Figure %i)'%(info,imfig))\n    ax.set_xlabel('Step')\n    ax.set_ylabel('Variable')\nax.plot(v)\nf=os.path.join(tempdir,'figure_%s_%05i.pdf'%(info,imfig))\nf=re.sub(r'\\s','_',f)\nplt.savefig(f)\nplt.show()""",
    fr_FR="Affiche graphiquement avec Matplolib la série des valeurs de la variable, et enregistre la figure dans un fichier situé dans le répertoire temporaire du système (affichage persistant)",
    en_EN="Graphically plot with Matplolib the value series of the variable, and save the figure in a file available in the system temporary directory (persistant plot)",
    order="next",
)
ObserverTemplates.store(
    name="ValuePrinterSaverAndMatPlotter",
    content="""print(str(info)+' '+str(var[-1]))\nimport os.path, numpy, re, tempfile\ntempdir=tempfile.gettempdir()\nimport matplotlib.pyplot as plt\nv=numpy.array(var[-1], ndmin=1)\nglobal istep\ntry:\n    istep+=1\nexcept:\n    istep=0\nf=os.path.join(tempdir,'value_%s_%05i.txt'%(info,istep))\nf=re.sub(r'\\s','_',f)\nprint('Value saved in \"%s\"'%f)\nnumpy.savetxt(f,v)\nglobal imfig, mp, ax\nplt.ion()\ntry:\n    imfig+=1\n    mp.suptitle('%s (Figure %i)'%(info,imfig))\nexcept:\n    imfig=0\n    mp = plt.figure()\n    ax = mp.add_subplot(1, 1, 1)\n    mp.suptitle('%s (Figure %i)'%(info,imfig))\nax.plot(v)\nplt.show()""",
    fr_FR="Imprime sur la sortie standard et, en même temps, enregistre dans un fichier situé dans le répertoire temporaire du système et affiche graphiquement avec Matplolib la valeur courante de la variable (affichage non persistant)",
    en_EN="Print on standard output and, in the same, time save in a file available in the system temporary directory and graphically plot with Matplolib the current value of the variable (non persistent plot)",
    order="next",
)
ObserverTemplates.store(
    name="ValuePrinterSaverAndMatPlotterSaver",
    content="""print(str(info)+' '+str(var[-1]))\nimport os.path, numpy, re, tempfile\ntempdir=tempfile.gettempdir()\nimport matplotlib.pyplot as plt\nv=numpy.array(var[-1], ndmin=1)\nglobal istep\ntry:\n    istep+=1\nexcept:\n    istep=0\nf=os.path.join(tempdir,'value_%s_%05i.txt'%(info,istep))\nf=re.sub(r'\\s','_',f)\nprint('Value saved in \"%s\"'%f)\nnumpy.savetxt(f,v)\nglobal imfig, mp, ax\nplt.ion()\ntry:\n    imfig+=1\n    mp.suptitle('%s (Figure %i)'%(info,imfig))\nexcept:\n    imfig=0\n    mp = plt.figure()\n    ax = mp.add_subplot(1, 1, 1)\n    mp.suptitle('%s (Figure %i)'%(info,imfig))\nax.plot(v)\nf=os.path.join(tempdir,'figure_%s_%05i.pdf'%(info,imfig))\nf=re.sub(r'\\s','_',f)\nplt.savefig(f)\nplt.show()""",
    fr_FR="Imprime sur la sortie standard et, en même temps, enregistre dans un fichier situé dans le répertoire temporaire du système et affiche graphiquement avec Matplolib la valeur courante de la variable (affichage non persistant et sauvegardé)",
    en_EN="Print on standard output and, in the same, time save in a file available in the system temporary directory and graphically plot with Matplolib the current value of the variable (saved and non persistent plot)",
    order="next",
)
ObserverTemplates.store(
    name="ValueSeriePrinterSaverAndMatPlotter",
    content="""print(str(info)+' '+str(var[:]))\nimport os.path, numpy, re, tempfile\ntempdir=tempfile.gettempdir()\nimport matplotlib.pyplot as plt\nv=numpy.array(var[:], ndmin=1)\nglobal istep\ntry:\n    istep+=1\nexcept:\n    istep=0\nf=os.path.join(tempdir,'value_%s_%05i.txt'%(info,istep))\nf=re.sub(r'\\s','_',f)\nprint('Value saved in \"%s\"'%f)\nnumpy.savetxt(f,v)\nglobal imfig, mp, ax\nplt.ion()\ntry:\n    imfig+=1\n    mp.suptitle('%s (Figure %i)'%(info,imfig))\nexcept:\n    imfig=0\n    mp = plt.figure()\n    ax = mp.add_subplot(1, 1, 1)\n    mp.suptitle('%s (Figure %i)'%(info,imfig))\n    ax.set_xlabel('Step')\n    ax.set_ylabel('Variable')\nax.plot(v)\nplt.show()""",
    fr_FR="Affiche graphiquement avec Matplolib la série des valeurs de la variable (affichage non persistant)",
    en_EN="Graphically plot with Matplolib the value series of the variable (non persistent plot)",
    order="next",
)
ObserverTemplates.store(
    name="ValueSeriePrinterSaverAndMatPlotterSaver",
    content="""print(str(info)+' '+str(var[:]))\nimport os.path, numpy, re, tempfile\ntempdir=tempfile.gettempdir()\nimport matplotlib.pyplot as plt\nv=numpy.array(var[:], ndmin=1)\nglobal istep\ntry:\n    istep+=1\nexcept:\n    istep=0\nf=os.path.join(tempdir,'value_%s_%05i.txt'%(info,istep))\nf=re.sub(r'\\s','_',f)\nprint('Value saved in \"%s\"'%f)\nnumpy.savetxt(f,v)\nglobal imfig, mp, ax\nplt.ion()\ntry:\n    imfig+=1\n    mp.suptitle('%s (Figure %i)'%(info,imfig))\nexcept:\n    imfig=0\n    mp = plt.figure()\n    ax = mp.add_subplot(1, 1, 1)\n    mp.suptitle('%s (Figure %i)'%(info,imfig))\n    ax.set_xlabel('Step')\n    ax.set_ylabel('Variable')\nax.plot(v)\nf=os.path.join(tempdir,'figure_%s_%05i.pdf'%(info,imfig))\nf=re.sub(r'\\s','_',f)\nplt.savefig(f)\nplt.show()""",
    fr_FR="Affiche graphiquement avec Matplolib la série des valeurs de la variable, et enregistre la figure dans un fichier situé dans le répertoire temporaire du système (affichage persistant)",
    en_EN="Graphically plot with Matplolib the value series of the variable, and save the figure in a file available in the system temporary directory (saved and persistant plot)",
    order="next",
)
ObserverTemplates.store(
    name="ValueMean",
    content="""import numpy\nprint(str(info)+' '+str(numpy.nanmean(var[-1])))""",
    fr_FR="Imprime sur la sortie standard la moyenne de la valeur courante de la variable",
    en_EN="Print on standard output the mean of the current value of the variable",
    order="next",
)
ObserverTemplates.store(
    name="ValueStandardError",
    content="""import numpy\nprint(str(info)+' '+str(numpy.nanstd(var[-1])))""",
    fr_FR="Imprime sur la sortie standard l'écart-type de la valeur courante de la variable",
    en_EN="Print on standard output the standard error of the current value of the variable",
    order="next",
)
ObserverTemplates.store(
    name="ValueVariance",
    content="""import numpy\nprint(str(info)+' '+str(numpy.nanvar(var[-1])))""",
    fr_FR="Imprime sur la sortie standard la variance de la valeur courante de la variable",
    en_EN="Print on standard output the variance of the current value of the variable",
    order="next",
)
ObserverTemplates.store(
    name="ValueL2Norm",
    content="""import numpy\nv = numpy.ravel( var[-1] )\nprint(str(info)+' '+str(float( numpy.linalg.norm(v) )))""",
    fr_FR="Imprime sur la sortie standard la norme L2 de la valeur courante de la variable",
    en_EN="Print on standard output the L2 norm of the current value of the variable",
    order="next",
)
ObserverTemplates.store(
    name="ValueRMS",
    content="""import numpy\nv = numpy.ravel( var[-1] )\nprint(str(info)+' '+str(float( numpy.sqrt((1./v.size)*numpy.dot(v,v)) )))""",
    fr_FR="Imprime sur la sortie standard la racine de la moyenne des carrés (RMS), ou moyenne quadratique, de la valeur courante de la variable",
    en_EN="Print on standard output the root mean square (RMS), or quadratic mean, of the current value of the variable",
    order="next",
)

# ==============================================================================
UserPostAnalysisTemplates = TemplateStorage()

UserPostAnalysisTemplates.store(
    name="AnalysisPrinter",
    content="""print('# Post-analysis')\nimport numpy\nxa=ADD.get('Analysis')[-1]\nprint('Analysis',xa)""",
    fr_FR="Imprime sur la sortie standard la valeur optimale",
    en_EN="Print on standard output the optimal value",
    order="next",
)
UserPostAnalysisTemplates.store(
    name="AnalysisSaver",
    content="""print('# Post-analysis')\nimport os.path, numpy, tempfile\ntempdir=tempfile.gettempdir()\nxa=ADD.get('Analysis')[-1]\nf=os.path.join(tempdir,'analysis.txt')\nprint('Analysis saved in \"%s\"'%f)\nnumpy.savetxt(f,xa)""",
    fr_FR="Enregistre la valeur optimale dans un fichier situé dans le répertoire temporaire du système nommé 'analysis.txt'",
    en_EN="Save the optimal value in a file available in the system temporary directory named 'analysis.txt'",
    order="next",
)
UserPostAnalysisTemplates.store(
    name="AnalysisPrinterAndSaver",
    content="""print('# Post-analysis')\nimport os.path, numpy, tempfile\ntempdir=tempfile.gettempdir()\nxa=ADD.get('Analysis')[-1]\nprint('Analysis',xa)\nf=os.path.join(tempdir,'analysis.txt')\nprint('Analysis saved in \"%s\"'%f)\nnumpy.savetxt(f,xa)""",
    fr_FR="Imprime sur la sortie standard et, en même temps enregistre dans un fichier situé dans le répertoire temporaire du système, la valeur optimale",
    en_EN="Print on standard output and, in the same time save in a file available in the system temporary directory, the optimal value",
    order="next",
)
UserPostAnalysisTemplates.store(
    name="AnalysisSeriePrinter",
    content="""print('# Post-analysis')\nimport numpy\nxa=ADD.get('Analysis')\nprint('Analysis',xa)""",
    fr_FR="Imprime sur la sortie standard la série des valeurs optimales",
    en_EN="Print on standard output the optimal value series",
    order="next",
)
UserPostAnalysisTemplates.store(
    name="AnalysisSerieSaver",
    content="""print('# Post-analysis')\nimport os.path, numpy, tempfile\ntempdir=tempfile.gettempdir()\nxa=ADD.get('Analysis')\nf=os.path.join(tempdir,'analysis.txt')\nprint('Analysis saved in \"%s\"'%f)\nnumpy.savetxt(f,xa)""",
    fr_FR="Enregistre la série des valeurs optimales dans un fichier situé dans le répertoire temporaire du système nommé 'analysis.txt'",
    en_EN="Save the optimal value series in a file available in the system temporary directory named 'analysis.txt'",
    order="next",
)
UserPostAnalysisTemplates.store(
    name="AnalysisSeriePrinterAndSaver",
    content="""print('# Post-analysis')\nimport os.path, numpy, tempfile\ntempdir=tempfile.gettempdir()\nxa=ADD.get('Analysis')\nprint('Analysis',xa)\nf=os.path.join(tempdir,'analysis.txt')\nprint('Analysis saved in \"%s\"'%f)\nnumpy.savetxt(f,xa)""",
    fr_FR="Imprime sur la sortie standard et, en même temps enregistre dans un fichier situé dans le répertoire temporaire du système, la série des valeurs optimales",
    en_EN="Print on standard output and, in the same time save in a file available in the system temporary directory, the optimal value series",
    order="next",
)

# ==============================================================================
if __name__ == "__main__":
    print("\n AUTODIAGNOSTIC\n")
