class Nodo():
  def __init__(self,valor):
    self.valor = valor
    self.izquierda = None
    self.derecha = None

class Arbol():
  # crea el arbol sin ningun nodo
  def __init__(self):
    self.raiz = None
  
  # si la raiz es None, crea un nodo con el valor y lo asigna a la raiz.
  def agregar(self,valor):
    if self.raiz == None:
      self.raiz = Nodo(valor)
    #si la raiz no es None, llama a la funcion recursiva
    else:
      self._agregar_recursivo(self.raiz, valor)
  
  # asigna los valores a derecha o izquierda 
  def _agregar_recursivo(self, nodo, valor):
    # si el rating es menor que el del nodo actual.
    if valor.rating < nodo.valor.rating:
      # verifica si es None lo agrega a la izquierda.
      if nodo.izquierda is None:
        nodo.izquierda = Nodo(valor)
      # si no, llama a recursivo con el nodo de la izquierda
      else:
        self._agregar_recursivo(nodo.izquierda, valor)
    # si el rating es mayor o igual que el del nodo actual.
    else:
      # verifica si en None lo agrega a la derecha.
      if nodo.derecha is None:
        nodo.derecha = Nodo(valor)
      # si no, llama a la funcion recursiva con el nodo de la derecha.
      else:
        self._agregar_recursivo(nodo.derecha, valor)
#---------------------------------------------------------------------------------#
  # si la raiz en None retorna None, si no llama a buscar recursivo.
  def buscar(self, rating):
    if self.raiz is None:
      return None
    else:
      return self._buscar_recursivo(self.raiz, rating)
  # funcion recursiva que busca un rating en el arbol.
  def _buscar_recursivo(self, nodo, rating):  
    #si el nodo en None retorna None.
    if nodo is None: 
      return None
    # si el rating del nodo es igual a rating  retorna el valor. (game completo)
    if nodo.valor.rating == rating:
      return nodo.valor
    # si el rating es menor que el rating del nodo.
    elif rating < nodo.valor.rating:
      # llama a la funcion recursiva con el nodo de la izquierda.
      return self._buscar_recursivo(nodo.izquierda, rating)
    else:
      # si es mayor llama a la funcion recursiva con el nodo de la derecha.
      return self._buscar_recursivo(nodo.derecha, rating)

#---------------------------------------------------------------------------------#
  # TIPOS DE RECORRIDO
  # preorder: raiz, izquierda, derecha
  def preorder(self, nodo):
    lista = []
    if nodo is None:
      return lista
    else:
      return self.preorder_recursivo(nodo, lista)
  
  def preorder_recursivo(self, nodo, lista):
    if nodo is None:
      return 
    lista.append(nodo.valor)
    self.preorder_recursivo(nodo.izquierda, lista)
    self.preorder_recursivo(nodo.derecha, lista)
    return lista

  # inorder: izquierda, raiz, derecha
  def inorder(self, nodo):
    lista = []
    if nodo is None:
      return lista
    else:
      return self.inorder_recursivo(nodo, lista)

  def inorder_recursivo(self, nodo, lista):
    if nodo is None:
      return 
    self.inorder_recursivo(nodo.izquierda, lista)
    lista.append(nodo.valor)
    self.inorder_recursivo(nodo.derecha, lista)
    return lista

  # postorder: izquierda, derecha, raiz
  def postorder(self, nodo):
    lista = []
    if nodo is None:
      return lista
    else:
      return self.postorder_recursivo(nodo, lista)
    
  def postorder_recursivo(self, nodo, lista):
    if nodo is None:
      return 
    self.postorder_recursivo(nodo.izquierda, lista)
    self.postorder_recursivo(nodo.derecha, lista)
    lista.append(nodo.valor)
    return lista
# ---------------------------------------------------------------------------------#
  def buscar_desde(self, rating_minimo):
    # Crea una lista vacia para almacenar los resultados.
    resultados = []
    # Llama a la funcion recursiva para buscar desde el nodo raiz.
    self._buscar_desde_recursivo(self.raiz, rating_minimo, resultados)
    return resultados
  
  def _buscar_desde_recursivo(self, nodo, rating_minimo, resultados):
    # Si no hay nodo termina la busqueda.
    if nodo is None:
      return
    # si el ratin del nodo es mayor o igual al rating minimo, cumple la condicion.
    if nodo.valor.rating >= rating_minimo:
      # recorre inorder inverso (derecha, raiz, izquierda) para obtener los valores en orden descendente.
      self._buscar_desde_recursivo(nodo.derecha, rating_minimo, resultados)
    # Guarda el nodo actual en la lista deresultados
      resultados.append(nodo.valor)
    # busca en izquierda los rating menores que tambien cumplen la condicion.
      self._buscar_desde_recursivo(nodo.izquierda, rating_minimo, resultados)
    else:
      # Si el rating del nodo es menor al rating minimo, descarta la rama izquierda porque todos sus valores son aun menores.
      self._buscar_desde_recursivo(nodo.derecha, rating_minimo, resultados)
