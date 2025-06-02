.. index:: single: ParameterCalibrationTask (exemple)

Premier exemple
...............

Cet exemple décrit le **recalage des paramètres** :math:`\mathbf{x}` d'un
modèle d'observation :math:`H` quadratique. Ce modèle :math:`H` est représenté
ici comme une fonction nommée ``QuadFunction`` pour les besoins de l'exemple.
Cette fonction accepte en entrée le vecteur de coefficients :math:`\mathbf{x}`
de la forme quadratique, et fournit en sortie le vecteur :math:`\mathbf{y}`
d'évaluation du modèle quadratique aux points de contrôle internes, prédéfinis
de manière statique dans le modèle.

Le recalage s'effectue sur la base d'un jeu initial de coefficients (état
d'ébauche désigné par ``Xb`` dans l'exemple), et avec l'information
:math:`\mathbf{y}^o` (désignée par ``Yobs`` dans l'exemple) de 5 mesures
obtenues aux points de contrôle internes. On se place ici en expériences
jumelles (voir :ref:`section_methodology_twin`), et les mesures sont
considérées comme parfaites. On choisit de privilégier les observations, au
détriment de l'ébauche, par l'indication artificielle d'une très importante
variance d'erreur d'ébauche, ici de :math:`10^{6}`.

On utilise une optimisation variationnelle de type 3DVAR (méthode par défaut),
explicitement demandée ici par la variante "3DVARGradientOptimization" indiquée
pour cet algorithme. On obtient par nature les mêmes résultats que dans le
premier exemple de l'algorithme du "3DVAR" (voir ses
:ref:`section_ref_algorithm_3DVAR_examples`).
