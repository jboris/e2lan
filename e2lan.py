#!/usr/bin/env python

from lexico import Lexico
from pila import Pila
from interRI import InterRI
import sys

if __name__ == '__main__':
    archivo = sys.argv[1]
    f = file(archivo,"r").readlines()
    s = "".join(f)
    l = Lexico(s=s)
    l.analizar()
    t = l.getTokens()
    t.reverse()
    inter = InterRI(t)
    inter.ejecutar()
    p = inter.getMainStack()
