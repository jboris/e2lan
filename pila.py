#!/usr/bin/env python
#-*- coding:utf-8 -*-
################################################################################
# Archivo:      pila.py                                                        #
# Programa:     Pila                                                           #
# Fecha:        2008-07-24                                                     #
# Autor:        José Boris Bellido Santa María (jboris)                        #
# Descripción:  Implementación de una pila                                     #
# Versión:      0.0.0.1                                                        #
################################################################################

class Pila():

    def __init__(self):
        self._elementos = []
    
    def push(self, x):
        self._elementos.append(x)
        
    def empty(self):
        return self._elementos == []
        
    def pop(self):
        if self.empty():
            raise "Pila vacia"
        else:
            return self._elementos.pop()
            
    def viewtop(self):
        i = self.pop()
        self.push(i)
        return i
        
    def reverse(self):
        self._elementos.reverse()
        
    def __len__(self):
        return len(self._elementos)
    
    def __str__(self):
        s = ""
        c = len(self._elementos)
        for i in self._elementos:
            s += str(c) + ": " + str(i) + "\n"
            c -= 1
        return s
