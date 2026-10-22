from ui.menu import MENU
from algoritmos.construir_arbol import construir_arbol
from algoritmos.construir_arbol_avl import construir_arbol_avl
from servicios.index import buscar_por_nombre, filtrar
from ui.index import _mostrar, ver_detalle_videojuego, Comparar_dos_videojuegos
from estructuras.arbol_busqueda_nombre import Arbol as Arbol_name, Nodo as Nodo_name
from estructuras.arbol_busqueda_rating import Arbol as Arbol_rating, Nodo as Nodo_rating

def iniciar_version2(juegos):
  arbol_nombre = construir_arbol(juegos, Arbol_name, Nodo_name, lambda x: x.name)
  arbol_rating = construir_arbol(juegos, Arbol_rating, Nodo_rating, lambda x: x.rating)
  arbol_nombre_avl = construir_arbol_avl(juegos)

  while True:
    print(MENU)
    opcion = input("Elegi una opcion: ").strip()

    if opcion == "1":
        print("seleccione tipo de busqueda: \n 1. por nombre exacto. \n 2. por nombre parcial. \n 0. Volver.")
        tipo_busqueda = input("Elegi una opcion: ").strip()
        
        if tipo_busqueda == "1":
            nombre = input("Ingresa el nombre exacto del videojuego: ").strip()
            resultados_BST = arbol_nombre.buscar(nombre)
            resultados_AVL = arbol_nombre_avl.buscar(nombre)
            print(f"\nResultados de la busqueda por nombre exacto en BST: {resultados_BST}")
            print(f"Resultados de la busqueda por nombre exacto en AVL: {resultados_AVL}")
        elif tipo_busqueda == "2":
            nombre = input("Ingresa el nombre parcial del videojuego: ").strip()
            resultados = buscar_por_nombre(juegos, nombre)
            print(f"\nResultados de la busqueda por nombre parcial: {resultados}")
        elif tipo_busqueda == "0":
            print("Volviendo al menú anterior...")
        else:
            print("Opcion invalida.")
    elif opcion == "2":
        print("Listando todos los videojuegos...")
        # Se obtiene la lista ordenada de videojuegos utilizando el recorrido inorden del árbol AVL
        lista_ordenada = arbol_nombre_avl.inorder(arbol_nombre_avl.raiz)
        _mostrar(lista_ordenada)
    
    elif opcion == "3":
        print("seleccione tipo de busqueda: \n 1. por genero \n 2. por plataforma \n 3. por rating minimo \n0.Volver.")
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
                print("\nResultados de la busqueda por rating minimo:")
                print(*resultados)
            else:
                resultados = arbol_rating.buscar_desde(float(rating_min))
                print("\nResultados de la busqueda por rating minimo:")
                print(*resultados)
        elif tipo_filtro == "0":
            print("Volviendo al menú anterior...")
        else:
            print("Opcion invalida.")
    
    elif opcion == "4":
        ver_detalle_videojuego(juegos)
    
    elif opcion == "5":
        Comparar_dos_videojuegos(juegos)  
    
    elif opcion == "0":
        print("Hasta la proxima!")
        return
    else:
        print("Opcion invalida.")