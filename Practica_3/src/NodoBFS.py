import simpy
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1
#Declaro los mensajes
START_MSG = "START"
GO_MSG = "GO"
BACK_MSG = "BACK"


class NodoBFS(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo BFS. '''
        super().__init__(id_nodo, vecinos, canal_entrada, canal_salida)
        self.padre = None
        self.hijos = []
        self.distancia = 0
        self.mensajes_esperados = 0

    def bfs(self, env):
        ''' Algoritmo BFS. '''
        #Simulamos START
        if self.id_nodo == 0:
            msg = (START_MSG, 0, None, -1)
            self.canal_entrada.put(msg)

        while(True):
            mensaje = yield self.canal_entrada.get()

            tipo_msg = mensaje[0]
            j = mensaje[1]
            resp = mensaje[2]
            d = mensaje[3]

            if tipo_msg == START_MSG:
                msg = (GO_MSG, self.id_nodo, None, -1)
                self.canal_salida.envia(msg, [self.id_nodo])
                yield env.timeout(TICK)

            elif tipo_msg == GO_MSG:
                if self.padre == None:
                    self.padre = j
                    self.hijos = []
                    self.distancia = d+1
                    nuevo_vecinos = [v for v in self.vecinos if v!=j]
                    self.mensajes_esperados = len(nuevo_vecinos)
                    if self.mensajes_esperados == 0:
                        msg = (BACK_MSG, self.id_nodo, "YES", d+1)
                        self.canal_salida.envia(msg, [self.padre])
                        yield env.timeout(TICK)
                    else:
                        msg = (GO_MSG, self.id_nodo, None, d+1)
                        self.canal_salida.envia(msg, nuevo_vecinos)
                        yield env.timeout(TICK) 
                elif self.distancia > d+1:
                    self.padre = j
                    self.hijos = []
                    self.distancia = d+1
                    nuevo_vecinos = [v for v in self.vecinos if v!=j]
                    self.mensajes_esperados = len(nuevo_vecinos)
                    if self.mensajes_esperados == 0:
                        msg = (BACK_MSG, self.id_nodo, "YES", d+1)
                        self.canal_salida.envia(msg, [self.padre])
                        yield env.timeout(TICK)
                    else:
                        msg = (GO_MSG, self.id_nodo, None, d+1)
                        self.canal_salida.envia(msg, nuevo_vecinos)
                        yield env.timeout(TICK) 
                else:
                    msg = (BACK_MSG, self.id_nodo, "NO", d+1)
                    self.canal_salida.envia(msg, [j])
                    yield env.timeout(TICK)


            elif tipo_msg == BACK_MSG:
                if d == self.distancia+1:
                    if resp == "YES":
                        self.hijos.append(j)
                    self.mensajes_esperados -= 1
                    if self.mensajes_esperados == 0:
                        if self.padre != self.id_nodo:
                            msg = (BACK_MSG, self.id_nodo, "YES", self.distancia)
                            self.canal_salida.envia(msg, [self.padre])
                            yield env.timeout(TICK)
                        else:
                            continue