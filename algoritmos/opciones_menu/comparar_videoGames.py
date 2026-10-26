def comparar_2_videoGames(arboles):
  nombre1 = input("Nombre exacto del primer videojuego: ").strip()
  nombre2 = input("Nombre exacto del segundo videojuego: ").strip()
  resultado1 = arboles["arbol_BST_nombre"].buscar(nombre1)
  resultado2 = arboles["arbol_BST_nombre"].buscar(nombre2)
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