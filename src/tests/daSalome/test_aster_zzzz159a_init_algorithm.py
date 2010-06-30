debug = init_data["debug"]
parametres = init_data["parametres"]

Bornes = []
for parametre in parametres:
    Bornes.append(parametre[2:4])

if debug:
    print
    print "Bornes  = ",Bornes
    print

AlgorithmParameters = { "Minimizer"           : "TNC",
    "Bounds"              : Bornes,
    }
