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

.. _section_ref_covariance_requirements:

Exigences pour décrire les matrices de covariance
-------------------------------------------------

.. index:: single: setBackgroundError
.. index:: single: setObservationError
.. index:: single: setEvolutionError
.. index:: single: matrice de covariance
.. index:: single: covariances d'erreurs d'ébauche
.. index:: single: covariances d'erreurs d'observation
.. index:: single: covariances

De manière générale, une matrice de variances-covariances, généralement appelée
matrice de covariance, doit être carrée, symétrique et semi-définie positive.
Chacun de ses termes décrit la covariance des deux variables aléatoires
correspondantes à sa position dans la matrice. La forme normalisée de la
covariance est la corrélation linéaire. On peut écrire la relation suivante,
entre une matrice de covariance :math:`\mathbf{M}` et ses matrices
correspondantes de corrélation :math:`\mathbf{C}` (matrice pleine) et
d'écart-type :math:`\mathbf{\Sigma}` (matrice diagonale):

.. math:: \mathbf{M} = \mathbf{\Sigma} * \mathbf{C} * \mathbf{\Sigma}

Diverses matrices de covariance sont nécessaires pour mettre en oeuvre des
procédures d'assimilation de données ou d'optimisation. Les principales sont la
matrice de covariance des erreurs d'ébauche, notée :math:`\mathbf{B}`, et la
matrice de covariance des erreurs d'observation, notée :math:`\mathbf{R}`.

Dans l'interface graphique EFICAS d'ADAO, il y a 3 méthodes pratiques pour
l'utilisateur pour fournir une matrice de covariance. La méthode est choisie à
l'aide du mot-clé "*INPUT_TYPE*" de chaque matrice de covariance, comme montré
dans la figure qui suit :

  .. eficas_covariance_matrix:
  .. image:: images/eficas_covariance_matrix.png
    :align: center
    :width: 100%
  .. centered::
    **Choisir la représentation d'une matrice de covariance**

Dans l'interface textuelle (TUI) d'ADAO (voir la partie :ref:`section_tui`),
les mêmes informations peuvent être données à l'aide de la commande adéquate
"*setBackgroundError*", "*setObservationError*" ou "*setEvolutionError*" selon
la grandeur physique à définir. Les autres arguments "*Matrix*",
"*ScalarSparseMatrix*" et "*DiagonalSparseMatrix*" de la commande permettent de
la définir comme décrit dans les sous-parties qui suivent. Ces informations
peuvent aussi être fournies dans un script contenu en fichier externe (argument
"*Script*").

Première forme matricielle : utiliser la représentation "*Matrix*"
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: Matrix
.. index:: single: BackgroundError
.. index:: single: EvolutionError
.. index:: single: ObservationError

La première forme est le défaut, et c'est la plus générale. La matrice de
covariance :math:`\mathbf{M}` doit être entièrement spécifiée. Même si la
matrice est symétrique par nature, la totalité de la matrice :math:`\mathbf{M}`
doit être fournie.

.. math:: \mathbf{M} =  \begin{pmatrix}
    m_{11} & m_{12} & \cdots   & m_{1n} \\
    m_{21} & m_{22} & \cdots   & m_{2n} \\
    \vdots & \vdots & \vdots   & \vdots \\
    m_{n1} & \cdots & m_{nn-1} & m_{nn}
    \end{pmatrix}

Cela peut être réalisé soit par un vecteur ou une matrice Numpy, soit par une
liste de listes de valeurs (c'est-à-dire une liste de lignes). Par exemple, une
matrice simple diagonale unitaire de covariances des erreurs d'ébauche
:math:`\mathbf{B}` peut être décrite dans un fichier de script Python par::

    BackgroundError = [[1, 0 ... 0], [0, 1 ... 0] ... [0, 0 ... 1]]

ou::

    BackgroundError = numpy.eye(...)

Seconde forme matricielle : utiliser la représentation "*ScalarSparseMatrix*"
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: ScalarSparseMatrix
.. index:: single: BackgroundError
.. index:: single: EvolutionError
.. index:: single: ObservationError

Au contraire, la seconde forme matricielle est une méthode très simplifiée pour
définir une matrice. La matrice de covariance :math:`\mathbf{M}` est ici
supposée être un multiple positif de la matrice identité. Cette matrice peut
alors être spécifiée de manière unique par le multiplicateur :math:`m`:

.. math:: \mathbf{M} =  m \times \begin{pmatrix}
    1       & 0      & \cdots   & 0      \\
    0       & 1      & \cdots   & 0      \\
    \vdots  & \vdots & \vdots   & \vdots \\
    0       & \cdots & 0        & 1
    \end{pmatrix}

Le multiplicateur :math:`m` doit être un nombre réel ou entier positif (s'il
est négatif, ce qui est impossible car une matrice de covariance est positive,
il est convertit en nombre positif). Par exemple, une simple matrice diagonale
unitaire de covariances des erreurs d'ébauche :math:`\mathbf{B}` peut être
décrite dans un fichier de script Python par::

    BackgroundError = 1.

ou, mieux, par un argument "*String*" directement dans le cas graphique ou
textuel ADAO.

Troisième forme matricielle : utiliser la représentation "*DiagonalSparseMatrix*"
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: DiagonalSparseMatrix
.. index:: single: BackgroundError
.. index:: single: EvolutionError
.. index:: single: ObservationError

La troisième forme est aussi une méthode simplifiée pour fournir la matrice,
mais un peu plus puissante que la seconde. La matrice de covariance
:math:`\mathbf{M}` est ici toujours considérée comme diagonale, mais
l'utilisateur doit spécifier toutes les valeurs positives situées sur la
diagonale. La matrice peut alors être définie uniquement par un vecteur
:math:`\mathbf{V}` qui se retrouve ensuite sur la diagonale:

.. math:: \mathbf{M} =  \begin{pmatrix}
    v_{1}  & 0      & \cdots   & 0      \\
    0      & v_{2}  & \cdots   & 0      \\
    \vdots & \vdots & \vdots   & \vdots \\
    0      & \cdots & 0        & v_{n}
    \end{pmatrix}

Cela peut être réalisé soit par vecteur ou une matrice Numpy, soit par
une liste, soit par une liste de listes de valeurs positives (dans tous les cas,
si certaines valeurs sont négatives, elles sont converties en valeurs
positives). Par exemple, un matrice simple diagonale unitaire des covariances
des erreurs d'ébauche :math:`\mathbf{B}` peut être décrite dans un fichier de
script Python par::

    BackgroundError = [1, 1 ... 1]

ou::

    BackgroundError = numpy.ones(...)

De la même manière que précédemment, on peut aussi définir cette matrice par
un "*String*" directement dans le cas graphique ou textuel ADAO.
