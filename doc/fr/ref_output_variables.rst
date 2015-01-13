..
   Copyright (C) 2008-2015 EDF R&D

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

Comment obtenir des informations disponibles en sortie
++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: UserPostAnalysis
.. index:: single: algoResults
.. index:: single: get

En sortie, après exécution d'une assimilation de données, d'une optimisation
ou d'une vérification, on dispose de variables et d'informations issues du
calcul. L'obtention de ces informations se fait ensuite de manière standardisée
à l'aide de l'étape de post-processing du calcul. 

L'étape est aisément identifiée par l'utilisateur dans son cas ADAO de
définition (par la mot-clé "*UserPostAnalysis*") ou dans son schéma YACS
d'exécution (par des noeuds ou blocs situés après le bloc de calcul, et reliés
graphiquement au port de sortie "*algoResults*" du bloc de calcul):

#. Dans le cas où l'utilisateur définit le post-processing dans son cas ADAO, il utilise un fichier script externe ou des commandes dans le champ de type "*String*" ou "*Template*". Le script qu'il fournit dispose d'une variable fixe "*ADD*" dans l'espace de noms.
#. Dans le cas où l'utilisateur définit le post-processing dans son schéma YACS par un noeud Python situé après le bloc de calcul, il doit ajouter un port d'entrée de type "*pyobj*" nommé par exemple "*Study*", relié graphiquement au port de sortie "*algoResults*" du bloc de calcul. Le noeud Python de post-processing doit ensuite débuter par ``ADD = Study.getResults()``.

Dans tous les cas, le post-processing de l'utilisateur dispose dans l'espace de
noms d'une variable dont le nom est "*ADD*", et dont l'unique méthode utilisable
est nommée ``get``. Les arguments de cette méthode sont un nom d'information de
sortie, comme décrit dans l':ref:`subsection_r_o_v_Inventaire`.

Par exemple, pour avoir l'état optimal après un calcul d'assimilation de données
ou d'optimisation, on utilise l'appel suivant::

    ADD.get("Analysis")

Cet appel renvoie une liste de valeurs de la notion demandée (ou, dans le cas 
de variables d'entrées qui ne sont par nature qu'en un unique exemplaire, la
valeur elle-même). On peut alors demander un élément particulier de la liste par
les commandes standards de liste (en particulier ``[-1]`` pour le dernier, et
``[:]`` pour tous les éléments).

Conditionnalité des informations disponibles en sortie
++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: StoreInternalVariables
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
lors de l'établissement de son cas ADAO, en utilisant l'option
"*StoreInternalVariables*" de chaque algorithme à travers la commande
optionnelle "*AlgorithmParameters*" du cas ADAO. On se reportera à la
:ref:`section_ref_options_AlgorithmParameters` pour le bon usage de cette
commande, et à la description de chaque algorithme pour les informations
disponibles par algorithme. On peut aussi demander à conserver certaines
informations en entrée en changeant le booléen "*Stored*" qui lui est associé
dans l'édition du cas ADAO. 

.. _subsection_r_o_v_Inventaire:

Inventaire des informations potentiellement disponibles en sortie
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

L'ensemble des informations potentiellement disponibles en sortie est indiqué
ici indépendamment des algorithmes, pour inventaire.

L'état optimal est une information qui est toujours naturellement disponible
après un calcul d'assimilation de données ou d'optimisation. Il désigné par le
mot-clé suivant:

  Analysis
    *Liste de vecteurs*. Chaque élément est un état optimal :math:`\mathbf{x}*`
    en optimisation ou une analyse :math:`\mathbf{x}^a` en assimilation de
    données.

    Exemple : ``Xa = ADD.get("Analysis")[-1]``

Les variables suivantes sont des variables d'entrée. Elles sont mises à
disposition de l'utilisateur en sortie pour faciliter l'écriture des procédures
de post-processing, et sont conditionnées par une demande utilisateur à l'aide
d'un booléen "*Stored*" en entrée.

  Background
    *Vecteur*, dont la disponibilité est conditionnée par "*Stored*" en entrée.
    C'est le vecteur d'ébauche :math:`\mathbf{x}^b`.

    Exemple : ``Xb = ADD.get("Background")``

  BackgroundError
    *Matrice*, dont la disponibilité est conditionnée par "*Stored*" en entrée. 
    C'est la matrice :math:`\mathbf{B}` de covariances des erreurs *a priori*
    de l'ébauche.

    Exemple : ``B = ADD.get("BackgroundError")``

  EvolutionError
    *Matrice*, dont la disponibilité est conditionnée par "*Stored*" en entrée. 
    C'est la matrice :math:`\mathbf{M}` de covariances des erreurs *a priori*
    de l'évolution.

    Exemple : ``M = ADD.get("EvolutionError")``

  Observation
    *Vecteur*, dont la disponibilité est conditionnée par "*Stored*" en entrée. 
    C'est le vecteur d'observation :math:`\mathbf{y}^o`.

    Exemple : ``Yo = ADD.get("Observation")``

  ObservationError
    *Matrice*, dont la disponibilité est conditionnée par "*Stored*" en entrée. 
    C'est la matrice :math:`\mathbf{R}` de covariances des erreurs *a priori*
    de l'observation.

    Exemple : ``R = ADD.get("ObservationError")``

Toutes les autres informations sont conditionnées par l'algorithme et/ou par la
demande utilisateur de disponibilité. Ce sont les suivantes, par ordre
alphabétique:

  APosterioriCovariance
    *Liste de matrices*. Chaque élément est une matrice :math:`\mathbf{A}*` de
    covariances des erreurs *a posteriori* de l'état optimal.

    Exemple : ``A = ADD.get("APosterioriCovariance")[-1]``

  BMA
    *Liste de vecteurs*. Chaque élément est un vecteur d'écart entre
    l'ébauche et l'état optimal.

    Exemple : ``bma = ADD.get("BMA")[-1]``

  CostFunctionJ
    *Liste de valeurs*. Chaque élément est une valeur de fonctionnelle d'écart
    :math:`J`.

    Exemple : ``J = ADD.get("CostFunctionJ")[:]``

  CostFunctionJb
    *Liste de valeurs*. Chaque élément est une valeur de fonctionnelle d'écart
    :math:`J^b`, c'est-à-dire de la partie écart à l'ébauche.

    Exemple : ``Jb = ADD.get("CostFunctionJb")[:]``

  CostFunctionJo
    *Liste de valeurs*. Chaque élément est une valeur de fonctionnelle d'écart
    :math:`J^o`, c'est-à-dire de la partie écart à l'observation.

    Exemple : ``Jo = ADD.get("CostFunctionJo")[:]``

  CurrentState
    *Liste de vecteurs*. Chaque élément est un vecteur d'état courant utilisé
    au cours du déroulement de l'algorithme d'optimisation.

    Exemple : ``Xs = ADD.get("CurrentState")[:]``

  Innovation
    *Liste de vecteurs*. Chaque élément est un vecteur d'innovation, qui est
    en statique l'écart de l'optimum à l'ébauche, et en dynamique l'incrément
    d'évolution.

    Exemple : ``d = ADD.get("Innovation")[-1]``

  MahalanobisConsistency
    *Liste de valeurs*. Chaque élément est une valeur de l'indicateur de
    qualité de Mahalanobis.

    Exemple : ``m = ADD.get("MahalanobisConsistency")[-1]``

  ObservedState
    *Liste de vecteurs*. Chaque élément est un vecteur d'état observé,
    c'est-à-dire dans l'espace des observations.

    Exemple : ``Ys = ADD.get("ObservedState")[-1]``

  OMA
    *Liste de vecteurs*. Chaque élément est un vecteur d'écart entre
    l'observation et l'état optimal dans l'espace des observations.

    Exemple : ``oma = ADD.get("OMA")[-1]``

  OMB
    *Liste de vecteurs*. Chaque élément est un vecteur d'écart entre
    l'observation et l'état d'ébauche dans l'espace des observations.

    Exemple : ``omb = ADD.get("OMB")[-1]``

  SigmaBck2
    *Liste de valeurs*. Chaque élément est une valeur de l'indicateur de
    qualité :math:`(\sigma^b)^2` de la partie ébauche.

    Exemple : ``sb2 = ADD.get("SigmaBck")[-1]``

  SigmaObs2
    *Liste de valeurs*. Chaque élément est une valeur de l'indicateur de
    qualité :math:`(\sigma^o)^2` de la partie observation.

    Exemple : ``so2 = ADD.get("SigmaObs")[-1]``

  SimulationQuantiles
    *Liste de vecteurs*. Chaque élément est un vecteur correspondant à l'état
    observé qui réalise le quantile demandé, dans le même ordre que les
    quantiles requis par l'utilisateur.

    Exemple : ``sQuantiles = ADD.get("SimulationQuantiles")[:]``
