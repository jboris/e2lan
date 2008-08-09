from pila import Pila
from lexico import Lexico

class InterRI():
    def __init__(self, ri):
        self.__ri = ri
        self.__mainStack = Pila()
        self.__tabla = {}
        
    def getMainStack(self):
        return self.__mainStack
    
    def setMainStack(self, value):
        self.__mainStack = value
    
    def getTabla(self):
        return self.__tabla
        
    def setTabla(self, tabla):
        self.__tabla = tabla
        
    def getValue(self, x):
        if x["type"] == "ID":
            valor = self.__tabla[x["value"]]
            
            if valor["type"] == "Bloque":
                
                l = Lexico(valor["value"][1:-1])
                l.analizar()
                t = l.getTokens()
                #t.pop()

                t.reverse()

                inter = InterRI(t)
                
                inter.setMainStack(self.__mainStack)
                
                inter.ejecutar()
                self.__mainStack = inter.getMainStack()
                
                return self.getValue(self.__mainStack.pop())
            else:
                return self.__tabla[x["value"]]["value"]
        elif x["type"] == "Logico":
            return x["value"] == "V"
        
            
        else:
            return x["value"]
        
    def evaluar(self, x):
        if x["type"] == "ID":
            valor = self.__tabla[x["value"]]
            if valor["type"] != "Bloque":
                self.__mainStack.push(valor)
            else:
                self.evaluar(valor)
        else:
            l = Lexico(x["value"][1:-1])
            
            l.analizar()
            t = l.getTokens()
            t.reverse()

            inter = InterRI(t)
            
            inter.setMainStack(self.__mainStack)
            inter.setTabla(self.__tabla)
            
            
            
            inter.ejecutar()
            self.__mainStack = inter.getMainStack()
            self.__tabla = inter.getTabla()

    def ejecutar(self):
        while not self.__ri.empty():
            i = self.__ri.pop()
            if i["type"] == "Entero" or i["type"] == "Flotante" or \
            i["type"] == "ID" or i["type"] == "Logico" or i["type"] == "Bloque":
                self.__mainStack.push(i)
            elif i["type"] == "Op":
                if i["value"] == "+":
                     op1 = self.getValue(self.__mainStack.pop())
                     op2 = self.getValue(self.__mainStack.pop())
                     r = op2 + op1
                elif i["value"] == "-":
                     op1 = self.getValue(self.__mainStack.pop())
                     op2 = self.getValue(self.__mainStack.pop())
                     r = op2 - op1
                elif i["value"] == "*":
                     op1 = self.getValue(self.__mainStack.pop())
                     op2 = self.getValue(self.__mainStack.pop())
                     r = op2 * op1
                elif i["value"] == "/":
                     op1 = self.getValue(self.__mainStack.pop())
                     op2 = self.getValue(self.__mainStack.pop())
                     r = op2 / op1
                elif i["value"] == "%":
                     op1 = self.getValue(self.__mainStack.pop())
                     op2 = self.getValue(self.__mainStack.pop())
                     r = op2 % op1
                elif i["value"] == "==":
                     op1 = self.getValue(self.__mainStack.pop())
                     op2 = self.getValue(self.__mainStack.pop())
                     r = op2 == op1
                elif i["value"] == ">=":
                     op1 = self.getValue(self.__mainStack.pop())
                     op2 = self.getValue(self.__mainStack.pop())
                     r = op2 >= op1
                elif i["value"] == "<=":
                     op1 = self.getValue(self.__mainStack.pop())
                     op2 = self.getValue(self.__mainStack.pop())
                     r = op2 <= op1
                elif i["value"] == ">":
                     op1 = self.getValue(self.__mainStack.pop())
                     op2 = self.getValue(self.__mainStack.pop())
                     r = op2 > op1
                elif i["value"] == "<":
                     op1 = self.getValue(self.__mainStack.pop())
                     op2 = self.getValue(self.__mainStack.pop())
                     r = op2 < op1
                elif i["value"] == "!=":
                     op1 = self.getValue(self.__mainStack.pop())
                     op2 = self.getValue(self.__mainStack.pop())
                     r = op2 <> op1
                elif i["value"] == "!":
                     op1 = self.getValue(self.__mainStack.pop())
                     r = not op1
                elif i["value"] == "|":
                     op1 = self.getValue(self.__mainStack.pop())
                     op2 = self.getValue(self.__mainStack.pop())
                     r = op2 or op1
                elif i["value"] == "&":
                     op1 = self.getValue(self.__mainStack.pop())
                     op2 = self.getValue(self.__mainStack.pop())
                     r = op2 and op1
                elif i["value"] == "=":
                     op1 = self.__mainStack.pop()
                     if op1["type"] == "ID":
                        op2 = self.__mainStack.pop()
                        self.__tabla[op1["value"]] = op2
                     else:
                        print "Error de asignacion"
                        break
                     continue
                tkn = {}
                if type(r) == type(0):
                    tkn["type"] = "Entero"
                elif type(r) == type(0.0):
                    tkn["type"] = "Flotante"
                elif type(r) == type(True):
                    tkn["type"] = "Logico"
                    if r:
                        r = "V"
                    else:
                        r = "F"
                tkn["value"] = r
                self.__mainStack.push(tkn)
                
            elif i["type"] == "Res":
                if i["value"] == "EVAL":
                    op1 = self.__mainStack.pop()
                    if op1["type"] == "Bloque" or op1["type"] == "ID":
                        self.evaluar(op1)
                    else:
                        print "Error no es una variable"
                        break
                elif i["value"] == "SI":
                    cond = self.__mainStack.pop()
                    if cond["type"] == "Logico":
                        f = self.__mainStack.pop()
                        v = self.__mainStack.pop()
                        if self.getValue(cond):
                            self.evaluar(v)
                        else:
                            self.evaluar(f)
                    else:
                        print "Error SI"
                        break
                elif i["value"] == "MIENTRAS":
                    cond = self.__mainStack.pop()
                    if cond["type"] == "Bloque":
                        bloque = self.__mainStack.pop()
                        if bloque["type"] == "Bloque":
                            
                            self.evaluar(cond)
                            while self.getValue(self.__mainStack.pop()):
                                self.evaluar(bloque)
                                self.evaluar(cond)
                        else:
                            print "Error MIENTRAS"
                            break
                    else:
                        print "Error MIENTRAS"
                        break
                elif i["value"] == "IMPRIMIR":
                    v = self.__mainStack.pop()
                    print self.getValue(v)
                elif i["value"] == "LEER":
                    op = self.__mainStack.pop()
                    if op["type"] == "ID":
                        v = raw_input("%s:"%op["value"])
                        l = Lexico(s = v)
                        l.analizar()
                        t = l.getTokens()
                        t.pop()
                        if len(t) == 1:
                            op2 = t.pop()
                            self.__tabla[op["value"]] = op2
                        else:
                            print "Error LEER"
                            break
                    else:
                        print "Error LEER"
                        break
            elif i["type"] == "Error":
                print "Error", i["value"]
                break
