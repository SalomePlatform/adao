La compatibilité du module est de plus vérifiée par rapport à diverses versions
de Python et des modules support comme Numpy et Scipy. L'étendue des versions
atteintes lors des tests dépend de leur disponibilité, et les tests ne sont pas
systématiques sur toutes les versions intermédiaires. Pour toutes les versions
testées, le module ADAO se comporte de manière identique (dans la mesure de
modifications dépendant des outils support). Il est fortement déconseillé (ou
impossible) d'utiliser ADAO avec une version inférieure à la version minimale,
et il n'y a pas de limitation à l'utilisation du module ADAO au-delà au-delà de
la version atteinte (mais cela reste sans garantie).

.. csv-table:: Intervalles de vérification des outils support pour ADAO
   :header: "Outil", "Version minimale", "Version atteinte"
   :widths: 20, 10, 10

   Python,     3.6.5,    3.10.9
   Numpy,      1.14.3,    1.24.2
   Scipy,      1.1.0,    1.10.0
   MatplotLib, 2.2.2,    3.6.3
   GnuplotPy,  1.8,    1.8
   NLopt,      2.4.2,    2.7.1
