def k_merge(arreglo):
    '''
    Algoritmo que hace un merge entre K arreglos ordenados
    Devuelve un arreglo ya ordenado con todos los elementos de los k arreglos
    '''

    arr_merge =[] #arreglo en el que se guardará el resultado
    indices = [0] * len(arreglo)  # posición actual en cada arreglo

    while True:

        elem_min = None #elemento minimo 
        index_min = -1 #indice del arreglo en donde esta el minimo
        
        for i in range(len(arreglo)): #busca el minimo entre los elementos actuales
            if(indices[i]<len(arreglo[i])): #si aun hay elementos en ese sub-arreglo
                actual = arreglo[i][indices[i]] 
                if elem_min is None or actual <= elem_min: 
                    elem_min = actual
                    index_min = i

        if index_min == -1: #todos están vacíos
            break 

        arr_merge.append(elem_min) #agrega el minimo
        indices[index_min] += 1 #aumenta ese índice

    return arr_merge


def cuadricula(arr,cantidad_nodos):
    '''
    Dado un arreglo, devuelve un arreglo de sus subarreglos equilibrados.
    '''
    #cuadricula = [[]] * cantidad_nodos NO es correcto
    cuadricula =  [[] for _ in range(cantidad_nodos)]
    
    if cantidad_nodos == 0: 
        return cuadricula 

    longitud = len(arr)
    num_elem = longitud // cantidad_nodos     
    elem_restantes = longitud % cantidad_nodos

    inicio = 0
    for i in range(cantidad_nodos):
        extra = 1 if i < elem_restantes else 0 #Agrega un elemento mas en los primeros i restantes
        fin = inicio + num_elem + extra 
        cuadricula[i]=arr[inicio:fin]
        inicio = fin


    return cuadricula



'''Pruebas locales 
ar1 = [1,2,3,4,5] 
n_c_1 = 5
c1 =  cuadricula(ar1,n_c_1)


ar2= [1,2,3,4]
n_c_2 = 5
c2 =  cuadricula(ar2,n_c_2)

ar3= [1,2,3,4]
n_c_3 = 8
c3 = cuadricula(ar3,n_c_3)


ar4= [1,2,3,4,5,6,7,8]
n_c4 = 4
c4 =  cuadricula(ar4,n_c4)



ar5= [1,2,3,4,5,6,7,8,9,10,11,12,13]
n_c5 = 5
c5 =  cuadricula(ar5,n_c5)

'''
