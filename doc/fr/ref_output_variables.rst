..
   Copyright (C) 2008-2019 EDF R&D

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

.. _section_ref_output_variables:

Variables et informations disponibles en sortie
-----------------------------------------------

Comment obtenir les informations disponibles en sortie
++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: UserPostAnalysis
.. index:: single: algoResults
.. index:: single: getResults
.. index:: single: get
.. index:: single: ADD

En sortie, après exécution d'une assimilation de données, d'une optimisation
ou d'une vérification, on dispose de variables et d'informations issues du
calcul. L'obtention de ces informations se fait ensuite de manière standardisée
à l'aide de l'étape de post-processing du calcul.

L'étape est aisément identifiée par l'utilisateur dans son cas ADAO de
définition (par le mot-clé "*UserPostAnalysis*") ou dans son schéma YACS
d'exécution (par des noeuds ou blocs situés après le bloc de calcul, et reliés
graphiquement au port de sortie "*algoResults*" du bloc de calcul):

#. Dans le cas où l'utilisateur définit le post-processing dans son cas ADAO, il utilise un fichier script externe ou des commandes dans le champ de type "*String*" ou "*Template*". Le script qu'il fournit dispose d'une variable fixe "*ADD*" dans l'espace de noms.
#. Dans le cas où l'utilisateur définit le post-processing dans son schéma YACS par un noeud Python situé après le bloc de calcul, il doit ajouter un port d'entrée de type "*pyobj*" nommé par exemple "*Study*", relié graphiquement au port de sortie "*algoResults*" du bloc de calcul. Le noeud Python de post-processing doit ensuite débuter par ``ADD = Study.getResults()``.

Des patrons (ou "templates") sont donnés ci-après en
:ref:`subsection_r_o_v_Template`.  Dans tous les cas, le post-processing de
l'utilisateur dispose dans l'espace de noms d'une variable dont le nom est
"*ADD*", et dont l'unique méthode utilisable est nommée ``get``. Les arguments
de cette méthode sont un nom d'information de sortie, comme décrit dans
l':ref:`subsection_r_o_v_Inventaire`.

Par exemple, pour avoir l'état optimal après un calcul d'assimilation de données
ou d'optimisation, on utilise l'appel suivant::

    ADD.get("Analysis")

Cet appel renvoie une liste de valeurs de la notion demandée (ou, dans le cas
de variables d'entrées qui ne sont par nature qu'en un unique exemplaire, la
valeur elle-même). On peut alors demander un élément particulier de la liste par
les commandes standards de liste (en particulier ``[-1]`` pour le dernier, et
``[:]`` pour tous les éléments).

.. _subsection_r_o_v_Template:

Exemples de scripts Python pour obtenir ou traiter les sorties
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: Template
.. index:: single: AnalysisPrinter
.. index:: single: AnalysisSaver
.. index:: single: AnalysisPrinterAndSaver

Ces exemples présentent des commandes ou scripts Python qui permettent d'obtenir
ou de traiter les sorties d'une exécution d'algorithme. Pour aider
l'utilisateur, ils sont directement disponibles dans l'interface, à la
construction du cas ADAO dans l'éditeur intégré de cas, dans les champs de type
"*Template*". De manière équivalente, ces commandes peuvent être contenues dans
un script utilisateur externe (et insérées dans le cas ADAO par l'entrée de type
"*Script*") ou contenues dans une chaîne de caractères, y compris les retour à
la ligne (et insérées dans le cas ADAO par l'entrée de type "*String*"). De
nombreuses variantes peuvent être imaginées à partir de ces exemples simples,
l'objectif étant surtout d'aider l'utilisateur à effectuer le traitement exact
dont il a besoin en sortie.

Le premier exemple (appelé "*AnalysisPrinter*" dans les entrées de type
"*Template*") consiste à afficher, dans la sortie standard d'exécution, la
valeur de l'analyse ou de l'état optimal, noté :math:`\mathbf{x}^a` dans la
partie :ref:`section_theory`. Cela se réalise par les commandes::

    import numpy
    xa=numpy.ravel(ADD.get('Analysis')[-1])
    print('Analysis:',xa)

La fonction ``numpy.ravel`` assure simplement que la variable ``xa`` contienne
un vrai vecteur unidimensionnel, quels que soient les choix informatiques
précédents.

Un second exemple (appelé "*AnalysisSaver*" dans les entrées de type
"*Template*") consiste à enregistrer sur fichier la valeur de l'analyse ou de
l'état optimal :math:`\mathbf{x}^a`. Cela se réalise par les commandes::

    import numpy
    xa=numpy.ravel(ADD.get('Analysis')[-1])
    f='/tmp/analysis.txt'
    print('Analysis saved in "%s"'%f)
    numpy.savetxt(f,xa)"

Le fichier d'enregistrement choisi est un fichier texte ``/tmp/analysis.txt``.

Il est aisé de combiner ces deux exemples pour en construire un troisième
(appelé "*AnalysisPrinterAndSaver*" dans les entrées de type "*Template*"). Il
consiste à simultanément afficher dans la sortie standard d'exécution et à
enregistrer sur fichier la valeur de :math:`\mathbf{x}^a`. Cela se réalise par
les commandes::

    import numpy
    xa=numpy.ravel(ADD.get('Analysis')[-1])
    print('Analysis:',xa)
    f='/tmp/analysis.txt'
    print('Analysis saved in "%s"'%f)
    numpy.savetxt(f,xa)

Pour faciliter l'extension de ces exemples selon les besoins utilisateurs, on
rappelle que l'ensemble des fonctions de SALOME sont disponibles au même niveau
que ces commandes. L'utilisateur peut en particulier requérir des actions de
représentation graphique avec le module PARAVIS [#]_ ou d'autres modules, des
actions de calcul pilotés par YACS [#]_ ou un autre module, etc.

D'autres exemples d'utilisation sont aussi donnés en :ref:`section_u_step4` de
la partie :ref:`section_gui_in_salome`, ou en partie :ref:`section_tutorials_in_salome`.

Conditionnalité des informations disponibles en sortie
++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: AlgorithmParameters
.. index:: single: Stored

La disponibilité des informations après le calcul est conditionnée par le fait
qu'elles aient été calculées ou demandées.

Chaque algorithme ne fournit pas obligatoirement les mêmes informations, et
n'utilise par exemple pas nécessairement les mêmes quantités intermédiaires. Il
y a donc des informations toujours présentes comme l'état optimal résultant du
calcul. Les autres informations ne sont présentes que pour certains algorithmes
et/ou que si elles ont été réclamées avant l'exécution du calcul.

On rappelle que l'utilisateur peut réclamer des informations supplémentaires
lors de l'établissement de son cas ADAO, en utilisant la commande optionnelle
"*AlgorithmParameters*" du cas ADAO. On se reportera à la
:ref:`section_ref_options_Algorithm_Parameters` pour le bon usage de cette
commande, et à la description de chaque algorithme pour les informations
disponibles par algorithme. On peut aussi demander à conserver certaines
informations en entrée en changeant le booléen "*Stored*" qui lui est associé
dans l'édition du cas ADAO.

.. _subsection_r_o_v_Inventaire:

Inventaire des informations potentiellement disponibles en sortie
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Les principales informations potentiellement disponibles en sortie sont
indiquées ici indépendamment des algorithmes, pour inventaire. On se reportera
directement aux détails des algorithmes pour avoir l'inventaire exhaustif.

L'état optimal est une information qui est toujours naturellement disponible
après un calcul d'assimilation de données ou d'optimisation. Il désigné par le
mot-clé suivant:

  .. include:: snippets/Analysis.rst

Les variables suivantes sont des variables d'entrée que l'on peut aussi obtenir
en sortie. Elles sont mises à disposition de l'utilisateur en sortie pour
faciliter l'écriture des procédures de post-processing, et sont conditionnées
par une demande utilisateur explicite à l'aide d'un booléen "*Stored*" en
entrée. Toutes ces variables d'entrée restituées sont obtenables par la
commande standard ".get(...)", qui s'applique à refournir l'unique objet donné
en entrée.

  .. include:: snippets/Background.rst

  .. include:: snippets/BackgroundError.rst

  .. include:: snippets/EvolutionError.rst

  .. include:: snippets/Observation.rst

  .. include:: snippets/ObservationError.rst

Toutes les autres informations sont conditionnées par l'algorithme et/ou par la
demande utilisateur de disponibilité. Les principales sont les suivantes, par
ordre alphabétique:

  .. include:: snippets/APosterioriCorrelations.rst

  .. include:: snippets/APosterioriCovariance.rst

  .. include:: snippets/APosterioriStandardDeviations.rst

  .. include:: snippets/APosterioriVariances.rst

  .. include:: snippets/BMA.rst

  .. include:: snippets/CostFunctionJ.rst

  .. include:: snippets/CostFunctionJb.rst

  .. include:: snippets/CostFunctionJo.rst

  .. include:: snippets/CostFunctionJAtCurrentOptimum.rst

  .. include:: snippets/CostFunctionJbAtCurrentOptimum.rst

  .. include:: snippets/CostFunctionJoAtCurrentOptimum.rst

  .. include:: snippets/CurrentOptimum.rst

  .. include:: snippets/CurrentState.rst

  .. include:: snippets/IndexOfOptimum.rst

  .. include:: snippets/Innovation.rst

  .. include:: snippets/InnovationAtCurrentState.rst

  .. include:: snippets/OMA.rst

  .. include:: snippets/OMB.rst

  .. include:: snippets/Residu.rst

  .. include:: snippets/SimulatedObservationAtBackground.rst

  .. include:: snippets/SimulatedObservationAtCurrentOptimum.rst

  .. include:: snippets/SimulatedObservationAtCurrentState.rst

  .. include:: snippets/SimulatedObservationAtOptimum.rst

  .. include:: snippets/SimulationQuantiles.rst

.. [#] Pour de plus amples informations sur PARAVIS, voir le *module PARAVIS* et son aide intégrée disponible dans le menu principal *Aide* de l'environnement SALOME.

.. [#] Pour de plus amples informations sur YACS, voir le *module YACS* et son aide intégrée disponible dans le menu principal *Aide* de l'environnement SALOME.
