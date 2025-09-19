import simpy
from Nodo import *
from Canales.CanalBroadcast import *
from Auxiliares import *


TICK = 1
class NodoSort(Nodo):
    def __init__(self, id_nodo,vecinos,cantidad_nodos,canal_entrada, canal_salida,mensaje=None):
        '''Inicializamos el nodo.'''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.cantidad_nodos =  cantidad_nodos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.arr = []

    def ordernar(self,env,arr):
        '''Implementar'''
        
        self.arr = arr
        p = self.cantidad_nodos
        
        #Algorimto para coordinador
        if self.id_nodo == 0: 
            partes = cuadricula(arr, p)

            for i in range(1, p):
                #send(i,Ai)
                yield env.timeout(TICK)
                self.canal_salida.envia(("WORK", partes[i]), [i])

            arr_0 = partes[0]
            arr_0.sort()

            # Arreglo con arreglos para k-merge
            arr_aux = [arr_0]  

            for i in range (1, p):
                #recv(i,Ai)
                orden, arr_i = yield self.canal_entrada.get()
                if orden == "DONE":
                    arr_aux.append(arr_i)

            resultado = k_merge(arr_aux)
            self.arr = resultado
                
        #Algorimto para trabajador        
        else:
            #recv(0,A)
            orden, arr_trabajo = yield self.canal_entrada.get()
            if orden == "WORK":
                #sort(A)
                arr_trabajo.sort()
                #send(0,A)
                yield env.timeout(TICK)
                self.canal_salida.envia(("DONE", arr_trabajo), [0])
