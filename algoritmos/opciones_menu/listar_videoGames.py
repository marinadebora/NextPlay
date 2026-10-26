def listar_todos(arboles):
  print("Listando todos los videojuegos...")
  # Se obtiene la lista ordenada de videojuegos utilizando el recorrido inorden 
  # del árbol AVL
  arbol_avl = arboles["arbol_avl"]
  lista_ordenada = arbol_avl.inorder(arbol_avl.raiz)
  print(*lista_ordenada)
