from lexico import Lexico
from pila import Pila
from interRI import InterRI
import sys

s = sys.argv[1]
l = Lexico(s=s)
l.analizar()
t = l.getTokens()
print t
t.reverse()

inter = InterRI(t)
inter.ejecutar()
p = inter.getMainStack()
print p
print inter.getTabla()
