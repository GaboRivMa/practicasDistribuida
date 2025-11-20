import simpy
from Nodo import *
from Canales.CanalRecorridos import *
from random import randint

TICK = 1

class NodoDFS(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida, num_nodos):
        ''' Constructor de nodo que implemente el algoritmo DFS. '''
        super().__init__(id_nodo, vecinos, canal_entrada, canal_salida)
        self.padre = None
        self.hijos = []
        self.eventos = []
        self.reloj = [0] * num_nodos
        self.num_nodos = num_nodos
        self.completed_children = set()

    def aumenta_reloj(self):
        self.reloj[self.id_nodo] += 1

    def actualiza_reloj(self, reloj):
        for i in range(len(self.reloj)):
            self.reloj[i] = max(self.reloj[i], reloj[i])

    def registra_evento(self, tipo, mensaje, emisor, receptor):
        self.eventos.append((self.reloj.copy(), tipo, mensaje, emisor, receptor))

    def dfs(self, env):
        ''' Algoritmo DFS. '''

        if self.id_nodo == 0:
            self.padre = self.id_nodo
            self.hijos = []
            self.completed_children = set()


            if self.vecinos:
                k = self.vecinos[0]
                self.completed_children.add(k)
                self.aumenta_reloj()
                msg = ("GO", None, self.id_nodo)
                self.registra_evento('E', msg, self.id_nodo, k)
                yield env.timeout(TICK)
                yield self.canal_salida.envia({"tipo":"GO", "emisor":self.id_nodo, "receptor":k, "reloj":self.reloj.copy()}, [k])

        
        while True:
            mensaje = yield self.canal_entrada.get()
            self.actualiza_reloj(mensaje["reloj"])
            self.aumenta_reloj()
            msg = (mensaje["tipo"], mensaje.get("resp"), mensaje["emisor"])
            self.registra_evento('R', msg, mensaje["emisor"], self.id_nodo)

            j = mensaje["emisor"]
            
            if mensaje["tipo"] == "GO":
                if self.padre is None:
                    self.padre = j
                    self.completed_children.add(j)
                    nuevos_vecinos = [v for v in self.vecinos if v not in self.completed_children]

                    if not nuevos_vecinos:
                        self.aumenta_reloj()
                        msg = ("BACK", "yes", self.id_nodo)
                        self.registra_evento('E', msg, self.id_nodo, self.padre)
                        yield env.timeout(TICK)
                        yield self.canal_salida.envia({"tipo":"BACK", "emisor":self.id_nodo, "receptor":self.padre, "resp":"yes", "reloj": self.reloj.copy()}, [self.padre])

                    else:
                        k = nuevos_vecinos[0]
                        self.completed_children.add(k)
                        self.aumenta_reloj()
                        msg = ("GO", None, self.id_nodo)
                        self.registra_evento('E', msg, self.id_nodo, k)
                        yield env.timeout(TICK)
                        yield self.canal_salida.envia({"tipo":"GO", "emisor":self.id_nodo, "receptor":k, "reloj":self.reloj.copy()}, [k])

                else:
                    self.aumenta_reloj()
                    msg = ("BACK", "no", self.id_nodo)
                    self.registra_evento('E', msg, self.id_nodo, j)
                    yield env.timeout(TICK)
                    yield self.canal_salida.envia({"tipo":"BACK", "emisor":self.id_nodo, "receptor":j, "resp":"no", "reloj":self.reloj.copy()}, [j])
            
            elif mensaje["tipo"] == "BACK":
                resp = mensaje["resp"]
                if resp == "yes":
                    self.hijos.append(j)

                self.completed_children.add(j)

                nuevos_vecinos = [v for v in self.vecinos if v not in self.completed_children]

                if not nuevos_vecinos:
                    if self.padre == self.id_nodo:
                        return
                    
                    self.aumenta_reloj()
                    msg = ("BACK", "yes", self.id_nodo)
                    self.registra_evento('E', msg, self.id_nodo, self.padre)
                    yield env.timeout(TICK)
                    yield self.canal_salida.envia({"tipo": "BACK", "emisor":self.id_nodo, "receptor":self.padre, "resp":"yes", "reloj":self.reloj.copy()}, [self.padre])

                else:
                    k = nuevos_vecinos[0]
                    self.completed_children.add(k)

                    self.aumenta_reloj()
                    msg = ("GO", None, self.id_nodo)
                    self.registra_evento('E', msg, self.id_nodo, k)
                    yield env.timeout(TICK)
                    yield self.canal_salida.envia({"tipo":"GO", "emisor":self.id_nodo, "receptor":k, "reloj":self.reloj.copy()}, [k])
