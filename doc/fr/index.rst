================================================================================
Documentation ADAO
================================================================================

.. image:: images/ADAO_logo.png
   :align: center
   :width: 20%

Le module ADAO fournit des fonctionnalités d'**assimilation de données et
d'optimisation** dans un contexte SALOME. Il est basé sur l'utilisation d'autres
modules, à savoir YACS et EFICAS, et sur l'utilisation d'une bibliothèque
générique sous-jacente d'assimilation de données.

En bref, l'assimilation de données est un cadre méthodologique pour calculer
l'estimation optimale de la valeur réelle (inaccessible) de l'état d'un système
au cours du temps. Il utilise des informations provenant de mesures
expérimentales, ou observations, et de modèles numériques *a priori*, y compris
des informations sur leurs erreurs. Certaines des méthodes incluses dans ce
cadre sont également connues sous les noms  d'*estimation des paramètres*, de
*problèmes inverses*, d'*estimation bayésienne*, d'*interpolation optimale*,
etc. De plus amples détails peuvent être trouvés dans la section
:ref:`section_theory`.

La documentation de ce module est divisée en plusieurs parties. La première
:ref:`section_intro` est une introduction. La deuxième partie
:ref:`section_theory` présente brièvement l'assimilation de données,
l'optimisation et les concepts. La troisième partie :ref:`section_using`
explique comment utiliser le module ADAO. La quatrième partie
:ref:`section_reference` donne une description détaillée de toutes les commandes
ADAO et des mots-clés. La cinquième partie :ref:`section_examples` donne des
exemples sur l'utilisation d'ADAO. Les utilisateurs intéressés par une
accès rapide au module peuvent sauter cette section, mais un usage utile
du module nécessite de lire et de revenir régulièrement aux troisième et
quatrième parties. La dernière partie :ref:`section_advanced` se focalise sur
des usages avancés du module, sur l'obtention de plus de renseignements, ou sur
l'usage par scripting, sans interface utilisateur graphique (GUI). Enfin,
n'oubliez pas de lire la partie :ref:`section_licence` pour respecter les
exigences de licence du module.

Dans cette documentation, on utilise les notations standards de l'algèbre
linéaire, de l'assimilation de données (comme décrit dans [Ide97]_) et de
l'optimisation. En particulier, les vecteurs sont écrits horizontalement ou
verticalement sans faire la différence. Les matrices sont écrites soit
normalement, ou avec une notation condensée, consistant à utiliser un espace
pour séparer les valeurs, et un "``;``" pour séparer les lignes de la matrice,
de façon continue sur une ligne.

Table des matières
------------------

.. toctree::
   :maxdepth: 2

   intro
   theory
   using
   reference
   examples
   advanced
   licence
   bibliography

Index et tables
---------------

* :ref:`genindex`
* :ref:`search`
* :ref:`section_glossary`
