from estructuras.arbol_avl import Arbol as Arbol_avl

def construir_arbol_avl(juegos):
  arbol = Arbol_avl()
  for juego in juegos:
    arbol.agregar(juego) 
  return arbol