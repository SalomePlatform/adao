#-*-coding:iso-8859-1-*-
import numpy
debug = init_data["debug"]
experience = init_data["experience"]

nbmesures = 11 # De 0 à 1 par pas de 0.1
instants = numpy.array([0.1*i for i in range(nbmesures)])
yo = []
for reponse in experience:
    for t,v in list(reponse):
        if min(abs(t - instants)) < 1.e-8:
            yo.append(v)
            # print t,'===>',v
if debug:
    print "Observations = ",yo
    print

Observation = yo
