#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os, sys, shutil, tempfile, glob
from math import log10

# Variables globales
debug=False
ASTER_ROOT   = ''
SOURCES_ROOT = ''
export = None
calcul = None
parametres = None
python_version = ''

#===============================================================================
def UTMESS(code='I', txt=''):
   print txt
   if code=='F': sys.exit()

#===============================================================================
def get_tables(tables_calc,tmp_repe_table,prof):
   """ Recupere les resultats Aster (Table Aster -> Numeric Python)
   """
   global debug
   import Numeric
   assert (tables_calc is not None)
   assert (tmp_repe_table is not None)

   # Import du module lire_table
   if os.environ.has_key('ASTER_ROOT'):
      version = prof['version'][0]
      bibpyt = os.path.join(os.environ['ASTER_ROOT'], version, 'bibpyt')
      sys.path.append(bibpyt)
      for mdl in glob.glob(os.path.join(bibpyt, '*')):
     	 sys.path.append(os.path.join(os.environ['ASTER_ROOT'], version, 'bibpyt', mdl))
   try:
      from lire_table_ops import lecture_table
   except:
      UTMESS('F', "Impossible d'importer le module lire_table!")

   reponses = tables_calc
   Lrep=[]
   _TB = [None]*len(reponses)
   for i in range(len(reponses)):
      _fic_table = tmp_repe_table + os.sep + "fort."+str(int(100+i))

      try:
	 file=open(_fic_table,'r')
	 texte=file.read()
	 file.close()
      except Exception, err:
	 ier=1
	 message = "Erreur 1!\n" + str(err)
	 UTMESS('F', message)

      try:
	 table_lue = lecture_table(texte, 1, ' ')
	 list_para = table_lue.para
	 tab_lue   = table_lue.values()
      except Exception, err:
	 ier=1
	 message = "Erreur 2!\n" + str(err)
      else:
	 ier=0

      if ier!=0 : UTMESS('F', message)

      try:
	  nb_val = len(tab_lue[ list_para[0] ])
	  F = Numeric.zeros((nb_val,2), Numeric.Float)
	  for k in range(nb_val):
	    F[k][0] = tab_lue[ str(reponses[i][1]) ][k]
	    F[k][1] = tab_lue[ str(reponses[i][2]) ][k]
	  Lrep.append(F)
      except Exception, err:
	  message = "Erreur 3!\n" + str(err)
	  UTMESS('F', message)
   resu_calc = Lrep
   if debug: print 'resu_calc:', resu_calc

   return resu_calc
#===============================================================================


#===============================================================================
def Calcul_Aster_Ponctuel( X0 = None ):
    #
    global ASTER_ROOT
    global debug
    global SOURCES_ROOT
    global export
    global calcul
    global parametres
    global python_version

    import numpy
    if type(X0) is type(numpy.matrix([])):
        X0 = X0.A1.tolist()
    else:
        X0 = list(X0)
    # ----------------------------------------------------------------------------
    # Parametres
    #isFromYacs = globals().get('ASTER_ROOT', None)  # execution via YACS ou en externe
    #isFromYacs = ASTER_ROOT
    #print "isFromYacs:", isFromYacs
    #if not isFromYacs:
    #    from N_Parameters import ASTER_ROOT, debug, SOURCES_ROOT, DISPLAY
    #    from N_Study_Parameters import export
    #    from N_MR_Parameters import calcul, parametres
    os.environ['ASTER_ROOT'] = ASTER_ROOT

    # ----------------------------------------------------------------------------
    # Repertoire contenant les resultats des calculs Aster (None = un rep temp est cree)
    resudir = globals().get('resudir', None)

    # ----------------------------------------------------------------------------
    # Parametres remis en forme
    list_params = [x[0] for x in parametres]
    list_calc = calcul

    # ----------------------------------------------------------------------------
    # Procedure de calculs distribues
    #
    # Import des modules python d'ASTK
    astk_serv_root = os.path.join(ASTER_ROOT, 'ASTK', 'ASTK_SERV')
    sys.path.append(os.path.join(astk_serv_root, 'lib'))
    sys.path.append(os.path.join(ASTER_ROOT, 'lib', python_version, 'site-packages'))
    if debug:
        print sys.path
    try:
      from asrun.run          import AsRunFactory
      from asrun.profil       import ASTER_PROFIL
      from asrun.common_func  import get_hostrc
      from asrun.utils        import get_timeout
      from asrun.parametric   import is_list_of_dict
      from asrun.thread       import Dispatcher
      from asrun.distrib      import DistribParametricTask
    except Exception, e:
      print e
      UTMESS('F', "Impossible de determiner l'emplacement d'Aster ! Fixer le chemin avec la variable d'environnement ASTER_ROOT.")

    # Import des modules supplementaires
    sys.path.insert(0, SOURCES_ROOT)
    sys.path.insert(0, os.path.join(SOURCES_ROOT, 'sources'))


    # result directories
    if resudir:
       if not os.path.isdir(resudir):
          try:    os.mkdir(resudir)
          except: 
             UTMESS('A', "Impossible de creer le repertoire : %s. On utilise un repertoire temporaire" % resudir)
             resudir = None
    if not resudir: resudir = tempfile.mkdtemp(prefix='tmp_macr_recal_')
    flashdir = os.path.join(resudir,'flash')
    UTMESS('I', "\n       ASTER Exécution simple\n       Répertoire temporaire de résultats : %s" % resudir)

    sys.argv = ['']

    run = AsRunFactory()

    prof = ASTER_PROFIL(filename=export)
    #prof = init_profil_from(run, prof, keep_surch=True)
    prof.Set('R', {
       'type' : 'repe', 'isrep' : True, 'ul' : 0, 'compr' : False,
       'path' : '/tmp/test_param' })

    if debug: print prof
    prof.WriteExportTo( os.path.join(resudir, 'master.export') )

    # get hostrc object
    hostrc = get_hostrc(run, prof)

    # timeout before rejected a job
    timeout = get_timeout(prof)


    # list of parameters
    list_val = []

    # Dictionnaire des parametres du point courant
    dic = dict( zip( list_params, X0 ) )
    list_val.append( dic )

    assert is_list_of_dict(list_val)
    nbval = len(list_val)


    # Ajout des impressions de tables a la fin du .comm
    t = []
    reponses = list_calc
    for i in range(len(reponses)):
        _ul = str(int(100+i))
        num_ul = '99'

        try:    os.remove( tmp_macr_recal+os.sep+"REPE_TABLE"+os.sep+"fort."+_ul )
        except: pass

        t.append("\n# Recuperation de la table : " + str(reponses[i][0]) + "\n")
        t.append("DEFI_FICHIER(UNITE=" + num_ul + ", FICHIER='" + os.path.join('.', 'REPE_OUT', 'fort.'+_ul) + "',);\n" )
        t.append("IMPR_TABLE(TABLE="+str(reponses[i][0])+", FORMAT='ASTER', UNITE="+num_ul+", INFO=1, FORMAT_R='E30.20',);\n")
        t.append("DEFI_FICHIER(ACTION='LIBERER', UNITE="+num_ul+",);\n")


    # number of threads to follow execution
    numthread = 1

    # ----- Execute calcutions in parallel using a Dispatcher object
    # elementary task...
    task = DistribParametricTask(run=run, prof=prof, # IN
		       hostrc=hostrc,
		       nbmaxitem=0, timeout=timeout,
		       resudir=resudir, flashdir=flashdir,
		       keywords={'POST_CALCUL': '\n'.join(t)},
		       info=1,
		       nbnook=0, exec_result=[])	    # OUT
    # ... and dispatch task on 'list_tests'
    etiq = 'calc_%%0%dd' % (int(log10(nbval)) + 1)
    labels = [etiq % (i+1) for i in range(nbval)]
    couples = zip(labels, list_val)
    execution = Dispatcher(couples, task, numthread=numthread)

    iret = 0
    if task.nbnook > 0:
        iret = 4
    #run.Sortie(iret)

    # Recuperation des tables calculees
    seq_FX   = []
    seq_FY   = []
    seq_DIMS = []
    lst_DIAG = []
    lst_iter = []
    i=0
    for c in labels:
        tbl = get_tables(tables_calc=list_calc, tmp_repe_table=os.path.join(resudir, c, 'REPE_OUT'), prof=prof)
        FX = []
        FY = []
        ldims = []
        for array in tbl:
#           print 'AA1:', array
#           print array[0]
            FX.extend([ x[0] for x in array ])
            FY.extend([ x[1] for x in array ])
            ldims.append(len(array))

        # Agregation des resultats
        seq_FX.append(FX)
        seq_FY.append(FY)
        seq_DIMS.append(ldims)
        lst_iter.append(i)
        i+=1

    # Liste des diagnostics
    d_diag = {}
    for result in task.exec_result:
        label = result[0]
        diag  = result[2]
        d_diag[label] = diag
    lst_DIAG = [ d_diag[label] for label in labels]

    if debug:
        print
        print "list_calc =",list_calc
        print "seq_FX    =",seq_FX
        print "seq_FY    =",seq_FY
        print "seq_DIMS  =",seq_DIMS
        print "lst_DIAG  =",lst_DIAG
        print "lst_iter  =",lst_iter
        print

    # ----------------------------------------------------------------------------
    # Procedure d'assemblage du gradient

    # Calcul maitre (point X0)
    idx0 = lst_iter.index(0)   # index (les calculs arrivent-ils dans le desordre?)
    FY_X0 = seq_FY[idx0]
    H_de_X = FY_X0

    # Arret si tous les jobs ne se sont pas deroules correctement
    for diag in lst_DIAG:
        if not diag[0:2] in ['OK', '<A']:
            raise ValueError("Au moins un calcul ne s'est pas deroule normalement")

    if debug:
        print "\nH_de_X (calcul ponstuel) au point X0: \n%s" % str(H_de_X)

    return H_de_X

#===============================================================================
def Calcul_Aster_Jacobienne( X0 = None ):
    global ASTER_ROOT
    global debug
    global SOURCES_ROOT
    global export
    global calcul
    global parametres
    global python_version
    #
    import numpy
    if type(X0) is type(numpy.matrix([])):
        X0 = X0.A1.tolist()
    else:
        X0 = list(X0)
    # ----------------------------------------------------------------------------
    FacteurdX = 1.e-4
    dX = globals().get('dX', [ x*FacteurdX for x in X0 ])  # execution via YACS ou en externe
    # dX = globals().get('dX', [ 0.1, 0.1, 0.001])  # execution via YACS ou en externe
    # ----------------------------------------------------------------------------
    # Parametres
    #isFromYacs = globals().get('ASTER_ROOT', None)  # execution via YACS ou en externe
    #if not isFromYacs:
    #    from N_Parameters import ASTER_ROOT, debug, SOURCES_ROOT, DISPLAY
    #    from N_Study_Parameters import export
    #    from N_MR_Parameters import calcul, parametres
    os.environ['ASTER_ROOT'] = ASTER_ROOT

    # ----------------------------------------------------------------------------
    # Repertoire contenant les resultats des calculs Aster (None = un rep temp est cree)
    resudir = globals().get('resudir', None)

    # ----------------------------------------------------------------------------
    # Parametres remis en forme
    list_params = [x[0] for x in parametres]
    list_calc = calcul

    # ----------------------------------------------------------------------------
    # Procedure de calculs distribues
    #
    # Import des modules python d'ASTK
    astk_serv_root = os.path.join(ASTER_ROOT, 'ASTK', 'ASTK_SERV')
    sys.path.append(os.path.join(astk_serv_root, 'lib'))
    sys.path.append(os.path.join(ASTER_ROOT, 'lib', python_version, 'site-packages'))
    if debug:
        print sys.path
    try:
      from asrun.run          import AsRunFactory
      from asrun.profil       import ASTER_PROFIL
      from asrun.common_func  import get_hostrc
      from asrun.utils        import get_timeout
      from asrun.parametric   import is_list_of_dict
      from asrun.thread       import Dispatcher
      from asrun.distrib      import DistribParametricTask
    except Exception, e:
      print e
      UTMESS('F', "Impossible de determiner l'emplacement d'Aster ! Fixer le chemin avec la variable d'environnement ASTER_ROOT.")

    # Import des modules supplementaires
    sys.path.insert(0, SOURCES_ROOT)
    sys.path.insert(0, os.path.join(SOURCES_ROOT, 'sources'))


    # result directories
    if resudir:
       if not os.path.isdir(resudir):
          try:    os.mkdir(resudir)
          except: 
             UTMESS('A', "Impossible de creer le repertoire : %s. On utilise un repertoire temporaire" % resudir)
             resudir = None
    if not resudir: resudir = tempfile.mkdtemp(prefix='tmp_macr_recal_')
    flashdir = os.path.join(resudir,'flash')
    UTMESS('I', "\n       ASTER Exécutions multiples\n       Répertoire temporaire de résultats : %s" % resudir)

    sys.argv = ['']

    run = AsRunFactory()

    prof = ASTER_PROFIL(filename=export)
    #prof = init_profil_from(run, prof, keep_surch=True)
    prof.Set('R', {
       'type' : 'repe', 'isrep' : True, 'ul' : 0, 'compr' : False,
       'path' : '/tmp/test_param' })

    if debug: print prof
    prof.WriteExportTo( os.path.join(resudir, 'master.export') )

    # get hostrc object
    hostrc = get_hostrc(run, prof)

    # timeout before rejected a job
    timeout = get_timeout(prof)


    # list of parameters
    list_val = []

    # Dictionnaire des parametres du point courant
    dic = dict( zip( list_params, X0 ) )
    list_val.append( dic )

    # Dictionnaires des parametres des calculs esclaves (perturbations des differences finies)
    for n in range(1,len(dX)+1):
        l = [0] * len(dX)
        l[n-1] = dX[n-1]
        X = [ X0[i] + l[i] for i in range(len(dX)) ]
        dic = dict( zip( list_params, X ) )
        list_val.append( dic )

    assert is_list_of_dict(list_val)
    nbval = len(list_val)


    # Ajout des impressions de tables a la fin du .comm
    t = []
    reponses = list_calc
    for i in range(len(reponses)):
        _ul = str(int(100+i))
        num_ul = '99'

        try:    os.remove( tmp_macr_recal+os.sep+"REPE_TABLE"+os.sep+"fort."+_ul )
        except: pass

        t.append("\n# Recuperation de la table : " + str(reponses[i][0]) + "\n")
        t.append("DEFI_FICHIER(UNITE=" + num_ul + ", FICHIER='" + os.path.join('.', 'REPE_OUT', 'fort.'+_ul) + "',);\n" )
        t.append("IMPR_TABLE(TABLE="+str(reponses[i][0])+", FORMAT='ASTER', UNITE="+num_ul+", INFO=1, FORMAT_R='E30.20',);\n")
        t.append("DEFI_FICHIER(ACTION='LIBERER', UNITE="+num_ul+",);\n")


    # number of threads to follow execution
    numthread = 1

    # ----- Execute calcutions in parallel using a Dispatcher object
    # elementary task...
    task = DistribParametricTask(run=run, prof=prof, # IN
		       hostrc=hostrc,
		       nbmaxitem=0, timeout=timeout,
		       resudir=resudir, flashdir=flashdir,
		       keywords={'POST_CALCUL': '\n'.join(t)},
		       info=1,
		       nbnook=0, exec_result=[])	    # OUT
    # ... and dispatch task on 'list_tests'
    etiq = 'calc_%%0%dd' % (int(log10(nbval)) + 1)
    labels = [etiq % (i+1) for i in range(nbval)]
    couples = zip(labels, list_val)
    execution = Dispatcher(couples, task, numthread=numthread)

    iret = 0
    if task.nbnook > 0:
        iret = 4
    #run.Sortie(iret)

    # Recuperation des tables calculees
    seq_FX   = []
    seq_FY   = []
    seq_DIMS = []
    lst_DIAG = []
    lst_iter = []
    i=0
    for c in labels:
        tbl = get_tables(tables_calc=list_calc, tmp_repe_table=os.path.join(resudir, c, 'REPE_OUT'), prof=prof)
        FX = []
        FY = []
        ldims = []
        for array in tbl:
#           print 'AA1:', array
#           print array[0]
            FX.extend([ x[0] for x in array ])
            FY.extend([ x[1] for x in array ])
            ldims.append(len(array))

        # Agregation des resultats
        seq_FX.append(FX)
        seq_FY.append(FY)
        seq_DIMS.append(ldims)
        lst_iter.append(i)
        i+=1

    # Liste des diagnostics
    d_diag = {}
    for result in task.exec_result:
        label = result[0]
        diag  = result[2]
        d_diag[label] = diag
    lst_DIAG = [ d_diag[label] for label in labels]

    if debug:
        print
        print "list_calc =",list_calc
        print "seq_FX    =",seq_FX
        print "seq_FY    =",seq_FY
        print "seq_DIMS  =",seq_DIMS
        print "lst_DIAG  =",lst_DIAG
        print "lst_iter  =",lst_iter
        print "dX        =",dX
        print

    # ----------------------------------------------------------------------------
    # Procedure d'assemblage du gradient

    # Calcul maitre (point X0)
    idx0 = lst_iter.index(0)   # index (les calculs arrivent-ils dans le desordre?)
    FY_X0 = seq_FY[idx0]
    H_de_X = FY_X0

    # Arret si tous les jobs ne se sont pas deroules correctement
    for diag in lst_DIAG:
        if not diag[0:2] in ['OK', '<A']:
            raise ValueError("Au moins un calcul ne s'est pas deroule normalement")

    # Calcul du gradient (une liste de liste)
    Gradient_de_H_en_X = []

    for n in range(len(lst_iter))[1:]:
        idx = lst_iter.index(n)
        FY   = seq_FY[idx]
        col = [ -(y-x)/dX[idx-1] for x, y in zip(FY, FY_X0) ]
        Gradient_de_H_en_X.append(col)
        if debug: print 'Calcul numero: %s - Diagnostic: %s' % (n, lst_DIAG[idx])

    if debug:
        print "\nCalcul H au point X0: \n%s" % str(H_de_X)
        import pprint
        print "\nGradient au point X0:"
        pprint.pprint(Gradient_de_H_en_X)

    return Gradient_de_H_en_X

#===============================================================================
def Calcul_Aster_Adjoint( (X0, dY) ):
    #
    if 0:
        print
        print "CALCUL ADJOINT"
        print "X0 =",X0
        print "dY =",dY
    #
    import numpy
    #
    Y0 = numpy.asmatrix(dY).flatten().T
    #
    Delta_HX = Calcul_Aster_Jacobienne( X0 )
    Delta_HX = numpy.matrix( Delta_HX )
    #
    HtY = numpy.dot(Delta_HX, Y0)
    #
    if 0:
        print "dHX =",Delta_HX
        print "HtY =",HtY
        print
    #
    return HtY.A1
