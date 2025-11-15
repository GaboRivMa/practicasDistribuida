import simpy
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1
#Declaro los mensajes
START_MSG = "START"
GO_MSG = "GO"
BACK_MSG = "BACK"

class NodoDFS(Nodo):

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo DFS. '''
        # Tu implementación va aquí
        super().__init__(id_nodo, vecinos, canal_entrada, canal_salida)
        self.padre = None
        self.hijos = []
        self.completed_children = set()



    def dfs(self, env):
        ''' Algoritmo DFS. '''
        #Simular START
        if self.id_nodo == 0:
            msg = (START_MSG, 0, None)
            self.canal_entrada.put(msg)

        while(True):
            mensaje = yield self.canal_entrada.get()

            tipo_msg = mensaje[0]
            j = mensaje[1]
            resp = mensaje[2]

            if tipo_msg == START_MSG:
                self.padre = self.id_nodo
                self.hijos = []
                self.completed_children = set()
                msg = (GO_MSG, self.id_nodo, None)
                self.canal_salida.envia(msg, [self.vecinos[0]])
                yield env.timeout(TICK)

            elif tipo_msg == GO_MSG:
                if self.padre == None:
                    self.padre = j
                    self.hijos = []
                    self.completed_children = {j}
                    if self.completed_children == set(self.vecinos) :
                        msg = (BACK_MSG, self.id_nodo, "YES")
                        self.canal_salida.envia(msg, [self.padre])
                        yield env.timeout(TICK)
                    else:
                        nuevo_vecinos = [k for k in self.vecinos if k not in self.completed_children]
                        msg = (GO_MSG, self.id_nodo, None)
                        self.canal_salida.envia(msg, [nuevo_vecinos[0]])
                        yield env.timeout(TICK)
                else:
                    msg = (BACK_MSG, self.id_nodo, "NO")
                    self.canal_salida.envia(msg, [j])
                    yield env.timeout(TICK)

            elif tipo_msg == BACK_MSG:
                if resp == "YES":
                    self.hijos.append(j)
                self.completed_children.add(j)
                if self.completed_children == set(self.vecinos): 
                    if self.padre == self.id_nodo:
                        return
                    else:
                        msg = (BACK_MSG, self.id_nodo, "YES")
                        self.canal_salida.envia(msg, [self.padre])
                        yield env.timeout(TICK)
                else:
                    nuevo_vecinos = [k for k in self.vecinos if k not in self.completed_children]
                    msg = (GO_MSG, self.id_nodo, None)
                    self.canal_salida.envia(msg, [nuevo_vecinos[0]])
                    yield env.timeout(TICK)
        # Tu implementación va aquí