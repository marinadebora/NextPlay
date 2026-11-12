from collections import deque
#================================================#
""" Breadth-First Search o BÚSQUEDA EN ANCHURA  """
#================================================#
def bfs(grafo, origen):
  """  
  Recorre el grafo desde un videojuego de origen utilizando el algoritmo BFS. 
  Visita primero los videojuegos directamente relacionados con el origen, 
  luego continúa recorriendo los siguientes niveles de relaciones.
  Permite conocer el orden de visita, la distancia en cantidad de aristas desde el origen 
  y el videojuego anterior que permitió llegar a cada vértice.
  Parámetros:
    grafo: grafo de videojuegos que se desea recorrer.
    origen: videojuego desde el cual comienza el recorrido.
  Retorna:
    El orden de visita, las distancias desde el origen y
    los padres de cada videojuego en el recorrido."""
  
  if not grafo.tiene_vertice(origen):
    raise ValueError(f"El videojuego {origen} no está en el grafo.")
  
  clave_origen = grafo.clave(origen)
  cola = deque([origen])
  visitados = {clave_origen}
  distancias = {clave_origen: 0}
  padres = {clave_origen: None}
  orden_visita = []

  while cola:
    actual = cola.popleft()
    clave_actual = grafo.clave(actual)

    for vecino, _  in grafo.vecinos(actual):
      clave_vecino = grafo.clave(vecino)

      if clave_vecino not in visitados:
        visitados.add(clave_vecino)        
        distancias[clave_vecino] = distancias[clave_actual] + 1
        padres[clave_vecino] = clave_actual
        cola.append(vecino)

    orden_visita.append(actual)

  return orden_visita, distancias, padres
# --------------------------------------------------------------------#
def camino_mas_corto(grafo, origen, destino):
    """
    Encuentra el camino con menor cantidad de aristas entre
    dos videojuegos utilizando BFS.

    Retorna una tupla (camino, distancia): el camino es la lista de objetos
    VideoJuego desde el origen hasta el destino y la distancia es la cantidad
    de aristas. Si no existe un camino, retorna None.
    """

    if not grafo.tiene_vertice(origen):
        raise ValueError("El videojuego de origen no está en el grafo.")

    if not grafo.tiene_vertice(destino):
        raise ValueError("El videojuego de destino no está en el grafo.")

    _, distancias, padres = bfs(grafo, origen)

    clave_destino = grafo.clave(destino)

    if clave_destino not in distancias:
        return None

    camino = []
    actual = clave_destino

    while actual is not None:
        camino.append(actual)
        actual = padres[actual]

    camino.reverse()

    videojuegos = {
        grafo.clave(juego): juego
        for juego in grafo.vertices()
    }
    games = [videojuegos[clave] for clave in camino]
    return games , distancias[clave_destino]

# --------------------------------------------------------------------#

#================================================#
""" Depth-first search o BÚSQUEDA EN PROFUNDIDAD """
#================================================#
def dfs(grafo, origen):
    """
    Recorre el grafo desde un videojuego de origen utilizando DFS.
    Explora cada rama hasta donde sea posible antes de
    retroceder y continuar con otras ramas.
    Retorna una lista de videojuegos en orden de visita.

    Es iterativo (pila explicita), asi que no tiene limite de profundidad
    de recursion. Un videojuego se marca como visitado recien cuando se
    saca de la pila (no cuando se apila): asi cada paso baja por una
    arista desde el ultimo videojuego visitado, que es lo que define a un DFS.
    """
    if not grafo.tiene_vertice(origen):
        raise ValueError("El videojuego de origen no está en el grafo.")

    pila = [origen]
    visitados = set()
    orden_visita = []

    while pila:
        actual = pila.pop()
        clave_actual = grafo.clave(actual)

        if clave_actual in visitados:
            continue  # ya se visito por otra rama

        visitados.add(clave_actual)
        orden_visita.append(actual)

        # en orden inverso para que el primer vecino sea el primero en explorarse
        for vecino, _ in reversed(grafo.vecinos(actual)):
            if grafo.clave(vecino) not in visitados:
                pila.append(vecino)

    return orden_visita
