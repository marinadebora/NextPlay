class Grafo:
  """Grafo pesado con lista de adyacencia (TP7).

  Cada vertice guarda solo sus vecinos: un diccionario {clave_del_vecino: peso}.
  Por eso el espacio es O(V + E) y no O(V^2) como una matriz.

  - Los vertices son objetos cualquiera (por ejemplo VideoJuego). La funcion
    `clave` dice como identificarlos (por defecto el propio objeto; para los
    juegos se usa lambda j: j.id), igual que en la Heap.
  - Por defecto el grafo es NO dirigido: agregar_arista(a, b) conecta a con b
    y b con a. Con dirigido=True solo conecta a -> b.
  - Toda arista tiene un peso (por defecto 1).
  """

  def __init__(self, clave=lambda x: x, dirigido=False):
    self.clave = clave
    self.dirigido = dirigido
    self._objetos = {}   # clave -> objeto original
    self._ady = {}       # clave -> {clave_vecino: peso}
    self._aristas = 0

  # --- consultas basicas -------------------------------------------------------

  def cantidad_vertices(self):
    return len(self._ady)

  def cantidad_aristas(self):
    """Cuenta cada arista una sola vez (tambien en un grafo no dirigido)."""
    return self._aristas

  def __len__(self):
    return len(self._ady)

  def tiene_vertice(self, v):
    return self.clave(v) in self._ady

  def vertices(self):
    return list(self._objetos.values())

  # --- vertices ----------------------------------------------------------------

  def agregar_vertice(self, v):
    """Agrega el vertice. Devuelve False (sin cambios) si ya estaba. O(1)."""
    k = self.clave(v)
    if k in self._ady:
      return False
    self._objetos[k] = v
    self._ady[k] = {}
    return True

  def _clave_existente(self, v):
    k = self.clave(v)
    if k not in self._ady:
      raise ValueError(f"el vertice {k!r} no esta en el grafo")
    return k

  # --- aristas -----------------------------------------------------------------

  def agregar_arista(self, a, b, peso=1):
    """Conecta a con b (y b con a si el grafo no es dirigido). O(1).

    Si la arista ya existe solo se actualiza el peso. Los dos vertices tienen
    que estar en el grafo y no pueden ser el mismo (no hay lazos).
    """
    ka = self._clave_existente(a)
    kb = self._clave_existente(b)
    if ka == kb:
      raise ValueError("no se permiten aristas de un vertice consigo mismo")
    nueva = kb not in self._ady[ka]
    self._ady[ka][kb] = peso
    if not self.dirigido:
      self._ady[kb][ka] = peso
    if nueva:
      self._aristas += 1

  def existe_arista(self, a, b):
    """True si hay arista a -> b. O(1) en promedio."""
    ka, kb = self.clave(a), self.clave(b)
    return ka in self._ady and kb in self._ady[ka]

  def peso(self, a, b):
    """Peso de la arista a -> b, o None si no existe. O(1) en promedio."""
    ka, kb = self.clave(a), self.clave(b)
    if ka not in self._ady:
      return None
    return self._ady[ka].get(kb)

  def vecinos(self, v):
    """Lista de (vecino, peso) del vertice v. O(grado(v)).

    Devuelve una lista nueva: modificarla no cambia el grafo.
    """
    k = self._clave_existente(v)
    return [(self._objetos[kv], p) for kv, p in self._ady[k].items()]

  def grado(self, v):
    """Cantidad de vecinos de v. O(1)."""
    return len(self._ady[self._clave_existente(v)])

  def aristas(self):
    """Lista de (a, b, peso). En un grafo no dirigido cada arista aparece una vez."""
    resultado = []
    vistos = set()
    for ka, vecinos in self._ady.items():
      for kb, p in vecinos.items():
        if not self.dirigido:
          if (kb, ka) in vistos:
            continue
          vistos.add((ka, kb))
        resultado.append((self._objetos[ka], self._objetos[kb], p))
    return resultado

  def densidad(self):
    """Aristas presentes / aristas posibles (0 = ninguna, 1 = grafo completo)."""
    v = len(self._ady)
    if v < 2:
      return 0.0
    posibles = v * (v - 1) if self.dirigido else v * (v - 1) / 2
    return self._aristas / posibles
