from algoritmos.recorridos_grafo import camino_mas_corto

def caminos_entre_dos_videojuegos(arbol, grafo):
    nombre_origen = input("Ingrese el nombre exacto del videojuego de origen: ").strip()
    origen = arbol.buscar(nombre_origen)
    
    if not origen:
        print(f"No se encontró el videojuego '{nombre_origen}'.")
        return
    
    nombre_destino = input("Ingrese el nombre exacto del videojuego de destino: ").strip()
    destino = arbol.buscar(nombre_destino)
    
    if not destino:
        print(f"No se encontró el videojuego '{nombre_destino}'.")
        return
    if origen == destino:
        print("El videojuego de origen y destino son el mismo.")
        return
    
    resultados = camino_mas_corto(grafo, origen, destino)
    if resultados is None:
        print(f"No hay camino entre '{nombre_origen}' y '{nombre_destino}'.")
        return
    games, distancias = resultados
    if games:
        print("Camino más corto de ")
        print(f"{nombre_origen} a {nombre_destino}:")
        print(f"{'=' * 32}")
        for videojuego in games:
            print(f"{' ' * 14} ⇩ ")
            print(videojuego.name)
        print(f"{'=' * 32}")
        print(distancias, "Aristas de distancia.")
    else:
        print(f"No hay camino entre '{nombre_origen}' y '{nombre_destino}'.")