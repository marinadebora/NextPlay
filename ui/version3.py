from ui.menu import MENU, MENU_NOMBRE, MENU_FILTRO, GENEROS, PLATAFORMAS
from config import GENRES, PLATFORM
from ui.index import _mostrar, ver_detalle_videojuego, Comparar_dos_videojuegos
from algoritmos import construir_arbol, construir_arbol_avl, construir_arbol_general,buscar_por_categoria
from estructuras import arbol_nombre, nodo_nombre, arbol_ratin, nodo_ratin
from servicios.index import buscar_por_nombre, filtrar

def iniciar_version_3(juegos ):
  arbol_BST_nombre = construir_arbol(juegos, arbol_nombre, nodo_nombre, lambda x: x.name)
  arbol_BST_rating = construir_arbol(juegos, arbol_ratin, nodo_ratin, lambda x: x.rating)
  arbol_avl = construir_arbol_avl(juegos)
  arbol_general_genres = construir_arbol_general("genres",juegos)
  arbol_general_platform = construir_arbol_general("platform",juegos)

  while True:
    print(MENU)
    opcion = input("Elegí una opción: ").strip()
    
    if opcion == "1":
      print(MENU_NOMBRE)
      tipo_busqueda = input("Elegí una opción: ").strip()
           
      if tipo_busqueda == "1":
        nombre = input("Ingresa el nombre exacto del videojuego: ").strip()
        resultados_BST = arbol_BST_nombre.buscar(nombre)
        resultados_AVL = arbol_avl.buscar(nombre)
        print(f"\n Resultados de la búsqueda por nombre exacto en BST: {resultados_BST}")
        print(f"Resultados de la búsqueda por nombre exacto en AVL: {resultados_AVL}")
      elif tipo_busqueda == "2":
        nombre = input("Ingresa el nombre parcial del videojuego: ").strip()
        resultados = buscar_por_nombre(juegos, nombre)
        print(f"\nResultados de la búsqueda por nombre parcial: {resultados}")
    
    if opcion == "2":
      print("Listando todos los videojuegos...")

      # Se obtiene la lista ordenada de videojuegos utilizando el recorrido inorden del árbol AVL
      lista_ordenada = arbol_avl.inorder(arbol_avl.raiz)
      _mostrar(lista_ordenada)

    if opcion == "3":
      print(MENU_FILTRO)
      tipo_filtro = input("Elegí una opción: ").strip()
      
      if tipo_filtro == "1":
        print(GENEROS)
        try:
          genero = int(input("Elegí una opción: ").strip())
          if genero <= 19 and genero > 0 :
            resultado = buscar_por_categoria(arbol_general_genres, GENRES[genero])
          else:
            print("Elegí una opción correcta")
            break
        except ValueError:
          print("Entrada inválida. Ingresá un número.")

      elif tipo_filtro == "2":
        print(PLATAFORMAS)

        while True:
          try:
            plataforma = int(input("Elegí una opción: ").strip())
            if plataforma <= 50 and plataforma > 0:
              resultado = buscar_por_categoria(arbol_general_platform, PLATFORM[plataforma])
            else:
              print("Elegí una opción correcta")
              break
          except ValueError:
            print("Entrada inválida. Ingresá un número.")

      elif tipo_filtro == "3":
        while True:
          try:
            rating_min = input("Rating minimo (enter para omitir): ").strip()
            if rating_min == "":              
              resultados = arbol_BST_rating.inorder(arbol_BST_rating.raiz) 
              print(f"\nResultados de la busqueda por rating minimo: {resultados}")
            else:
              resultados = arbol_BST_rating.buscar_desde(float(rating_min))
              print(f"\nResultados de la busqueda por rating minimo: {resultados}")
              break
          except ValueError:
            print("Entrada inválida. Ingresá un número.")
      
      else:
        print("Opcion invalida.")
    if opcion == "4":
      nombre = input("Ingresa el nombre exacto del videojuego:").strip()
      if nombre:
        resultado = arbol_BST_nombre.buscar(nombre)
        if resultado:
          print(f"Detalle del Videogame: {nombre}")
          print(resultado)
        else:
          print("No se encontro el videojuego")
      else:
        print("No ingreso un nombre")
    if opcion == "5":
      nombre1 = input("Nombre exacto del primer videojuego: ").strip()
      nombre2 = input("Nombre exacto del segundo videojuego: ").strip()
      resultado1 = arbol_BST_nombre.buscar(nombre1)
      resultado2 = arbol_BST_nombre.buscar(nombre2)
      if not resultado1 or not resultado2:
        if not resultado1:
          print(f"No se encontro {nombre1}.")
        if not resultado2:
          print(f"No se encontro {nombre2}.")
      else:
        print(f"\n{resultado1.name}: rating {resultado1.rating}")
        print(f"{resultado2.name}: rating {resultado2.rating}")
        if resultado1.rating > resultado2.rating:
          print(f"\n{resultado1.name} tiene mejor rating.")
        elif resultado2.rating > resultado1.rating:
          print(f"\n{resultado2.name} tiene mejor rating.")
        else:
          print("\nEstan empatados en rating.")

    if opcion == "0":
            print("Hasta la proxima!")
            break
      