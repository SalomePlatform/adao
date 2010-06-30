debug = init_data["debug"]
parametres = init_data["parametres"]

xb = []
Bornes = []
for parametre in parametres:
    xb.append( parametre[1] )
if debug:
    print
    print "Ebauche = ",xb
    print

Background = xb
