from collections import deque

class Nodo:
  def __init__(self, valor):
    self.valor = valor
    self.hijos = []

  def agregar_hijo(self, hijo):
    self.hijos.append(hijo)
  
  def eliminar_hijo(self, hijo):
    if hijo in self.hijos:
      self.hijos.remove(hijo)


class Arbol:
  def __init__(self, raiz):
    self.raiz = Nodo(raiz)
    # Se agrega un diccionario auxiliar para almacenar las categorias y sus nodos correspondientes esto evita que tenga que iterar la lista hijos de la raiz constantemente
    self.categorias = {}

  def agregar_hijo(self, hijo):
    # Obtiene la lista de generos o plataformas segun la raiz.
    nueva_categoria = getattr(hijo, self.raiz.valor) 
    # Procesa cada categoria del videojuego.
    for categoria in nueva_categoria:
      # Reutliza el nodo existente.
      if categoria in self.categorias:
       nuevo_nodo = self.categorias[categoria]
      # Crea el nodo,se agrega a la raiz y se registra en el diccionario.
      else:
        nuevo_nodo = Nodo(categoria)
        self.raiz.agregar_hijo(nuevo_nodo)
        # Se guarda en el diccionario la categoria y el nodo correspondiente
        self.categorias[categoria] = nuevo_nodo
      # Se agrega el hijo al nuevo nodo
      nuevo_nodo.agregar_hijo(Nodo(hijo))

  def buscar_por_categoria(self, categoria):
    # Si la categoria existe en el diccionario, se retorna la lista de hijos del nodo correspondiente.
    if categoria in self.categorias:
      resultado = self.categorias[categoria]
      return resultado.hijos
    else:
      return None
#---------------------------------------------------------------------------------#
  # TIPOS DE RECORRIDO
  # preorder: raiz, hijos
  def preorder(self):
    if self.raiz is None:
      return []
    return self._preorder_recursivo(self.raiz)

  def _preorder_recursivo(self, nodo):
    # Guarda en el resultado el valor del nodo actual.
    resultado= [nodo.valor]
    # Si el nodo no tiene hijos, retorna el resultado.
    if nodo.hijos == []:
      return resultado
    else:
      # Recorre cada hijo del nodo y llama recursivamente a la función para obtener los valores de los hijos.
      for hijo in nodo.hijos:
        resultado.extend(self._preorder_recursivo(hijo))
      # Retorna el resultado final con los valores de todos los nodos en el orden preorder.
      return resultado

  # inorder: primer hijo, raiz, hijos restantes
  def inorder(self):
    if self.raiz is None:
      return []
    return self._inorder_recursivo(self.raiz)
  def _inorder_recursivo(self, nodo):
    resultado = []
    # Si el nodo tiene hijos, se procesa el primer hijo antes de agregar el valor del nodo actual.
    if nodo.hijos:
      resultado.extend(self._inorder_recursivo(nodo.hijos[0]))
    # Se agrega el valor del nodo actual al resultado.
    resultado.append(nodo.valor)
    # Si el nodo tiene más de un hijo, se procesan los hijos restantes después de agregar el valor del nodo actual.
    if len(nodo.hijos) > 1:
      for hijo in nodo.hijos[1:]:
        resultado.extend(self._inorder_recursivo(hijo))
    return resultado
  
  # postorder: los hijos, raiz
  def postorder(self):
    if self.raiz is None:
      return []
    return self._postorder_recursivo(self.raiz)
  
  def _postorder_recursivo(self, nodo):
    resultado = []
    # Si el nodo tiene hijos, se procesan todos los hijos antes de agregar el valor del nodo actual.
    for hijo in nodo.hijos:
      resultado.extend(self._postorder_recursivo(hijo))
    # Se agrega el valor del nodo actual al resultado.
    resultado.append(nodo.valor)
    return resultado
  # por_nivel: Se procesan los nodos teniendo en cuenta sus niveles raiz, hijos de la raiz, hijos de los hijos, etc.
  def por_nivel(self):
    if self.raiz is None:
      return []
    # Se utiliza deque como cola FIFO porque permite quitar el primer elemnto con popleft en O(1)
    cola = deque([self.raiz])
    resultado = []
    while cola:
      # Se obtiene el primer nodo de la cola.
      nodo_actual = cola.popleft()
      # Se agrega el valor del nodo actual al resultado.
      resultado.append(nodo_actual.valor)
      # Se agregan los hijos del nodo actual a la cola para procesarlos en el siguiente nivel.
      cola.extend(nodo_actual.hijos)
    return resultado
