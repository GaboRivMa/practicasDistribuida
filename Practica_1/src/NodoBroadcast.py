import simpy
import time
from Nodo import *
from Canales.CanalBroadcast import *

# La unidad de tiempo
TICK = 1


class NodoBroadcast(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida, mensaje=None):
	    #Aqui va tu codigo
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.mensaje = mensaje
        self.seen_message =  False 

    def broadcast(self, env):
        ''' Algoritmo de Broadcast. Desde el nodo distinguido (0)
            vamos a enviar un mensaje a todos los demás nodos.'''
        #3
        if self.id_nodo == 0:
            #4
            self.seen_message = True
            self.mensaje = "MENSAJE"
            #5
            if self.vecinos:
                self.canal_salida.envia(("BROADCAST", self.mensaje), self.vecinos)
                yield env.timeout(TICK)
        #7
        while True:
            mensaje = yield self.canal_entrada.get()
            tipo_mensaje, mensaje_recibido = mensaje 

            #8
            if tipo_mensaje == "BROADCAST" and not self.seen_message:
                #9
                self.seen_message = True
                #10
                self.mensaje = mensaje_recibido
                if self.vecinos:
                    self.canal_salida.envia(("BROADCAST", self.mensaje), self.vecinos)
                    yield env.timeout(TICK)
        




