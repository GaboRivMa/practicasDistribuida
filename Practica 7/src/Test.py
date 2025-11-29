import random
from Canales.CanalRecorridos import *
from NodoConsenso import *

TIEMPO_DE_EJECUCION = 50

def grafica_random(n):
    limite_n_random = random.randint(2, n)
    adyacencias_aleatorias =  [[j for j in range(0,limite_n_random) if i != j] for i in range(limite_n_random)]
    return adyacencias_aleatorias

class TestPractica2:
    ''' Clase para las pruebas unitarias de la práctica 2. '''
    

    # Las aristas de adyacencias de la gráfica.
    adyacencias = [[1, 2, 3, 4, 5, 6], [0, 2, 3, 4, 5, 6], [0, 1, 3, 4, 5, 6],
                   [0, 1, 2, 4, 5, 6], [0, 1, 2, 3, 5, 6], [0, 1, 2, 3, 4, 6],
                   [0, 1, 2, 3, 4, 5]]
    
     #Grafica de al menos 2 nodos y maximo de 10
    nodos_random = 10 #Valor maximo
    adyacencias_random =  grafica_random(nodos_random + 1)
    cantidad_nodos = len(adyacencias_random)


    def test_ejercicio_uno(self):
        ''' Método que prueba el algoritmo de consenso. '''
        # Creamos el ambiente y el objeto Canal
        env = simpy.Environment()
        bc_pipe = CanalRecorridos(env)

        # La lista que representa la gráfica
        grafica = []

        # Creamos los nodos
        for i in range(0, len(self.adyacencias)):
            grafica.append(NodoConsenso(i, self.adyacencias[i],
                                        bc_pipe.crea_canal_de_entrada(), bc_pipe))

        # Le decimos al ambiente lo que va a procesar ...
        #f = 2 # El número de fallos
        f = 2
        for nodo in grafica:
            env.process(nodo.consenso(env, f))
        # ...y lo corremos
        env.run(until=TIEMPO_DE_EJECUCION)

        nodos_fallidos = 0
        lider_elegido = None
        for i in range(0, len(grafica)):
            nodo = grafica[i]
            print("Id: ",nodo.id_nodo," valores: ",nodo.V)
            if nodo.fallare:
                nodos_fallidos += 1
            else:
                #print("Nodo lider : ", nodo.lider)
                lider_elegido = nodo.lider if lider_elegido is None else lider_elegido
                #print("Lider elegido, ",lider_elegido)
                assert lider_elegido == nodo.lider , ("Fallo en primera prueba") 
                #print("Nodo lider : ",nodo.lider," Output: ",  next(item for item in nodo.V if item is not None))
                assert nodo.lider == next(item for item in nodo.V if item is not None) ,("Fallo en segunda prueba")
                
        #print("Nodos fallidos: ",nodos_fallidos," F: ",f)
        assert nodos_fallidos == f , ("Tercer fallo")
        
        
    
    def test_f_0(self):
        ''' Método que prueba el algoritmo de consenso con F =  0. '''
        # Creamos el ambiente y el objeto Canal
        env = simpy.Environment()
        bc_pipe = CanalRecorridos(env)

        # La lista que representa la gráfica
        grafica = []

        # Creamos los nodos
        for i in range(0, len(self.adyacencias)):
            grafica.append(NodoConsenso(i, self.adyacencias[i],
                                        bc_pipe.crea_canal_de_entrada(), bc_pipe))

        # Le decimos al ambiente lo que va a procesar ...
        #f = 2 # El número de fallos
        f = 0
        for nodo in grafica:
            env.process(nodo.consenso(env, f))
        # ...y lo corremos
        env.run(until=TIEMPO_DE_EJECUCION)

        nodos_fallidos = 0
    
        for i in range(0, len(grafica)):
            nodo = grafica[i]
            #print("Id: ",nodo.id_nodo," valores: ",nodo.V)
            if nodo.fallare:
                nodos_fallidos += 1
            else:
                assert nodo.V == [0,1,2,3,4,5,6], ("Valores V_i incorrectos para el nodo %d",nodo.id_nodo)
                assert  0 == nodo.lider == next(item for item in nodo.V if item is not None), ("Fallo en lider elegido")
                assert nodos_fallidos == f == 0 , ("Nodos fallidos")
    
    def test_f_3(self):
        ''' Método que prueba el algoritmo de consenso con F =  3. '''
        # Creamos el ambiente y el objeto Canal
        env = simpy.Environment()
        bc_pipe = CanalRecorridos(env)

        # La lista que representa la gráfica
        grafica = []

        # Creamos los nodos
        for i in range(0, len(self.adyacencias)):
            grafica.append(NodoConsenso(i, self.adyacencias[i],
                                        bc_pipe.crea_canal_de_entrada(), bc_pipe))

        # Le decimos al ambiente lo que va a procesar ...
        #f = 2 # El número de fallos
        f = 3
        for nodo in grafica:
            env.process(nodo.consenso(env, f))
        # ...y lo corremos
        env.run(until=TIEMPO_DE_EJECUCION)

        nodos_fallidos = 0
    
        for i in range(0, len(grafica)):
            nodo = grafica[i]
            #print("Id: ",nodo.id_nodo," valores: ",nodo.V)
            if nodo.fallare:
                nodos_fallidos += 1
            else:
                if nodo.id_nodo >= f :
                    assert nodo.V == [None,None,None,3,4,5,6], ("Valores V_i incorrectos para el nodo %d",nodo.id_nodo)
                else:
                    print("OUTPUT HOLAAAAAAAAAA")
                    output = [None] * (len(self.adyacencias) )
                    output[nodo.id_nodo] = nodo.id_nodo
                    assert nodo.v == output  ("Los nodos que fallaron al inicio no debieron comunicarse")
                                       
                assert  3 == nodo.lider == next(item for item in nodo.V if item is not None), ("Fallo en lider elegido")
                assert nodos_fallidos == f == 3 , ("Nodos fallidos")
    
    def test_Random(self):
        ''' Método que prueba el algoritmo con una grafica completa generada aleatoriamente . F = valor aleatorio '''
        # Creamos el ambiente y el objeto Canal
        env = simpy.Environment()
        bc_pipe = CanalRecorridos(env)

        # La lista que representa la gráfica
        grafica = []


        # Creamos los nodos
        for i in range(0, len(self.adyacencias_random)):
            grafica.append(NodoConsenso(i, self.adyacencias_random[i],
                                        bc_pipe.crea_canal_de_entrada(), bc_pipe))
            

        # Le decimos al ambiente lo que va a procesar ...
        #f = 2 # El número de fallos
        print("Grafica: ",self.adyacencias_random)

        #random.randrange(limit)
        f = random.randrange(self.cantidad_nodos)
        
        if ( f + 1 ) == self.cantidad_nodos :  #Esto quiere decir que solo un nodo esta funcionando, 
            f-=1  

        if f < 0 : f = 0

        print("Nodos: ", self.cantidad_nodos, " Len grafica", len(grafica))
        print("F: ", f)


        for nodo in grafica:
            env.process(nodo.consenso(env, f))
        # ...y lo corremos
        env.run(until=TIEMPO_DE_EJECUCION)

        nodos_fallidos = 0

        lider_elegido = None 
        salida_valoresi = [None]*((self.cantidad_nodos))

        for i in range(len(salida_valoresi)) :
            if i >= f :
                salida_valoresi[i] = i
            

        for i in range(0, len(grafica)):
            nodo = grafica[i]
            #print("Id: ",nodo.id_nodo," valores: ",nodo.V)
            if nodo.fallare:
                nodos_fallidos += 1
            else:
                
                lider_elegido = nodo.lider if lider_elegido is None else lider_elegido
                
                assert lider_elegido == nodo.lider , ("Fallo Lider elegido") 
                
                assert nodo.lider == next(item for item in nodo.V if item is not None) ,("Fallo Lider elegido segunda prueba")

                if nodo.id_nodo >= f :
                    #assert nodo.V == [None,None,None,3,4,5,6], ("Valores V_i incorrectos para el nodo %d",nodo.id_nodo)
                    print("Salida valores: ", nodo.V," ","Salida esperada: ", salida_valoresi   )
                    assert nodo.V == salida_valoresi, ("Valores V_i incorrectos para el nodo %d",nodo.id_nodo)
                    
                else:
                    output = [None] * (len(self.nodos_random))
                    output[nodo.id_nodo] = nodo.id_nodo
                    assert nodo.v == output , ("Los nodos que fallaron al inicio no debieron comunicarse")
                                       
                assert  nodo.lider == next(item for item in nodo.V if item is not None), ("Fallo en lider elegido")

                assert nodos_fallidos == f  , ("Prueba de nodos fallidos")
        

                
    

        