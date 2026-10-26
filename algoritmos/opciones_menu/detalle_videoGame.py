def detalle(arboles):
  nombre = input("Ingresa el nombre exacto del videojuego:").strip()
  if nombre:
    resultado = arboles["arbol_BST_nombre"].buscar(nombre)
    if resultado:
      print(f"Detalle del Videogame: {nombre}")
      print(resultado)
    else:
      print("No se encontro el videojuego")
  else:
    print("No ingreso un nombre")