class Heap:
  """Heap binaria (TP6), implementada a mano sobre una lista.

  Es un arbol binario completo guardado en una lista: para el elemento que esta
  en la posicion i, su hijo izquierdo esta en 2*i+1, su hijo derecho en 2*i+2 y
  su padre en (i-1)//2. Todo elemento "va antes" que sus hijos, asi que la raiz
  (posicion 0) siempre es el primero del ranking.

  - clave: funcion que recibe un elemento y devuelve su prioridad (por ejemplo
    lambda juego: juego.rating). Por defecto el propio elemento.
  - maximo: True  -> la raiz es la prioridad MAS ALTA (heap de maximos).
            False -> la raiz es la prioridad mas baja (heap de minimos).
  """

  def __init__(self, clave=lambda x: x, maximo=True):
    self.items = []
    self.clave = clave
    self.maximo = maximo

  def __len__(self):
    return len(self.items)

  def esta_vacia(self):
    return len(self.items) == 0

  # Devuelve True si el elemento a debe ir ANTES (mas cerca de la raiz) que b.
  def _va_antes(self, a, b):
    if self.maximo:
      return self.clave(a) > self.clave(b)
    return self.clave(a) < self.clave(b)

  def _intercambiar(self, i, j):
    self.items[i], self.items[j] = self.items[j], self.items[i]

# ------------------------- Operaciones principales -------------------------#

  # Agrega un elemento: se pone al final y "sube" mientras vaya antes que su padre.
  # Costo: O(log n), porque sube como mucho la altura del arbol.
  def insertar(self, valor):
    self.items.append(valor)
    self._subir(len(self.items) - 1)

  def _subir(self, i):
    while i > 0:
      padre = (i - 1) // 2
      if self._va_antes(self.items[i], self.items[padre]):
        self._intercambiar(i, padre)
        i = padre
      else:
        break

  # Mira la raiz sin sacarla. Costo: O(1). Devuelve None si la heap esta vacia.
  def ver_raiz(self):
    if self.esta_vacia():
      return None
    return self.items[0]

  # Saca y devuelve la raiz (el primero del ranking). Costo: O(log n).
  # El ultimo elemento pasa a la raiz y "baja" intercambiandose con su mejor hijo.
  def extraer(self):
    if self.esta_vacia():
      return None
    raiz = self.items[0]
    ultimo = self.items.pop()
    if self.items:
      self.items[0] = ultimo
      self._bajar(0)
    return raiz

  def _bajar(self, i):
    n = len(self.items)
    while True:
      izquierdo = 2 * i + 1
      derecho = 2 * i + 2
      mejor = i
      if izquierdo < n and self._va_antes(self.items[izquierdo], self.items[mejor]):
        mejor = izquierdo
      if derecho < n and self._va_antes(self.items[derecho], self.items[mejor]):
        mejor = derecho
      if mejor == i:
        break
      self._intercambiar(i, mejor)
      i = mejor

# --------------------------- Construccion y Top-N ---------------------------#

  # Arma una heap a partir de una lista completa. En vez de insertar uno por uno
  # (O(n log n)), copia la lista y hace "bajar" desde el ultimo padre hasta la
  # raiz: costo total O(n).
  @classmethod
  def desde_lista(cls, lista, clave=lambda x: x, maximo=True):
    heap = cls(clave, maximo)
    heap.items = list(lista)
    for i in range(len(heap.items) // 2 - 1, -1, -1):
      heap._bajar(i)
    return heap

  # Devuelve los n primeros del ranking, del mejor al peor, SIN modificar la heap.
  # En vez de copiar y vaciar toda la heap, usa una heap auxiliar con las
  # posiciones "candidatas": el siguiente mejor elemento siempre es hijo de alguno
  # ya elegido. Cada paso cuesta O(log n) y se repite n veces, asi que el Top-N
  # cuesta O(n log n) con n = cantidad pedida, sin depender del tamaño del catalogo.
  def top_n(self, n):
    resultado = []
    if n <= 0 or self.esta_vacia():
      return resultado
    candidatos = Heap(clave=lambda pos: self.clave(self.items[pos]), maximo=self.maximo)
    candidatos.insertar(0)
    while len(resultado) < n and not candidatos.esta_vacia():
      pos = candidatos.extraer()
      resultado.append(self.items[pos])
      for hijo in (2 * pos + 1, 2 * pos + 2):
        if hijo < len(self.items):
          candidatos.insertar(hijo)
    return resultado
