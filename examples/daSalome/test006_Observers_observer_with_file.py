# -*- coding: utf-8 -*-
print("  ---> observerState")
print("       var  =",var[-1])
print("       info =",info)
#
import Gnuplot
import os

try:
  numero
except NameError:
  numero = 0

gp = Gnuplot.Gnuplot()
gp('set style data lines')
gp('set title  "'+str(info)+'"')
gp.plot( Gnuplot.Data( var[-1] ) )

filename = os.path.join("/tmp", "imageState_%02i.ps"%numero)
print("       imageState \"%s\""%filename)

gp.hardcopy(filename=filename, color=1)
numero += 1
