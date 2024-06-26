.. index:: single: NonLinearLeastSquares (exemple)

Cet exemple décrit le recalage des paramètres :math:`\mathbf{x}` d'un modèle
d'observation :math:`H` quadratique. Ce modèle est représenté ici comme une
fonction nommée ``QuadFunction``. Cette fonction accepte en entrée le vecteur
de coefficients :math:`\mathbf{x}`, et fournit en sortie le vecteur
:math:`\mathbf{y}` d'évaluation du modèle quadratique aux points de contrôle
internes prédéfinis dans le modèle. Le calage s'effectue sur la base d'un jeu
initial de coefficients (état d'ébauche désigné par ``Xb`` dans l'exemple), et
avec l'information :math:`\mathbf{y}^o` (désignée par ``Yobs`` dans l'exemple)
de 5 mesures obtenues à ces mêmes points de contrôle internes. On se place en
expériences jumelles (voir :ref:`section_methodology_twin`) et les mesures sont
parfaites.

L'ajustement s'effectue en affichant des résultats intermédiaires lors de
l'optimisation itérative.
