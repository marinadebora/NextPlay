from estructuras.arbol_busqueda_nombre import Arbol, Nodo

# recive una lista con todos los OBJETOS de video juegos
def construir_arbol(lista):
  	# Ordena la lista alfabeticamente por nombre.
    lista_ordenada =sorted(lista, key=lambda x: x.name)
    # Si lalista contiene elementos... 
    if len(lista_ordenada) > 0:
        # Obtiene la posicion del elemento central.
        position = len(lista_ordenada)//2
        # Crea el nodo raiz con el objeto central.
        raiz = Nodo(lista_ordenada[position])
        # Crea el arbol
        arbol = Arbol()
        # Asigna el nodo raiz al arbol.
        arbol.raiz = raiz
        # Creamos la funcion recursiva.
        def construir_arbol_recursivo(lista):
            # Si la lista contiene elementos...
            if len(lista) > 0:
                # Obtiene la posicion del elemento central.
                nueva_position = len(lista)//2
                # Crea el nodo raiz con el objeto central.
                nueva_raiz = Nodo(lista[nueva_position])
                # Construye recursivamente el subArbol izquierdo.
                nueva_raiz.izquierda = construir_arbol_recursivo(lista[:nueva_position])
                # Construye recursivamente el subArbol derecho.
                nueva_raiz.derecha = construir_arbol_recursivo(lista[nueva_position + 1:])
                # Retorna el nodo creado.
                return nueva_raiz
            else:
                # Si la lista esta vacia no puede contruir nodo por lo que devuelve None
                return None
        # Llama a la funcion recursiva para construir la raiz del subArbol izquierdo.
        arbol.raiz.izquierda = construir_arbol_recursivo(lista_ordenada[:position])
        # Llama a la funcion recursiva para construir la raiz del subArbol derecho.
        arbol.raiz.derecha = construir_arbol_recursivo(lista_ordenada[position + 1:])
    else:
        # Si la lista esta vacia no puede contruir un arbol por lo retorna None.
        return None
    # Retorna el arbol construido.
    return arbol