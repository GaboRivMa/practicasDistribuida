import simpy
from Nodo import *
from Canales.CanalBroadcast import *

TICK = 1
GO_MSG = "GO"
BACK_MSG = "BACK"

class NodoGenerador(Nodo):
    '''Implementa la interfaz de Nodo para el algoritmo de flooding.'''
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        '''Inicializamos el nodo.'''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        
        # Atributos propios del algoritmo
        #self.padre = None if id_nodo != 0 else id_nodo # Si es el nodo distinguido, el padre es el mismo 
        self.padre = None
        self.hijos = []
        self.mensajes_esperados = len(self.vecinos) # Cantidad de mensajes que esperamo

    def tostring(self):
        return f"ID: {self.id_nodo}, Parent: {self.padre}, Children: {self.hijos}"

    
    def genera_arbol(self, env):
    #Tu código aquí
        if self.id_nodo == 0:
            self.padre = self.id_nodo
            self.mensajes_esperados = len(self.vecinos)
            mensaje = (GO_MSG, self.id_nodo, None)
            self.canal_salida.envia(mensaje, self.vecinos)
            yield env.timeout(TICK)

        while(True):
            msg = yield self.canal_entrada.get()
            tipo = msg[0]
            remitente = msg[1]
            valor = msg[2]

            if tipo == GO_MSG:
                if self.padre is None:
                    self.padre = remitente
                    self.mensajes_esperados = len(self.vecinos)-1

                    if self.mensajes_esperados == 0:
                        mensaje = (BACK_MSG, self.id_nodo, self.id_nodo)
                        self.canal_salida.envia(mensaje, [self.padre])
                        yield env.timeout(TICK)
                    else:
                        nuevo_vecinos = [v for v in self.vecinos if v!=remitente]
                        mensaje = (GO_MSG, self.id_nodo, None)
                        self.canal_salida.envia(mensaje, nuevo_vecinos)
                        yield env.timeout(TICK)
                else:
                    mensaje = (BACK_MSG, self.id_nodo, None)
                    self.canal_salida.envia(mensaje, [remitente])
                    yield env.timeout(TICK)

            elif tipo == BACK_MSG:  
                self.mensajes_esperados -= 1
                if valor is not None:
                    self.hijos.append(remitente)
                if self.mensajes_esperados == 0:
                    if self.padre != self.id_nodo:
                        mensaje = (BACK_MSG, self.id_nodo, self.id_nodo)
                        self.canal_salida.envia(mensaje, [self.padre])
                        yield env.timeout(TICK)


        
        print("codigo")
        



                    
                    





                    







                


