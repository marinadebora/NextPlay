# recive una lista con todos los OBJETOS de video juegos
def buscar_nombre_exacto(juegos, nombre):
  # Busca juego por juego hasta encontrar el nombre exacto.
  for juego in juegos:
    if juego.name.lower() == nombre.lower():
      return juego
  return None

  