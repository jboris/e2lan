from pila import Pila

class Lexico():
    def __init__(self, s=""):
        self.__tokens = Pila()
        self.__string = s + " "
        self.__busqueda = -1
        self.__actual = 0
    
    def getTokens(self):
        return self.__tokens
    
    def dame(self):
        self.__busqueda += 1
        if self.__busqueda >= len(self.__string):
            return ""
        else:
            return self.__string [self.__busqueda]
        
    def falla(self):
        self.__busqueda = self.__actual - 1
        
    def retraer(self):
        self.__busqueda -= 1
        
    def aceptar(self):
        self.__actual = self.__busqueda + 1
        
    def getValor(self):
        return self.__string[self.__actual:self.__busqueda]
        
    def instalar(self, tipo, valor):
        tkn = {}
        tkn["type"] = tipo
        tkn["value"] = valor
        if tipo == "ID":
            if valor == "V" or valor == "F":
                tkn["type"] = "Logico"
            elif valor == "EVAL" or valor == "SI" or valor == "MIENTRAS"\
             or valor == "IMPRIMIR" or valor == "LEER":
                tkn["type"] = "Res"
        self.__tokens.push(tkn)
            
    def esLetra(self, x):
        return "a" <= x <= "z" or "A" <= x <= "Z" or x == "_"
    
    def esDigito(self, x):
        return "0" <= x <= "9"
        
    def esOperadorMatematico(self, x):
        return x in ['+', '-', '*', '/', '%','=', '!', '>', '<', '|', '&']
        
    def esEspacio(self, x):
        return x in [" ", "\n"]
    
    def esSigno(self, x):
        return x in ['+', '-']
        
    def esDesconocido(self, x):
        return not (self.esDigito(x) or self.esOperadorMatematico(x) or \
        self.esEspacio(x) or x == "" or self.esLetra(x) or self.esSigno(x) \
        or x ==":" or x == ";")
        
    def analizar(self):
        while self.__actual < len(self.__string):
            c = self.dame()
            if c == ":":
                
                cont = True
                b = 1
                while cont:
                    
                    c = self.dame()
                    if c == ":":
                        
                        b += 1
                    elif c == ";":
                        
                        b -= 1
                        
                    if b == 0:
                        
                        cont = False
                        self.dame()
                        self.instalar("Bloque", self.getValor())
                        self.retraer()
                        self.aceptar()
                    
            else:
                self.falla()
            
            c = self.dame()
            if self.esDigito(c) or self.esSigno(c):
                if self.esSigno(c):
                    c = self.dame()
                if self.esDigito(c):
                        while self.esDigito(c):
                            c = self.dame()
                        if c == ".":
                            c = self.dame()
                            if self.esDigito(c):
                                while self.esDigito(c):
                                    c = self.dame()
                            self.instalar("Flotante", float(self.getValor()))
                            self.retraer()
                            self.aceptar()
                        else:
                            self.instalar("Entero", int(self.getValor()))
                            self.retraer()
                            self.aceptar()
                else:
                        self.falla()
            else:
                self.falla()
            
            c = self.dame()
            if self.esLetra(c):
                while self.esLetra(c) or self.esDigito(c):
                    c = self.dame()
                self.instalar("ID", self.getValor())
                self.retraer()
                self.aceptar()
            else:
                self.falla()
            c = self.dame()
            if self.esOperadorMatematico(c):
                while self.esOperadorMatematico(c):
                    c = self.dame()
                self.instalar("Op", self.getValor())
                self.retraer()
                self.aceptar()
            else:
                self.falla()
                
            c = self.dame()
            if self.esEspacio(c):
                while self.esEspacio(c):
                    c = self.dame()
                self.retraer()
                self.aceptar()
            else:
                self.falla()
                
            c = self.dame()
            if c == "":
                self.instalar("Fin", "")
                
            else:
                self.falla()
                
            c = self.dame()
            if self.esDesconocido(c):
                self.instalar("Error", "%s -> %d"%(c, self.__busqueda))
                self.aceptar()
            else:
                self.falla()

