from servicios.index import buscar_por_nombre

def busqueda_por_nombre(menu,arboles,juegos):
  while True:
    print(menu)
    try:
      tipo_busqueda = input("Elegí una opción: ").strip()
      if tipo_busqueda == "1":
        nombre = input("Ingresa el nombre exacto del videojuego: ").strip()
        resultados_BST=arboles["arbol_BST_nombre"].buscar(nombre)
        resultados_AVL=arboles["arbol_avl"].buscar(nombre)
        print("\nResultados de la búsqueda por nombre exacto en BST: ")
        print(*resultados_BST)
        print("\nResultados de la búsqueda por nombre exacto en AVL: ")
        print(*resultados_AVL)      
      elif tipo_busqueda == "2":
        nombre = input("Ingresa el nombre parcial del videojuego: ").strip()
        resultados = buscar_por_nombre(juegos, nombre)
        print("\nResultados de la búsqueda por nombre parcial: ")
        print(*resultados)
  
      elif tipo_busqueda == "0":
        print("Volviendo al menú anterior...")
        break
      else:
        print("Opcion invalida.")
        break
    except ValueError:
      print("Entrada inválida. Ingresá un número.")