.. _section_glossary:

Glossaire
=========

.. glossary::
   :sorted:

   cas
      Un cas ADAO est d�fini par un jeu de donn�es et de choix, rassembl�s par
      l'interm�diaire de l'interface utilisateur du module. Les donn�es sont les
      mesures physiques qui doivent �tre techniquement disponibles avant ou
      pendant l'ex�cution du cas. Le (ou les) code(s) de simulation et la
      m�thode d'assimilation de donn�es ou d'optimisation, ainsi que leurs
      param�tres, doivent �tre choisis, ils d�finissent les propri�t�s
      d'ex�cution du cas.

   it�ration
      Une it�ration a lieu lorsque l'on utilise des m�thodes d'optimisation
      it�ratives (par exemple le 3DVAR), et c'est enti�rement cach� �
      l'int�rieur du noeud principal de type YACS OptimizerLoop nomm�
      "*compute_bloc*". N�anmoins, l'utilisateur peut observer le processus
      it�ratif � l'aide de la fen�tre "*YACS Container Log*", qui est mise �
      jour au fur et � mesure du d�roulement du calcul, et en utilisant des
      "*Observers*" attach�s � des variables de calcul.

   APosterioriCovariance
      Mot-cl� indiquant la matrice de covariance des erreurs *a posteriori*
      d'analyse.

   BMA (Background minus Analysis)
      Diff�rence entre l'�tat d'�bauche et l'�tat optimal estim�, not�e
      :math:`\mathbf{x}^b - \mathbf{x}^a`.

   OMA (Observation minus Analysis)
      Diff�rence entre les observations et le r�sultat de la simulation bas�e
      sur l'�tat optimal estim�, l'analyse, filtr� pour �tre compatible avec les
      observations, not�e :math:`\mathbf{y}^o - \mathbf{H}\mathbf{x}^a`.

   OMB (Observation minus Background)
      Diff�rence entre les observations et le r�sultat de la simulation bas�e
      sur l'�tat d'�bauche,  filtr� pour �tre compatible avec les observations,
      not�e :math:`\mathbf{y}^o - \mathbf{H}\mathbf{x}^b`.

   SigmaBck2
      Mot-cl� indiquant le param�tre de Desroziers-Ivanov mesurant la
      consistance de la partie due � l'�bauche dans l'estimation optimale d'�tat
      par assimilation de donn�es. Sa valeur peut �tre compar�e � 1, une "bonne"
      estimation conduisant � un param�tre "proche" de 1.

   SigmaObs2
      Mot-cl� indiquant le param�tre de Desroziers-Ivanov mesurant la
      consistance de la partie due � l'observation dans l'estimation optimale
      d'�tat par assimilation de donn�es. Sa valeur peut �tre compar�e � 1, une
      "bonne" estimation conduisant � un param�tre "proche" de 1.

   MahalanobisConsistency
      Mot-cl� indiquant le param�tre de Mahalanobis mesurant la consistance de
      l'estimation optimale d'�tat par assimilation de donn�es. Sa valeur peut
      �tre compar�e � 1, une "bonne" estimation conduisant � un param�tre
      "proche" de 1.

   analyse
      L'�tat optimal estim� par une proc�dure d'assimilation de donn�es ou
      d'optimisation.

   background
      C'est le terme anglais pour d�signer l'�bauche.
  
   �bauche
      C'est l'�tat du syst�me connu *a priori*, qui n'est pas optimal, et qui
      est utilis� comme une estimation grossi�re, ou "la meilleure connue",
      avant une estimation optimale.

   innovation
      Diff�rence entre les observations et le r�sultat de la simulation bas�e
      sur l'�tat d'�bauche,  filtr� pour �tre compatible avec les observations.
      C'est similaire � OMB dans les cas statiques.

   CostFunctionJ
      Mot-cl� indiquant la fonction de minimisation, not�e :math:`J`.

   CostFunctionJo
      Mot-cl� indiquant la partie due aux observations dans la fonction de
      minimisation, not�e :math:`J^o`.

   CostFunctionJb
      Mot-cl� indiquant la partie due � l'�bauche dans la fonction de
      minimisation, not�e :math:`J^b`.