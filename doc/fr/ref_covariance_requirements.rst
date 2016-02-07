..
   Copyright (C) 2008-2016 EDF R&D

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

Exigences pour d�crire les matrices de covariance
-------------------------------------------------

.. index:: single: matrice de covariance
.. index:: single: covariances d'erreurs d'�bauche
.. index:: single: covariances d'erreurs d'observation
.. index:: single: covariances

De mani�re g�n�rale, une matrice de covariance (ou une matrice de
variance-covariance) doit �tre carr�e, sym�trique, semi-d�finie positive. Chacun
de ses termes d�crit la covariance des deux variables al�atoires correspondantes
� sa position dans la matrice. La forme normalis�e de la covariance est la
corr�lation lin�aire. On peut �crire la relation suivante, entre une matrice de
covariance :math:`\mathbf{M}` et ses matrices correspondantes de corr�lation
:math:`\mathbf{C}` (matrice pleine) et d'�cart-type :math:`\mathbf{\Sigma}`
(matrice diagonale):

.. math:: \mathbf{M} = \mathbf{\Sigma} * \mathbf{C} * \mathbf{\Sigma}

Diverses matrices de covariance sont n�cessaires pour mettre en oeuvre des
proc�dures d'assimilation de donn�es ou d'optimisation. Les principales sont la
matrice de covariance des erreurs d'�bauche, not�e :math:`\mathbf{B}`, et la
matrice de covariance des erreurs d'observation, not�e :math:`\mathbf{R}`.

Il y a 3 m�thodes pratiques pour l'utilisateur pour fournir une matrice de
covariance. La m�thode est choisie � l'aide du mot-cl� "*INPUT_TYPE*" de chaque
matrice de covariance, comme montr� dans la figure qui suit :

  .. eficas_covariance_matrix:
  .. image:: images/eficas_covariance_matrix.png
    :align: center
    :width: 100%
  .. centered::
    **Choisir la repr�sentation d'une matrice de covariance**

Premi�re forme matricielle : utiliser la repr�sentation "*Matrix*"
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: Matrix
.. index:: single: BackgroundError
.. index:: single: EvolutionError
.. index:: single: ObservationError

La premi�re forme est le d�faut, et c'est la plus g�n�rale. La matrice de
covariance :math:`\mathbf{M}` doit �tre enti�rement sp�cifi�e. M�me si la
matrice est sym�trique par nature, la totalit� de la matrice :math:`\mathbf{M}`
doit �tre donn�e.

.. math:: \mathbf{M} =  \begin{pmatrix}
    m_{11} & m_{12} & \cdots   & m_{1n} \\
    m_{21} & m_{22} & \cdots   & m_{2n} \\
    \vdots & \vdots & \vdots   & \vdots \\
    m_{n1} & \cdots & m_{nn-1} & m_{nn}
    \end{pmatrix}

Cela peut �tre r�alis� soit par un vecteur ou une matrice Numpy, soit par une
liste de listes de valeurs (c'est-�-dire une liste de lignes). Par exemple, une
matrice simple diagonale unitaire de covariances des erreurs d'�bauche
:math:`\mathbf{B}` peut �tre d�crite dans un fichier de script Python par::

    BackgroundError = [[1, 0 ... 0], [0, 1 ... 0] ... [0, 0 ... 1]]

ou::

    BackgroundError = numpy.eye(...)

Seconde forme matricielle : utiliser la repr�sentation "*ScalarSparseMatrix*"
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: ScalarSparseMatrix
.. index:: single: BackgroundError
.. index:: single: EvolutionError
.. index:: single: ObservationError

Au contraire, la seconde forme matricielle est une m�thode tr�s simplifi�e pour
d�finir une matrice. La matrice de covariance :math:`\mathbf{M}` est ici
suppos�e �tre un multiple positif de la matrice identit�. Cette matrice peut
alors �tre sp�cifi�e de mani�re unique par le multiplicateur :math:`m`:

.. math:: \mathbf{M} =  m \times \begin{pmatrix}
    1       & 0      & \cdots   & 0      \\
    0       & 1      & \cdots   & 0      \\
    \vdots  & \vdots & \vdots   & \vdots \\
    0       & \cdots & 0        & 1
    \end{pmatrix}

Le multiplicateur :math:`m` doit �tre un nombre r�el ou entier positif (s'il
est n�gatif, ce qui est impossible car une matrice de covariance est positive,
il est convertit en nombre positif). Par exemple, une simple matrice diagonale
unitaire de covariances des erreurs d'�bauche :math:`\mathbf{B}` peut �tre
d�crite dans un fichier de script Python par::

    BackgroundError = 1.

ou, mieux, par un "*String*" directement dans le cas ADAO.

Troisi�me forme matricielle : utiliser la repr�sentation "*DiagonalSparseMatrix*"
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: DiagonalSparseMatrix
.. index:: single: BackgroundError
.. index:: single: EvolutionError
.. index:: single: ObservationError

La troisi�me forme est aussi une m�thode simplifi�e pour fournir la matrice,
mais un peu plus puissante que la seconde. La matrice de covariance
:math:`\mathbf{M}` est ici toujours consid�r�e comme diagonale, mais
l'utilisateur doit sp�cifier toutes les valeurs positives situ�es sur la
diagonale. La matrice peut alors �tre d�finie uniquement par un vecteur
:math:`\mathbf{V}` qui se retrouve ensuite sur la diagonale:

.. math:: \mathbf{M} =  \begin{pmatrix}
    v_{1}  & 0      & \cdots   & 0      \\
    0      & v_{2}  & \cdots   & 0      \\
    \vdots & \vdots & \vdots   & \vdots \\
    0      & \cdots & 0        & v_{n}
    \end{pmatrix}

Cela peut �tre r�alis� soit par vecteur ou une matrice Numpy, soit par
une liste, soit par une liste de listes de valeurs positives (dans tous les cas,
si certaines valeurs sont n�gatives, elles sont converties en valeurs
positives). Par exemple, un matrice simple diagonale unitaire des covariances
des erreurs d'�bauche :math:`\mathbf{B}` peut �tre d�crite dans un fichier de
script Python par::

    BackgroundError = [1, 1 ... 1]

ou::

    BackgroundError = numpy.ones(...)
