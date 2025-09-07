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
        super().__init__(id_nodo, vecinos, canal_entrada, canal_salida)
        self.mensaje = mensaje
        self.seen_message =  False 

    def broadcast(self, env):
        ''' Algoritmo de Broadcast. Desde el nodo distinguido (0)
            vamos a enviar un mensaje a todos los demás nodos.'''
        #Aqui va tu codigo
        while True:
            #3
            if self.id_nodo == 0:
                #4
                self.seen_message = True
                #5
                self.canal_salida.envia(("MESSAGE", self.mensaje), self.vecinos)

            #7
            message = yield self.canal_entrada.get()
            tipo_mensaje, mensaje_recibido = message

            #8
            if not self.seen_message:
                #9
                self.seen_message = True
                #10
                self.canal_salida.envia(message, self.vecinos)

            yield env.timeout(TICK)
        




