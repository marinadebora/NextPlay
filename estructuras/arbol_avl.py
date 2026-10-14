class Nodo:
  def __init__(self, valor):
    self.valor = valor
    self.izquierda = None
    self.derecha = None
    self.altura = 1  # Altura del nodo, inicializada en 1 para nodos hoja

class Arbol:
  def __init__(self):
    self.raiz = None
# ------------------------- Metodos de balanceo y rotacion -------------------------#

  def obtener_altura(self, nodo):
    # Si el nodo es None, retorna 0, de lo contrario retorna la altura del nodo.
    if nodo is None:
      return 0
    return nodo.altura

  def altura(self):
    # Retorna la altura del árbol, que es la altura de la raíz.
    return self.obtener_altura(self.raiz)
  
  def factor_balance(self, nodo):
    # Calcula el factor de balance del nodo.
    if nodo is None:
      return 0
    return self.obtener_altura(nodo.izquierda) - self.obtener_altura(nodo.derecha)
 
  def rotacion_derecha(self, y):
    # Obtiene el nodo izquierdo de y y su subárbol derecho 
    x = y.izquierda
    T2 = x.derecha

    # Realiza la rotación
    x.derecha = y
    y.izquierda = T2

    # Actualiza las alturas
    y.altura = 1 + max(self.obtener_altura(y.izquierda), self.obtener_altura(y.derecha))
    x.altura = 1 + max(self.obtener_altura(x.izquierda), self.obtener_altura(x.derecha))

    # Retorna la nueva raíz
    return x

  def rotacion_izquierda(self, x):
    # Obtiene el nodo derecho de x y su subárbol izquierdo
    y = x.derecha
    T2 = y.izquierda

    # Realiza la rotación
    y.izquierda = x
    x.derecha = T2

    # Actualiza las alturas
    x.altura = 1 + max(self.obtener_altura(x.izquierda), self.obtener_altura(x.derecha))
    y.altura = 1 + max(self.obtener_altura(y.izquierda), self.obtener_altura(y.derecha))

    # Retorna la nueva raíz
    return y
# ---------------------------------------------------------------------------------#
# Metodos principales
  def agregar(self, valor):
    # Si la raíz es None, crea un nodo con el valor y lo asigna a la raíz.
    if self.raiz is None:
      self.raiz = Nodo(valor)
    else:
      # Llama a la función recursiva para agregar el valor al árbol.
      self.raiz = self._agregar_recursivo(self.raiz, valor)

  def _agregar_recursivo(self, nodo, valor):
    # Si el nodo es None, crea un nuevo nodo con el valor.
    if nodo is None:
      return Nodo(valor)

    # Compara el valor con el valor del nodo actual para decidir dónde insertarlo.
    if valor.name.lower() < nodo.valor.name.lower():
      nodo.izquierda = self._agregar_recursivo(nodo.izquierda, valor)
    else:
      nodo.derecha = self._agregar_recursivo(nodo.derecha, valor)

    # Actualiza la altura del nodo actual.
    nodo.altura = 1 + max(self.obtener_altura(nodo.izquierda), self.obtener_altura(nodo.derecha))

    # Calcula el factor de balance del nodo actual.
    balance = self.factor_balance(nodo)

    # Realiza las rotaciones necesarias para mantener el árbol balanceado.
    # Para decidir el caso se mira el factor de balance del hijo (y no el valor
    # insertado): asi tambien funciona cuando hay nombres repetidos, que el
    # arbol manda siempre hacia la derecha.
    # Caso izquierda-izquierda: rotacion simple a la derecha.
    if balance > 1 and self.factor_balance(nodo.izquierda) >= 0:
      return self.rotacion_derecha(nodo)
    # Caso derecha-derecha: rotacion simple a la izquierda.
    if balance < -1 and self.factor_balance(nodo.derecha) <= 0:
      return self.rotacion_izquierda(nodo)
    # Caso izquierda-derecha: rotacion izquierda en el hijo y luego derecha en el nodo.
    if balance > 1 and self.factor_balance(nodo.izquierda) < 0:
      nodo.izquierda = self.rotacion_izquierda(nodo.izquierda)
      return self.rotacion_derecha(nodo)
    # Caso derecha-izquierda: rotacion derecha en el hijo y luego izquierda en el nodo.
    if balance < -1 and self.factor_balance(nodo.derecha) > 0:
      nodo.derecha = self.rotacion_derecha(nodo.derecha)
      return self.rotacion_izquierda(nodo)

    # Retorna el nodo (sin cambios si no se realizaron rotaciones).
    return nodo

  def buscar(self, name):
    # Si la raíz es None, retorna None.
    if self.raiz is None:
      return None
    else:
      # Llama a la función recursiva para buscar el nombre en el árbol.
      return self._buscar_recursivo(self.raiz, name)

  def _buscar_recursivo(self, nodo, name):
    # Si el nodo es None, retorna None.
    if nodo is None:
      return None
    # Si el nombre del nodo es igual al nombre buscado, retorna el valor del nodo.
    if nodo.valor.name.lower() == name.lower():
      return nodo.valor
    # Si el nombre buscado es menor que el nombre del nodo, busca en el subárbol izquierdo.
    elif name.lower() < nodo.valor.name.lower():
      return self._buscar_recursivo(nodo.izquierda, name)
    else:
      # Si el nombre buscado es mayor que el nombre del nodo, busca en el subárbol derecho.
      return self._buscar_recursivo(nodo.derecha, name)
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