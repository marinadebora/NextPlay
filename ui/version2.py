from ui.menu import MENU
from algoritmos.construir_arbol import construir_arbol
from servicios.index import buscar_por_nombre, filtrar
from ui.index import _mostrar, ver_detalle_videojuego, Comparar_dos_videojuegos
from estructuras.arbol_busqueda_nombre import Arbol as Arbol_name, Nodo as Nodo_name
from estructuras.arbol_busqueda_rating import Arbol as Arbol_rating, Nodo as Nodo_rating


def iniciar_version2(juegos):
  arbol_nombre = construir_arbol(juegos, Arbol_name, Nodo_name, lambda x: x.name)
  arbol_rating = construir_arbol(juegos, Arbol_rating, Nodo_rating, lambda x: x.rating)

  while True:
    print(MENU)
    opcion = input("Elegi una opcion: ").strip()

    if opcion == "1":
        print("seleccione tipo de busqueda: \n 1. por nombre exacto. \n 2. por nombre parcial.")
        tipo_busqueda = input("Elegi una opcion: ").strip()
        
        if tipo_busqueda == "1":
            nombre = input("Ingresa el nombre exacto del videojuego: ").strip()
            resultados = arbol_nombre.buscar(nombre)
            print(f"\nResultados de la busqueda por nombre exacto: {resultados}")
        elif tipo_busqueda == "2":
            nombre = input("Ingresa el nombre parcial del videojuego: ").strip()
            resultados = buscar_por_nombre(juegos, nombre)
            print(f"\nResultados de la busqueda por nombre parcial: {resultados}")
    
    if opcion == "2":
        print("Listando todos los videojuegos...")
        _mostrar(juegos)
    
    if opcion == "3":
        print("seleccione tipo de busqueda: \n 1. por genero \n 2. por plataforma \n 3. por rating minimo")
        tipo_filtro = input("Elegi una opcion: ").strip()
        if tipo_filtro == "1":
            genero = input("Genero (enter para omitir): ").strip() or None
            _mostrar(filtrar(juegos, genero=genero))
        elif tipo_filtro == "2":
            plataforma = input("Plataforma (enter para omitir): ").strip() or None
            _mostrar(filtrar(juegos, plataforma=plataforma))
        elif tipo_filtro == "3":
            rating_min = input("Rating minimo (enter para omitir): ").strip() or None
            if rating_min is None:
                resultados = arbol_rating.inorder(arbol_rating.raiz) 
                print(f"\nResultados de la busqueda por rating minimo: {resultados}")
            else:
                resultados = arbol_rating.buscar_desde(float(rating_min))
                print(f"\nResultados de la busqueda por rating minimo: {resultados}")
        else:
            print("Opcion invalida.")
    
    if opcion == "4":
        ver_detalle_videojuego(juegos)
    
    if opcion == "5":
        Comparar_dos_videojuegos(juegos)  
    
    if opcion == "0":
        print("Hasta la proxima!")
        break