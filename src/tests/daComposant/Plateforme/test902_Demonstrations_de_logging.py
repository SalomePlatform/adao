#-*-coding:iso-8859-1-*-
__doc__ = """
    Cas-test démontrant les possibilités de logging, sous la forme de fonctions
    successives illustrant le fonctionnement par défaut.
"""
__author__ = "Jean-Philippe ARGAUD - Octotbre 2008"

import os
execfile("context.py")

#===============================================================================
def demo1():
    from AssimilationStudy import AssimilationStudy
    print """
 DEMO 1
 ------
 L'initialisation de l'environnement de logging a été automatiquement faite à
 l'import de AssimilationStudy.
 
 Seuls les messages d'un niveau au moins égal à warning sont disponibles par
 défaut. Cela permet de truffer le code de messages de DEBUG ou d'INFO sans
 qu'ils apparaissent à l'affichage standard.
"""
    import logging
    logging.debug("Un message de debug")
    logging.info("Un message d'info")
    logging.warning("Un message d'avertissement")
    logging.error("Un message d'erreur")
    logging.critical("Un message critique")

def demo2():
    from AssimilationStudy import AssimilationStudy
    print """
 DEMO 2
 ------
 On recommence le cas précédent, mais en affichant tous les messages. Cela
 permet de deboguer le code en ayant les messages non affichés précédemment.
 
 La commande de disponibilité de tous les niveaux est atteignable à travers le
 module standard "logging" (avec une minuscule) :
   logging.getLogger().setLevel(...)
"""
    import logging
    
    logging.getLogger().setLevel(logging.DEBUG)
    
    logging.debug("Un message de debug")
    logging.info("Un message d'info")
    logging.warning("Un message d'avertissement")
    logging.error("Un message d'erreur")
    logging.critical("Un message critique")

def demo3():
    print """
 DEMO 3
 ------
 On peut disposer des messages conjointement à la console et dans un fichier.

 Pour cela, il faut importer le module Logging n'importe où (après le module
 AssimilationStudy ou en son absence, mais pas avant). On en profite aussi pour
 initier le logging général avec le niveau INFO, donc le message de debug
 précédemment affiché ne l'est plus.
 
"""
    import Logging
    Logging.Logging().setLogfile()
    
    if os.path.isfile("AssimilationStudy.log"):
        print " ---> Le fichier attendu a bien été créé."
    else:
        raise ValueError("Le fichier attendu n'a pas été créé.")
    
    import logging
    logging.getLogger().setLevel(logging.INFO)
    
    logging.debug("Un message de debug")
    logging.info("Un message d'info")
    logging.warning("Un message d'avertissement")
    logging.error("Un message d'erreur")
    logging.critical("Un message critique")
    
    print
    print " On peut vérifier le contenu du fichier \"AssimilationStudy.log\"."

#===============================================================================
if __name__ == "__main__":

    print
    print "AUTODIAGNOSTIC"
    print "=============="
    
    demo1()
    demo2()
    demo3()
    print
    print " Pour les autres modes avancés de contôle du fichier et des niveaux"
    print " on se reportera à la documentation du module \"Logging\"."
    print
