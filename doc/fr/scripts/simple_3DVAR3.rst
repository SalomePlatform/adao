Troisième exemple
.................

A partir de l'exemple précédent, si l'on veut adapter la convergence temporelle
du 3DVAR, on peut modifier par exemple les hypothèses de covariance *a priori*
des erreurs d'ébauche au cours des itérations. Cette remise à jour est une
**hypothèse** de l'utilisateur, et il y a de multiples possibilités qui vont
dépendre de la physique du cas. On en illustre une ici.

On choisit, **arbitrairement**, de faire décroître la covariance *a priori* des
erreurs d'ébauche d'un facteur constant :math:`0.9^2=0.81` tant qu'elle reste
supérieure à une valeur limite de :math:`0.1^2=0.01` (qui est la valeur fixe de
covariance *a priori* des erreurs d'ébauche de l'exemple précédent), sachant
qu'elle commence à la valeur `1` (qui est la valeur fixe de covariance *a
priori* des erreurs d'ébauche utilisée pour le premier pas du filtrage de
Kalman). Cette valeur est remise à jour à chaque pas, en la réinjectant comme
covariance *a priori* de l'état qui est utilisé comme ébauche lors du pas
suivant d'analyse, dans une boucle explicite.

On constate dans ce cas que l'estimation d'état converge plus vite vers la
valeur vraie, et que l'assimilation se comporte ensuite de manière similaire
aux :ref:`section_ref_algorithm_KalmanFilter_examples` pour le Filtre de
Kalman, ou à l'exemple précédent avec les covariances *a priori* manuellement
adaptée. De plus, la covariance *a posteriori* décroît tant que l'on force la
décroissance de la covariance *a priori*.

.. note::

    On insiste sur le fait que les variations de covariance *a priori*, qui
    conditionnent les variations de covariance *a posteriori*, relèvent d'une
    **hypothèse arbitraire de l'utilisateur** et non pas d'une obligation.
    Cette hypothèse doit donc être **adaptée en fonction du cas physique**.
