.. index:: single: ExecuteInContainer

ExecuteInContainer
  *Commande optionnelle*. Cette variable permet de choisir le mode d'exécution
  dans YACS en container spécifique. En son absence ou si sa valeur est "No",
  il n'est pas utilisé de container séparé pour l'exécution et elle se déroule
  dans le processus principal de YACS. Si sa valeur est "Mono", un container
  YACS spécifique est crée et il est utilisé pour héberger l'exécution de tous
  les noeuds dans un même processus. Si sa valeur est "Multi", un container
  YACS spécifique est crée et il est utilisé pour héberger l'exécution de
  chaque noeud dans un processus spécifique. La valeur par défaut est "No", et
  les choix possibles sont "No", "Mono" et "Multi".

  .. warning::

    dans sa présente version, cet commande est expérimentale, et reste donc
    susceptible de changements dans les prochaines versions.
