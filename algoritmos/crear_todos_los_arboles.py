from algoritmos import construir_arbol, construir_arbol_avl, construir_arbol_general,buscar_por_categoria
from estructuras import arbol_nombre, nodo_nombre, arbol_ratin, nodo_ratin

def crear_arboles(juegos):
  arbol_BST_nombre = construir_arbol(juegos, arbol_nombre, nodo_nombre, lambda x: x.name)
  arbol_BST_rating = construir_arbol(juegos, arbol_ratin, nodo_ratin, lambda x: x.rating)
  arbol_avl = construir_arbol_avl(juegos)
  arbol_general_genres = construir_arbol_general("genres",juegos)
  arbol_general_platform = construir_arbol_general("platform",juegos)
  return {
    "arbol_BST_nombre":arbol_BST_nombre,
    "arbol_BST_rating":arbol_BST_rating,
    "arbol_avl":arbol_avl,
    "arbol_general_genres":arbol_general_genres,
    "arbol_general_platform":arbol_general_platform,
    
  }
