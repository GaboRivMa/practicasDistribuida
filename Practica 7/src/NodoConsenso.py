import simpy
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1

class NodoConsenso(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Consenso.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo de consenso. '''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        # Atributos extra
        self.V = [None] * (len(vecinos) + 1) # Llenamos la lista de Nodos
        self.V[id_nodo] = id_nodo
        self.New = set([(id_nodo, id_nodo)]) #Se modifico para tener el nodo propuesto y el nodo que los envia
        self.rec_from = [None] * (len(vecinos) + 1)
        self.fallare = False      # Colocaremos esta en True si el nodo fallará
        self.lider = None         # La elección del lider.

    def consenso(self, env, f):
        '''El algoritmo de consenso.'''
        # Aquí va su implementación
        if self.id_nodo < f:
            self.fallare = True
        
        for ronda in range(1, f+2):
            #Revisamos si el nodo falla
            if self.fallare:
                yield env.timeout(TICK)
                continue

            if len(self.New) > 0:
                #Si New es no vacía entonces se propaga
                for j in self.vecinos:
                    self.canal_salida.envia((self.id_nodo, self.New.copy()), [j])

            yield env.timeout(TICK)

            for j in range(len(self.rec_from)):
                self.rec_from[j] = set()


            #Recibimos los mensajes durante la ronda
            mensajes_recibidos = []

            while len(self.canal_entrada.items) > 0:
                try:
                    mensaje = yield self.canal_entrada.get()
                    mensajes_recibidos.append(mensaje)
                except simpy.Interrupt:
                    break

            for mensaje in mensajes_recibidos:
                id_remitente, mensajes = mensaje
                if id_remitente < len(self.rec_from):
                    self.rec_from[id_remitente] = mensajes.copy()

            self.New = set()
            for j in self.vecinos:
                for (v,k) in self.rec_from[j]:
                    if k < len(self.V) and self.V[k] is None:
                        self.V[k] = v
                        self.New.add((v,k))
            yield env.timeout(TICK)

        #Cuando terminan las rondas
        v_decision = None
        for valor in self.V:
            if valor is not None:
                v_decision = valor
                break
        self.lider = v_decision
        return self.lider
