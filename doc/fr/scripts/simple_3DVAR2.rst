Deuxième exemple
................

Le 3DVAR peut aussi être utilisé pour une **analyse temporelle des observations
d'un modèle dynamique donné**. Dans ce cas, l'analyse est conduite de manière
itérative, lors de l'arrivée de chaque observation. On utilise pour cet exemple
le même système dynamique simple [Welch06]_ que celui qui est analysé dans les
:ref:`section_ref_algorithm_KalmanFilter_examples` du Filtre de Kalman.

A chaque étape, l'analyse 3DVAR classique remet à jour uniquement l'état du
système. Moyennant une modification des valeurs de covariances *a priori* par
rapport aux hypothèses initiales du filtrage, cette réanalyse 3DVAR permet de
converger vers la trajectoire vraie, comme l'illustre la figure associée, de
manière ici un peu plus lente qu'avec un Filtre de Kalman.

.. note::

    Remarque concernant les covariances *a posteriori* : classiquement,
    l'analyse itérative 3DVAR remet à jour uniquement l'état et non pas sa
    covariance. Comme les hypothèses d'opérateurs et de covariance *a priori*
    restent inchangées ici au cours de l'évolution, la covariance *a
    posteriori* est constante. Le tracé qui suit de cette covariance *a
    posteriori* permet d'insister sur cette propriété tout à fait attendue de
    l'analyse 3DVAR. Une hypothèse plus évoluée est proposée dans l'exemple qui
    suit.
