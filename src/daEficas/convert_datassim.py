# -*- coding: utf-8 -*-
print "import convert_datassim"

import convert.parseur_python
from convert.convert_python import *

def entryPoint():
   """
       Retourne les informations nécessaires pour le chargeur de plugins
       Ces informations sont retournées dans un dictionnaire
   """
   return {
        # Le nom du plugin
          'name' : 'datassim',
        # La factory pour créer une instance du plugin
          'factory' : PythonParser,
          }


