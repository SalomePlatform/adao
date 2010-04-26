#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
   Ce module sert à lancer EFICAS pour Datassim
"""
# Configuration
import prefs
import prefs_DATASSIM

# Modules Eficas
import sys
from InterfaceQT4 import eficas_go
eficas_go.lance_eficas(code=prefs.code)
