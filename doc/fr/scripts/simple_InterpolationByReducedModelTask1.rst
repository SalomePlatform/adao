.. index:: single: InterpolationByReducedModelTask (example)

Premier exemple
...............

Cet exemple décrit la mise en oeuvre d'une **reconstruction par
interpolation**, faisant suite à l'établissement d'une représentation réduite
par une recherche de *positionnement optimal de mesures*.

Pour l'illustration, on utilise la même collection artificielle de champs
physiques très simple (engendré de manière à exister dans un espace vectoriel
de dimension 2) que pour les :ref:`exemples d'étude avec
"MeasurementsOptimalPositioningTask"<section_ref_algorithm_MeasurementsOptimalPositioningTask_examples>`.
La recherche de positionnement ADAO préalable permet d'obtenir 2 positions
optimales pour les mesures, qui servent ensuite à établir une interpolation de
champ physique à partir de mesures aux positions optimales.
