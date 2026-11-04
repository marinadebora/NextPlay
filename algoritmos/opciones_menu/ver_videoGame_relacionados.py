def ver_videoGame_relacionados(grafo,arbol):
    """Permite al usuario ingresar un videojuego y muestra los videojuegos relacionados.

    Args:
        grafo: El grafo que contiene los videojuegos y sus relaciones.
    """
    nombre = input("Ingresa el nombre exacto del videojuego para ver sus relacionados: ").strip()
    videoGame = arbol.buscar(nombre)
    
    if videoGame is None:
        print(f"No se encontró el videojuego '{nombre}'.")
        return
    else:
      buscar_relacionados(grafo, videoGame, nombre)


def buscar_relacionados(grafo, videoGame, nombre):
    """Muestra los videojuegos relacionados con el videojuego dado.

    Args:
        grafo: El grafo que contiene los videojuegos y sus relaciones.
        videoGame: El videojuego del cual se desean obtener los relacionados.
        nombre: El nombre del videojuego para mostrar en los mensajes.
    """
    if not grafo.tiene_vertice(videoGame):
        print(f"El videojuego '{nombre}' no está en el grafo.")
        return

    relacionados = grafo.vecinos(videoGame)
    if not relacionados:
        print(f"No hay videojuegos relacionados con '{nombre}'.")
        return
    relacionados = sorted(relacionados, key=lambda x: x[1], reverse=True)
    print("=" * 40)
    print(videoGame)
    print(f"Videojuegos relacionados con '{nombre}'")
    print("=" * 40)
    for relacionado, peso in relacionados:
        print(relacionado)
        print(f"Peso de la relación: {peso}")
