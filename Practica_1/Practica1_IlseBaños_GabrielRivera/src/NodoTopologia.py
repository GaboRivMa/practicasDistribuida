import simpy
import time
from Nodo import *
from Canales.CanalBroadcast import *


# La unidad de tiempo
TICK = 1


class NodoTopologia(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida, mensaje=None):
	    #Aqui va tu codigo
        self.id_nodo =  id_nodo 
        self.vecinos =  vecinos  # Vecinos del proceso
        self.canal_entrada = canal_entrada 
        self.canal_salida = canal_salida 
        self.mensaje = mensaje
        self.proc_conocidos =  {self.id_nodo}
        self.canales_conocidos =  {(self.id_nodo,y)  for y in self.vecinos }


    def topologia(self, env):
        #Aqui va tu codigo

        #4-6
        for vecino in self.vecinos:
            mensaje = ("POSITION", self.id_nodo, self.vecinos)
            self.canal_salida.envia(mensaje, [vecino])

        #7
        while True:
            (tipo_mensaje, k, vecinos_k) = yield self.canal_entrada.get()
            if tipo_mensaje == "POSITION":
                #8
                if k not in self.proc_conocidos:
                    #9
                    self.proc_conocidos.add(k)
                    #10
                    for i in vecinos_k:
                        self.canales_conocidos.add((k,i))

                    #11-13
                    for i in self.vecinos:
                        mensaje_reenviar = ("POSITION", k, vecinos_k)
                        self.canal_salida.envia(mensaje_reenviar, [i])

                #14-16
                if all((l in self.proc_conocidos and m in self.proc_conocidos) for(l,m) in self.canales_conocidos):
                    print(f"El nodo {self.id_nodo} conoce la gráfica de comunicación.")
                    break

                yield env.timeout(1)







            
    
    
