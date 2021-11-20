..
   Copyright (C) 2008-2021 EDF R&D

   This file is part of SALOME ADAO module.

   This library is free software; you can redistribute it and/or
   modify it under the terms of the GNU Lesser General Public
   License as published by the Free Software Foundation; either
   version 2.1 of the License, or (at your option) any later version.

   This library is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   Lesser General Public License for more details.

   You should have received a copy of the GNU Lesser General Public
   License along with this library; if not, write to the Free Software
   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA

   See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com

   Author: Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D

.. _section_ref_userpostanalysis_requirements:

Exigences pour décrire un post-traitement dédié après calcul ADAO
-----------------------------------------------------------------

.. index:: single: Post-Traitement
.. index:: single: UserPostAnalysis
.. index:: single: setUserPostAnalysis
.. index:: single: UserPostAnalysis Template

Des traitements de résultats sont usuellement nécessaires après un calcul ADAO,
pour l'insérer dans une étude complète. Après exécution d'un cas de calcul,
l'information principale est la variable "*Analysis*" qui contient un résultat
d'estimation optimale. On dispose en plus aussi de toutes les variables de
calcul qui ont été demandées en stockage intermédiaire à l'aide de la variable
spéciale d'algorithme "*StoreSupplementaryCalculations*".

Les traitements les plus simples se représentent souvent par quelques lignes de
Python, qu'il est aisé de reprendre ou reporter entre deux études. Mais les
traitements plus complexes de résultats, dans l'environnement d'étude complet
SALOME, sont souvent effectués par des parties explicites de post-traitements
complémentaires, que ce soit dans des noeuds YACS ou par des commandes Python
en TUI, ou d'autres méthodes. Il est donc souvent intéressant d'identifier une
partie au moins des calculs à la suite de l'estimation ADAO, et de les associer
dans le cas de calcul.

ADAO donne ainsi la possibilité de définir un post-traitement général pour
chaque cas de calcul. Cette définition se fait en indiquant les commandes à
réaliser en sortie de calcul ADAO.

Enregistrer un post-traitement dédié
++++++++++++++++++++++++++++++++++++

Dans l'interface graphique EFICAS d'ADAO, il y a 3 méthodes pratiques pour
intégrer un post-traitement dédié à un cas ADAO. La méthode est choisie à
l'aide du mot-clé "*FROM*" de l'entrée principale "*UserPostAnalysis*", comme
montré dans la figure qui suit :

  .. eficas_userpostanalysis_nodetype:
  .. image:: images/eficas_userpostanalysis_nodetype.png
    :align: center
    :width: 100%
  .. centered::
    **Choisir son type d'entrée pour le post-traitement enregistré**

Le post-traitement peut être fourni sous la forme d'un script explicite (entrée
de type "*String*"), d'un script contenu dans un fichier externe (entrée de
type "*Script*"), ou en utilisant un modèle (entrée de type "*Template*"). Les
modèles sont fournis par défaut dans ADAO lors de l'usage de l'éditeur
graphique EFICAS pour ADAO ou de l'interface TUI, et sont détaillés dans la
partie :ref:`section_ref_userpostanalysis_templates` qui suit. Ces derniers
sont des scripts simples qui peuvent être adaptés par l'utilisateur, soit dans
l'étape d'édition intégrée du cas avec EFICAS d'ADAO, soit dans l'étape
d'édition du schéma avant l'exécution, pour améliorer la performance du calcul
ADAO dans le superviseur d'exécution de SALOME.

Dans l'interface textuelle TUI d'ADAO (voir la partie :ref:`section_tui`), les
mêmes informations peuvent être données à l'aide de la commande
"*setUserPostAnalysis*". Les arguments de cette commande permettent de définir
le traitement soit comme un modèle (argument "*Template*") désignant l'un des
scripts détaillés dans la partie :ref:`section_ref_userpostanalysis_templates`,
soit comme un script explicite (argument "*String*"), soit comme un script
contenu dans un fichier externe (argument "*Script*").

Forme générale d'un script permettant de définir un post-traitement dédié
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Une série de commandes de post-traitement est un script Python spécial, qui est
automatiquement activée à la fin des calculs d'estimation dans ADAO. Toutes les
commandes Python, qu'un utilisateur peut ajouter après un calcul ADAO en
interface graphique GUI, peuvent faire partie de ce post-traitement. Plusieurs
modèles de série de commandes sont disponibles par défaut, essentiellement pour
donner un exemple le plus simple possible d'enregistrement de ces séries.

Pour être utilisable de manière automatique, il est requis tout appel du cas de
calcul ADAO, pour récupérer une variable, se fasse uniquement avec le nom
réservé "*ADD*". A titre d'exemple, voici un script très simple (très similaire
au modèle "*ValuePrinter*"), utilisable pour afficher la valeur de l'estimation
optimale :
::

    import numpy
    xa = numpy.ravel(ADD.get('Analysis')[-1])
    print('  === Analysis =',xa)

Si la commande "*ADD.get(...)*", utilisée pour l'obtention d'une variable
résultat, n'utilise pas le nom réservé "*ADD*" pour le cas de calcul, alors
l'appel conduira à une erreur d'exécution et préviendra de l'absence du nom du
cas.

Pour illustration, la déclaration d'un modèle, en interface TUI, se fait en
utilisant la commande :
::

    ADD.setUserPostAnalysis(Template = "AnalysisPrinter")

.. warning::

    Si les modèles disponibles par défaut ne sont pas utilisés, il revient à
    l'utilisateur de faire des scripts soigneusement établis et vérifiés, ou
    des programmes externes qui ne se plantent pas, avant d'être enregistrés
    comme un post-traitement. Le débogage peut sinon être vraiment difficile !

On donne ci-après l'identifiant et le contenu de tous les modèles simples
disponibles.

.. _section_ref_userpostanalysis_templates:

Inventaire des modèles simples de post-traitement disponibles ("*Template*")
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: AnalysisPrinter (Observer)

Modèle **AnalysisPrinter**
..........................

Imprime sur la sortie standard la valeur optimale.

::

    print('# Post-analysis')
    import numpy
    xa=ADD.get('Analysis')[-1]
    print('Analysis',xa)

.. index:: single: AnalysisSaver (Observer)

Modèle **AnalysisSaver**
........................

Enregistre la valeur optimale dans un fichier du répertoire '/tmp' nommé 'analysis.txt'.

::

    print('# Post-analysis')
    import numpy
    xa=ADD.get('Analysis')[-1]
    f='/tmp/analysis.txt'
    print('Analysis saved in "%s"'%f)
    numpy.savetxt(f,xa)

.. index:: single: AnalysisPrinterAndSaver (Observer)

Modèle **AnalysisPrinterAndSaver**
..................................

Imprime sur la sortie standard et, en même temps enregistre dans un fichier du répertoire '/tmp', la valeur optimale.

::

    print('# Post-analysis')
    import numpy
    xa=ADD.get('Analysis')[-1]
    print('Analysis',xa)
    f='/tmp/analysis.txt'
    print('Analysis saved in "%s"'%f)
    numpy.savetxt(f,xa)

.. index:: single: AnalysisSeriePrinter (Observer)

Modèle **AnalysisSeriePrinter**
...............................

Imprime sur la sortie standard la série des valeurs optimales.

::

    print('# Post-analysis')
    import numpy
    xa=ADD.get('Analysis')
    print('Analysis',xa)

.. index:: single: AnalysisSerieSaver (Observer)

Modèle **AnalysisSerieSaver**
.............................

Enregistre la série des valeurs optimales dans un fichier du répertoire '/tmp' nommé 'analysis.txt'.

::

    print('# Post-analysis')
    import numpy
    xa=ADD.get('Analysis')
    f='/tmp/analysis.txt'
    print('Analysis saved in "%s"'%f)
    numpy.savetxt(f,xa)

.. index:: single: AnalysisSeriePrinterAndSaver (Observer)

Modèle **AnalysisSeriePrinterAndSaver**
.......................................

Imprime sur la sortie standard et, en même temps enregistre dans un fichier du répertoire '/tmp', la série des valeurs optimales.

::

    print('# Post-analysis')
    import numpy
    xa=ADD.get('Analysis')
    print('Analysis',xa)
    f='/tmp/analysis.txt'
    print('Analysis saved in "%s"'%f)
    numpy.savetxt(f,xa)
