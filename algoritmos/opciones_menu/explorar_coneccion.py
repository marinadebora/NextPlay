from algoritmos.recorridos_grafo import dfs

def explorar_conexiones(arbol, grafo):
    """
    Permite al usuario explorar los videojuegos relacionados con un videojuego de su elección.
    Muestra los videojuegos relacionados en el orden en que son visitados mediante una búsqueda en profundidad.
    Parámetros:
        grafo: grafo de videojuegos que se desea explorar.
        arbol: árbol AVL que contiene los videojuegos.
    Retorna:
        None
    """
    nombre = input("Ingrese el nombre exacto del videojuego que desea explorar: ").strip()
    videojuego = arbol.buscar(nombre)

    if not videojuego:
        print(f"El videojuego '{nombre}' no se encuentra en la base de datos.")
        return

    orden_visita = dfs(grafo, videojuego)
    if len(orden_visita) == 1:# Siempre trae el videojuego de origen, por eso si es 1 significa que no hay vecinos
        print(f"No se encontraron videojuegos relacionados con '{nombre}'.")
        return
    
    relacionados = orden_visita[1:]  # Excluye el videojuego de origen
    print("Videojuegos relacionados con: ")
    print(len(relacionados), "videojuegos encontrados.")
    print(nombre)
    for i, juego in enumerate(relacionados, start=1):
        print(f"{' ' * 5} ⇩ ")
        print(f"  {i}. {juego.name}")