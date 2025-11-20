import simpy
from Nodo import *
from Canales.CanalRecorridos import *
from random import randint

#Unidad de tiempo
TICK = 1

class NodoBroadcast(Nodo):
    def __init__(self, id_nodo: int, vecinos: list, canal_entrada: simpy.Store,
                 canal_salida: simpy.Store):
        super().__init__(id_nodo,vecinos,canal_entrada,canal_salida)
        self.mensaje = None
        self.reloj = 0
        self.eventos = []

    def broadcast(self, env: simpy.Environment, data="Mensaje"):
        #Tu implementacion va aqui
        if not hasattr(self, "seen_messafe"):
            self.seen_message = False
        
        if self.id_nodo == 0:
            self.seen_message = True
            self.mensaje = data
            self.reloj += 1

            for vecino in self.vecinos:
                retraso = randint(1,3)*TICK
                yield env.timeout(retraso)
                self.reloj += 1
                msg = ["BROADCAST", self.mensaje, self.reloj, self.id_nodo]
                self.canal_salida.envia(msg, [vecino])
                evento = [self.reloj, 'E', self.mensaje, self.id_nodo, vecino]
                self.eventos.append(evento)

        #7
        while True:
            message = yield self.canal_entrada.get()
            tipo_mensaje, info_mensaje, reloj_mensaje, emisor_mensaje = message 

            if tipo_mensaje == "BROADCAST" and not self.seen_message:
                self.reloj = max(self.reloj, reloj_mensaje) + 1
                self.seen_message = True
                self.mensaje = info_mensaje
                evento = [self.reloj, 'R', info_mensaje, emisor_mensaje, self.id_nodo]
                self.eventos.append(evento)

                for vecino in self.vecinos:
                    if vecino != emisor_mensaje:
                        retraso = randint(1,3)*TICK
                        yield env.timeout(retraso)
                        self.reloj += 1
                        msg = ["BROADCAST", self.mensaje, self.reloj, self.id_nodo]
                        self.canal_salida.envia(msg, [vecino])
                        evento = [self.reloj, 'E', self.mensaje, self.id_nodo, vecino]
                        self.eventos.append(evento)