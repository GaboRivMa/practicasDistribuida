import simpy
from Canales.Canal import Canal


class CanalComuniacion(Canal):

    def __init__(self,env,capacidad =simpy.core.Infinity):
        self.env = env  
        self.capacidad = capacidad 
        self.canales = []

    def get_canales(self):
        return self.canales
    
    def envia(self,mensaje,vecinos):
        if not self.canales :
            raise RuntimeError ("No hay canales disponibles")
        #Eventos  
        eventos = []
        for vecino in vecinos : 
            if vecino in range(len(self.canales)):
                eventos.append(self.canales[vecino].put(mensaje))

    
    def crea_canal_entrada (self):
        canal_entrada = simpy.Store(self.env,capacity = self.capacidad)
        self.canales.append(canal_entrada)
        return canal_entrada

        

