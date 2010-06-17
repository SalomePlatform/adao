#-*-coding:iso-8859-1-*-
#
# Script à lancer avec l'environnement ASTER+SALOME4 surchargé par SALOME5.Dev
# ----------------------------------------------------------------------------

from N_Code_Aster_dist import Calcul_Aster_Ponctuel
from N_Code_Aster_dist import Calcul_Aster_Jacobienne
from N_Code_Aster_dist import Calcul_Aster_Adjoint

Point_courant = [ 80000.,  1000., 30. ]
Experience    = 22*[1.]

HX       = Calcul_Aster_Ponctuel( Point_courant )

Delta_HX = Calcul_Aster_Jacobienne( Point_courant )

HtY      = Calcul_Aster_Adjoint( ( Point_courant, Experience) )

print
print "HX       =", HX
print
print "Delta_HX =", Delta_HX
print
print "HtY      =", HtY
print 
