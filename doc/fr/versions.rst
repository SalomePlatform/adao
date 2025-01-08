..
   Copyright (C) 2008-2025 EDF R&D

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

.. _section_versions:

================================================================================
Versions d'ADAO et compatibilités externes
================================================================================

.. _subsection_new_adao_version:
.. index::
    pair: Version ; ADAO
    pair: Version d'ADAO ; Changement de

Passer d'une version d'ADAO à une nouvelle
------------------------------------------

Le module ADAO et ses fichiers de cas ".comm" sont identifiés par des versions,
avec des caractéristiques "Major", "Minor", "Revision" et optionnellement
"Installation". Une version particulière est numérotée "Major.Minor.Revision",
avec un lien fort avec la numérotation de la plateforme SALOME. L'indication
optionnelle d'un quatrième numéro désigne une différence dans le mode
d'installation, pas dans le contenu de la version.

Chaque version "Major.Minor.Revision" du module ADAO peut lire les fichiers de
cas ADAO de la précédente version mineure "Major.Minor-1.*". En général, elle
peut aussi lire les fichiers de cas de toutes les versions mineures "Major.*.*"
d'une branche majeure, mais ce n'est pas obligatoirement vrai pour toutes les
commandes ou tous les mots-clés. En général aussi, un fichier de cas ADAO d'une
version ne peut pas être lu par une précédente version mineure ou majeure du
module ADAO.

Passer de la version 9.x à la 9.y avec y > x
++++++++++++++++++++++++++++++++++++++++++++

Il n'y a pas d'incompatibilité connue pour les fichiers de cas ADAO. La
procédure de montée en version consiste à lire l'ancien fichier de cas ADAO
avec le nouveau module SALOME/ADAO, et à l'enregistrer avec un nouveau nom.

Cependant, il peut se présenter des incompatibilités provenant de cas
utilisateurs écrits directement en interface TUI. Il est conseillé de revoir la
syntaxe et les arguments dans les scripts TUI à chaque changement de version.
En particulier, il convient de vérifier que les paramètres d'algorithme sont
toujours adéquats et actifs, sachant qu'il a été explicitement choisi qu'il n'y
ait pas de message lorsqu'un paramètre optionnel devient inactif ou change de
nom (pour l'exemple, on cite le paramètre "*MaximumNumberOfSteps*" comme ayant
changé de nom pour devenir "*MaximumNumberOfIterations*", par homogénéité avec
les variables pouvant être affichées) pour éviter un blocage.

Passer de la version 8.5 à la 9.2
+++++++++++++++++++++++++++++++++

Il n'y a pas d'incompatibilité connue pour les fichiers de cas ADAO. La
procédure de montée en version consiste à lire l'ancien fichier de cas ADAO
avec le nouveau module SALOME/ADAO, et à l'enregistrer avec un nouveau nom.

Cependant, il peut se présenter des incompatibilités provenant de fichiers
scripts utilisateurs qui n'auraient pas une syntaxe compatible avec Python 3.
L'erreur la plus immédiate est l'usage de l'impression "*print*" avec la
syntaxe "*commande*" au lieu de la syntaxe fonctionnelle "*print(...)*". Dans
ce cas, il est suggéré de corriger la syntaxe des fichiers utilisateurs dans
l'environnement 8 avant de passer en environnement 9.

Passer de la version 8.x à la 8.y avec y > x
++++++++++++++++++++++++++++++++++++++++++++

Il n'y a pas d'incompatibilité connue pour les fichiers de cas ADAO. La
procédure de montée en version consiste à lire l'ancien fichier de cas ADAO
avec le nouveau module SALOME/ADAO, et à l'enregistrer avec un nouveau nom.

Pour faciliter les futures évolutions, il est fortement recommandé de veiller à
ce que vos fichiers scripts utilisateurs utilisent une syntaxe compatible avec
Python 2 et avec Python 3. En particulier, on recommande d'utiliser la syntaxe
fonctionnelle pour les "*print*" et non pas la syntaxe "*commande*", comme par
exemple :
::

    # Python 2 & 3
    x, unit = 1., "cm"
    print( "x = %s %s"%(str(x),str(unit)) )

ou :
::

    # Python 2 & 3
    x, unit = 1., "cm"
    print( "x = {0} {1}".format(str(x),str(unit)) )

plutôt que :
::

    # Python 2 uniquement
    x, unit = 1., "cm"
    print "x =", x, unit

Passer de la version 7.8 à la 8.1
+++++++++++++++++++++++++++++++++

Il n'y a pas d'incompatibilité connue pour les fichiers de cas ADAO. La
procédure de montée en version consiste à lire l'ancien fichier de cas ADAO
avec le nouveau module SALOME/ADAO, et à l'enregistrer avec un nouveau nom.

Passer de la version 7.x à la 7.y avec y > x
++++++++++++++++++++++++++++++++++++++++++++

Il n'y a pas d'incompatibilité connue pour les fichiers de cas ADAO. La
procédure de montée en version consiste à lire l'ancien fichier de cas ADAO
avec le nouveau module SALOME/ADAO, et à l'enregistrer avec un nouveau nom.

Passer de la version 6.6 à la 7.2
+++++++++++++++++++++++++++++++++

Il n'y a pas d'incompatibilité connue pour les fichiers de cas ADAO. La
procédure de montée en version consiste à lire l'ancien fichier de cas ADAO avec
le nouveau module SALOME/ADAO, et à l'enregistrer avec un nouveau nom.

Il y a une incompatibilité introduite dans les fichiers de script de
post-processing ou d'observers. L'ancienne syntaxe pour interroger un objet
résultat, comme celui d'analyse "*Analysis*" (fourni dans un script à travers le
mot-clé "*UserPostAnalysis*"), était par exemple :
::

    Analysis = ADD.get("Analysis").valueserie(-1)
    Analysis = ADD.get("Analysis").valueserie()

La nouvelle syntaxe est entièrement compatible avec celle (classique) pour les
objets de type liste ou tuple :
::

    Analysis = ADD.get("Analysis")[-1]
    Analysis = ADD.get("Analysis")[:]

Les scripts de post-processing doivent être modifiés.

Passer de la version 6.x à la 6.y avec y > x
++++++++++++++++++++++++++++++++++++++++++++

Il n'y a pas d'incompatibilité connue pour les fichiers de cas ADAO. La
procédure de montée en version consiste à lire l'ancien fichier de cas ADAO avec
le nouveau module SALOME/ADAO, et à l'enregistrer avec un nouveau nom.

Il y a une incompatibilité introduite dans les fichiers de script d'opérateur,
lors de la dénomination des opérateurs élémentaires utilisés pour l'opérateur
d'observation par script. Les nouveaux noms requis sont "*DirectOperator*",
"*TangentOperator*" et "*AdjointOperator*", comme décrit dans la quatrième
partie du chapitre :ref:`section_reference`. Les fichiers de script d'opérateur
doivent être modifiés.

.. _subsection_version_compatibility:
.. index::
    pair: Version ; ADAO
    pair: Version ; SALOME
    pair: Version ; EFICAS
    pair: Version ; Python
    pair: Version ; Numpy
    pair: Version ; Scipy
    pair: Version ; MatplotLib
    pair: Version ; Gnuplot
    pair: Version ; NLopt

Versions de compatibilité d'ADAO avec les outils support
--------------------------------------------------------

Le module ADAO bénéficie largement de l'**environnement Python** [Python]_ et
des nombreuses possibilités de ce langage, des outils de calcul scientifique
inclus dans **NumPy** [NumPy20]_, **SciPy** [SciPy20]_, **NLopt** [Johnson08]_
ou dans les outils atteignables grâce à eux, et des nombreuses capacités de
**SALOME** [Salome]_ lorsqu'il est utilisé en association.

.. include:: snippets/ModuleValidation.rst

.. include:: snippets/ModuleCompatibility.rst
