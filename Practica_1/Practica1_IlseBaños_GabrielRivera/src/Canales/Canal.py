import simpy

class Canal():
    '''
    Interfaz que modela el comportamiento que cualquier canal debe tomar.
    '''
    def __init__(self, env: simpy.Environment, capacidad):
        '''Constructor de la clase. Se debe inicializar la lista de objetos Store al
        ser creado un canal.
        '''
        self.env = env
        self.capacidad = capacidad
        self.canales = []

    def envia(self, mensaje, vecinos):
        '''
        Envia un mensaje a los canales de entrada de los vecinos.
        '''
        if not self.canales:
            raise RuntimeError("No hay canales disponibles")
        eventos = []

        for vecino in vecinos:
            if vecino in range(len(self.canales)):
                eventos.append(self.canales[vecino].put(mensaje))

    def crea_canal_de_entrada(self):
        '''
        Creamos un objeto Store en el un nodo recibirá los mensajes.
        '''
        canal_entrada = simpy.Store(self.env, capacity = self.capacidad)
        self.canales.append(canal_entrada)
        return canal_entrada

    def get_canales(self):
        '''
        Regresa la lista con los canales
        '''
        return self.canales