..
   Copyright (C) 2008-2024 EDF R&D

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

.. _section_gui_in_salome:

================================================================================
**[DocR]** Interface graphique pour l'utilisateur (GUI/EFICAS)
================================================================================

.. |eficas_new| image:: images/eficas_new.png
   :align: middle
   :scale: 50%
.. |eficas_save| image:: images/eficas_save.png
   :align: middle
   :scale: 50%
.. |eficas_saveas| image:: images/eficas_saveas.png
   :align: middle
   :scale: 50%
.. |eficas_yacs| image:: images/eficas_yacs.png
   :align: middle
   :scale: 50%
.. |yacs_compile| image:: images/yacs_compile.png
   :align: middle
   :scale: 50%

Cette section présente l'usage du module ADAO dans la plateforme SALOME. On
décrit ici le cheminement général pour établir un cas ADAO, les détails étant
fournis dans les chapitres suivants. Il est complété par la description
détaillée de l'ensemble des commandes et mots-clés dans la section
:ref:`section_reference`, par des procédures avancées d'usage dans la section
:ref:`section_advanced`, et par des exemples dans la section
:ref:`section_tutorials_in_salome`.

Procédure logique pour construire un cas ADAO
---------------------------------------------

La construction d'un cas ADAO suit une démarche simple pour définir l'ensemble
des données d'entrée, et ensuite générer un diagramme complet d'exécution
utilisé dans YACS [#]_. De nombreuses variations existent pour la définition
des données d'entrée, mais la séquence logique reste inchangée.

De manière générale, l'utilisateur doit connaître ses données d'entrées,
requises pour mettre au point une étude d'assimilation de données, en suivant la
:ref:`section_methodology`. Ces données peuvent déjà être disponibles dans
SALOME ou non.

Fondamentalement, la procédure d'utilisation de ADAO comprend les étapes
suivantes:

- :ref:`section_u_step1`
- :ref:`section_u_step2`
- :ref:`section_u_step3`
- :ref:`section_u_step4`
- :ref:`section_u_step5`

Chaque étape est détaillée dans la section suivante.

Procédure détaillée pour construire un cas ADAO
-----------------------------------------------

.. _section_u_step1:

ÉTAPE 1 : Activer le module ADAO et utiliser l'interface graphique d'édition (GUI)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Comme toujours pour un module, il doit être préalablement activé en
sélectionnant le bouton de module approprié (ou le menu) dans la barre d'outils
de SALOME. S'il n'existe aucune étude SALOME chargée, un menu contextuel
apparaît, permettant de choisir entre la création d'une nouvelle étude, ou
l'ouverture d'une étude déjà existante:

  .. _adao_activate1:
  .. image:: images/adao_activate.png
    :align: center
  .. centered::
    **Activation du module ADAO dans SALOME**

En choisissant le bouton "*Nouveau*", un éditeur intégré de cas [#]_ sera
ouvert, en même temps que le "*navigateur d'objets*" standard. On peut alors
cliquer sur le bouton "*Nouveau*" (ou choisir l'entrée "*Nouveau*"  dans le
menu principal "*ADAO*") pour créer un nouveau cas ADAO, et on obtient :

  .. _adao_viewer:
  .. image:: images/adao_viewer.png
    :align: center
    :width: 100%
  .. centered::
    **L'éditeur intégré pour la définition des cas dans le module ADAO**

.. _section_u_step2:

ÉTAPE 2 : Créer et modifier le cas ADAO, et l'enregistrer
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Pour construire un cas en utilisant l'éditeur intégré, on doit passer par une
série de sous-étapes, en choisissant, à chaque sous-étape, un mot-clé puis en
remplissant ses valeurs. On note que c'est dans cette étape qu'il faut, entre
autres, définir un **appel au code de simulation** utilisé dans les opérateurs
d'observation ou d'évolution décrivant le problème [#]_.

L'éditeur structuré indique des types hiérarchiques, des valeurs ou des
mots-clés autorisés. Les mots-clés incomplets ou incorrects sont identifiés par
un indicateur d'erreur visuel rouge. Les valeurs possibles sont indiquées pour
les mots-clés par la définition d'une liste limitée de valeurs, et les entrées
adaptées sont données pour les autres mots-clés. Des messages d'aide sont
fournis de manière contextuelle aux places réservées de l'éditeur.

Un nouveau cas est mis en place avec la liste minimale des commandes. Toutes les
commandes ou les mots-clés obligatoires sont déjà présents, aucun d'eux ne peut
être supprimé. Des mots-clés optionnels peuvent être ajoutés en les choisissant
dans une liste de suggestions de ceux autorisés pour la commande principale, par
exemple la commande "*ASSIMILATION_STUDY*". À titre d'exemple, on peut ajouter
des paramètres dans le mot-clé "*AlgorithmParameters*", comme décrit dans la
dernière partie de la section :ref:`section_tutorials_in_salome`.

A la fin de ces actions, lorsque tous les champs ou les mots-clés ont été
correctement définis, chaque ligne de l'arborescence des commandes doit
présenter un drapeau vert. Cela signifie que l'ensemble du cas est valide et
dûment rempli (et qu'il peut être sauvegardé).

  .. _adao_jdcexample00:
  .. image:: images/adao_jdcexample01.png
    :align: center
    :scale: 75%
  .. centered::
    **Exemple d'un cas ADAO valide**

Au final, il faut enregistrer le cas ADAO en utilisant le bouton "*Enregistrer*"
|eficas_save|, ou le bouton "*Enregistrer sous*" |eficas_saveas|, ou en
choisissant l'entrée "*Enregistrer/ Enregistrer sous*" dans le menu "*ADAO*". Il
est alors demandé un emplacement, à choisir dans l'arborescence des fichiers, et
un nom, qui sera complété par l'extension "*.comm*" utilisée pour les fichiers
de l'éditeur intégré de cas. Cette action va générer une paire de fichiers
décrivant le cas ADAO, avec le même nom de base, le premier présentant une
extension "*.comm*" et le second une extension "*.py*" [#]_.

.. _section_u_step3:

ÉTAPE 3 : Exporter le cas ADAO comme un schéma YACS
+++++++++++++++++++++++++++++++++++++++++++++++++++

Lorsque le cas ADAO est complété, il doit être converti ou exporté sous la forme
d'un schéma YACS pour pouvoir exécuter le calcul d'assimilation de données. Cela
peut être réalisé facilement en utilisant le bouton "*Exporter vers YACS*"
|eficas_yacs|, ou de manière équivalente en choisissant l'entrée "*Exporter vers
YACS*" dans le menu principal "*ADAO*", ou dans le menu contextuel du cas dans
le navigateur d'objets SALOME.

  .. _adao_exporttoyacs01:
  .. image:: images/adao_exporttoyacs.png
    :align: center
    :scale: 75%
  .. centered::
    **Sous-menu "Exporter vers YACS" pour générer le schéma YACS à partir d'un cas ADAO**

Cela conduit à générer automatiquement un schéma YACS, et à activer le module
YACS sur ce schéma. Le fichier YACS, associé au schéma, est stocké dans le même
répertoire et avec le même nom de base de fichier que le cas ADAO enregistré,
changeant simplement son extension en "*.xml*". Attention, *si le nom de fichier
XML existe déjà, le fichier est écrasé sans avertissement sur le remplacement du
fichier XML*.

.. _section_u_step4:

ÉTAPE 4 : Compléter et modifier le schéma YACS, et l'enregistrer
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: Analysis

Lorsque le schéma YACS est généré et ouvert dans SALOME à travers l'interface
graphique du module YACS, on peut modifier ou compléter le schéma comme tout
schéma YACS standard. Des noeuds ou des blocs peuvent être ajoutés, copiés ou
modifiés pour élaborer une analyse complexe, ou pour insérer des capacités
d'assimilation de données ou d'optimisation dans des schémas de calculs YACS
plus complexes.

Le principal complément nécessaire dans un schéma YACS est une étape de
post-processing. L'évaluation du résultat doit être réalisée dans le contexte
physique de simulation utilisé par la procédure d'assimilation de données. Le
post-processing peut être fourni à travers le mot-clé "*UserPostAnalysis*"
d'ADAO sous la forme d'un fichier de script ou d'une chaîne de caractères, par
des patrons ("templates"), ou peut être construit comme des noeuds YACS. Ces
deux manières de construire le post-processing peuvent utiliser toutes les
capacités de SALOME. On se reportera à la partie traitant des
:ref:`section_ref_output_variables`, ou à l'aide de chaque algorithme, pour la
description complète de ces éléments.

En pratique, le schéma YACS dispose d'un port de sortie "*algoResults*" dans le
bloc de calcul, qui donne accès à un objet structuré nommé ci-après "*ADD*" par
exemple, qui contient tous les résultats de calcul. Ces résultats peuvent être
obtenus en récupérant les variables nommées stockées au cours des calculs.
L'information principale est la variable "*Analysis*", qui peut être obtenue par
une commande python (par exemple dans un noeud script intégré ("in-line script
node") ou un script fourni à travers le mot-clé "*UserPostAnalysis*"::

    Analysis = ADD.get("Analysis")[:]

"*Analysis*" est un objet complexe, similaire à une liste de valeurs calculées à
chaque étape du calcul d'assimilation. Pour obtenir et afficher l'évaluation
optimale de l'état par assimilation de données, dans un script fourni par
l'intermédiaire du mot-clé "*UserPostAnalysis*", on peut utiliser::

    Xa = ADD.get("Analysis")[-1]
    print("Optimal state:", Xa)
    print()

Cette variable ``Xa`` est un vecteur de valeurs, qui représente la solution du
problème d'évaluation par assimilation de données ou par optimisation, notée
:math:`\mathbf{x}^a` dans la section :ref:`section_theory`.

Une telle méthode peut être utilisée pour imprimer les résultats, ou pour les
convertir dans des structures qui peuvent être nécessaires à un post-processing
natif ou externe à SALOME. Un exemple simple est disponible dans la section
:ref:`section_tutorials_in_salome`.

.. _section_u_step5:

ÉTAPE 5 : Exécuter le schéma YACS et obtenir les résultats
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Le schéma YACS est maintenant complet et peut être exécuté. La paramétrisation
et l'exécution de ce cas YACS est entièrement compatible avec la manière
standard de traiter un schéma YACS, comme décrit dans le *Guide de l'utilisateur
du module YACS*.

Pour rappeler la manière la plus simple de procéder, le schéma YACS doit être
compilé en utilisant le bouton |yacs_compile|, ou l'entrée équivalente du menu
YACS, pour préparer le schéma à son exécution. Ensuite, le schéma compilé peut
être démarré, exécuté pas à pas ou en utilisant des points d'arrêt, etc.

La sortie standard est restituée dans la "*fenêtre de sortie de YACS*" (ou
"*YACS Container Log*"), à laquelle on accède par un clic droit sur la fenêtre
"*proc*" dans l'interface graphique YACS. Les erreurs sont présentées soit
dans la "*fenêtre de sortie de YACS*", ou à la ligne de commande dans la fenêtre
de commandes (si l'environnement SALOME a été lancé par une commande explicite,
et non par un menu ou une icône de bureau). Par exemple, la sortie de l'exemple
simple ci-dessus est de la forme suivante::

   Entering in the assimilation study
   Name is set to........: Test
   Algorithm is set to...: Blue
   Launching the analysis

   Optimal state: [0.5, 0.5, 0.5]

présentée dans la "*fenêtre de sortie de YACS*".

L'exécution peut aussi être conduite en utilisant un script de commandes Shell,
comme décrit dans la section :ref:`section_advanced`.

.. [#] Pour de plus amples informations sur YACS, voir le *module YACS* et son aide intégrée disponible dans le menu principal *Aide* de l'environnement SALOME.

.. [#] Pour de plus amples informations sur l'éditeur intégré de cas, voir le *module EFICAS* et son aide intégrée disponible dans le menu principal *Aide* de l'environnement SALOME.

.. [#] L'utilisation du code de simulation physique dans les opérateurs de base de l'assimilation de données est illustrée ou décrite dans les parties principales qui suivent.

.. [#] Ce fichier python intermédiaire peut aussi être utilisé comme décrit dans la section :ref:`section_advanced`.
