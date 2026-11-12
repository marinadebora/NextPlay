"""Pruebas de BFS y DFS sobre el grafo (TP8)."""
import random
import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from algoritmos.construir_grafo import construir_grafo
from algoritmos.recorridos_grafo import bfs, camino_mas_corto, dfs
from estructuras.grafo import Grafo
from servicios.index import cargar_juegos

DATOS = Path(__file__).resolve().parent.parent / "datos"


def _grafo(vertices, aristas):
  g = Grafo()
  for v in vertices:
    g.agregar_vertice(v)
  for a, b in aristas:
    g.agregar_arista(a, b)
  return g


def _es_preorden_dfs(g, orden):
  """True si `orden` es un preorden valido de DFS.

  En un DFS, cada vertice nuevo es un vecino sin visitar del ultimo vertice de
  la rama actual; si ese no tiene vecinos sin visitar, se retrocede por la rama.
  """
  visitados = {orden[0]}
  rama = [orden[0]]
  for v in orden[1:]:
    while rama and all(w in visitados for w, _ in g.vecinos(rama[-1])):
      rama.pop()
    if not rama or v in visitados or not g.existe_arista(rama[-1], v):
      return False
    visitados.add(v)
    rama.append(v)
  return True


def _alcanzables(g, origen):
  """Referencia independiente: expande por capas hasta que no hay nada nuevo."""
  alcanzados = {origen}
  frontera = {origen}
  distancias = {origen: 0}
  nivel = 0
  while frontera:
    nivel += 1
    siguiente = set()
    for v in frontera:
      for w, _ in g.vecinos(v):
        if w not in alcanzados:
          alcanzados.add(w)
          distancias[w] = nivel
          siguiente.add(w)
    frontera = siguiente
  return distancias


# Grafo de ejemplo:      A - B - C - D        E - F        G
#                         \_____________/
GRAFO_CHICO = ([*"ABCDEFG"], [("A", "B"), ("B", "C"), ("C", "D"), ("A", "D"), ("E", "F")])


# --- BFS -------------------------------------------------------------------------

def test_bfs_distancias_en_saltos():
  g = _grafo(*GRAFO_CHICO)
  orden, distancias, padres = bfs(g, "A")
  assert distancias == {"A": 0, "B": 1, "D": 1, "C": 2}
  assert padres["A"] is None
  assert padres["B"] == "A" and padres["D"] == "A"
  assert padres["C"] in ("B", "D")


def test_bfs_visita_por_niveles():
  g = _grafo(*GRAFO_CHICO)
  orden, distancias, _ = bfs(g, "A")
  assert orden[0] == "A"
  niveles = [distancias[v] for v in orden]
  assert niveles == sorted(niveles)      # nunca baja de nivel
  assert len(orden) == len(set(orden))   # sin repetidos


def test_bfs_no_sale_de_su_componente():
  g = _grafo(*GRAFO_CHICO)
  orden, distancias, _ = bfs(g, "A")
  assert set(orden) == {"A", "B", "C", "D"}
  assert "E" not in distancias and "G" not in distancias


def test_bfs_desde_un_vertice_aislado():
  g = _grafo(*GRAFO_CHICO)
  orden, distancias, padres = bfs(g, "G")
  assert orden == ["G"]
  assert distancias == {"G": 0}
  assert padres == {"G": None}


def test_bfs_con_ciclos_no_repite():
  g = _grafo([1, 2, 3], [(1, 2), (2, 3), (3, 1)])
  orden, distancias, _ = bfs(g, 1)
  assert sorted(orden) == [1, 2, 3]
  assert distancias == {1: 0, 2: 1, 3: 1}


def test_bfs_origen_inexistente():
  g = _grafo(*GRAFO_CHICO)
  try:
    bfs(g, "Z")
    assert False, "tendria que haber lanzado ValueError"
  except ValueError:
    pass


# --- camino mas corto ----------------------------------------------------------------

def test_camino_mas_corto_toma_el_atajo():
  g = _grafo(*GRAFO_CHICO)
  camino, distancia = camino_mas_corto(g, "A", "D")
  assert camino == ["A", "D"]            # directo, no A-B-C-D
  assert distancia == 1


def test_camino_mas_corto_de_varios_saltos():
  g = _grafo([1, 2, 3, 4, 5], [(1, 2), (2, 3), (3, 4), (4, 5)])
  camino, distancia = camino_mas_corto(g, 1, 5)
  assert camino == [1, 2, 3, 4, 5]
  assert distancia == 4
  camino_inverso, _ = camino_mas_corto(g, 5, 1)
  assert camino_inverso == [5, 4, 3, 2, 1]


def test_camino_mas_corto_mismo_origen_y_destino():
  g = _grafo(*GRAFO_CHICO)
  assert camino_mas_corto(g, "A", "A") == (["A"], 0)


def test_camino_mas_corto_sin_camino():
  g = _grafo(*GRAFO_CHICO)
  assert camino_mas_corto(g, "A", "E") is None
  assert camino_mas_corto(g, "A", "G") is None


def test_camino_mas_corto_con_vertices_inexistentes():
  g = _grafo(*GRAFO_CHICO)
  for args in (("Z", "A"), ("A", "Z")):
    try:
      camino_mas_corto(g, *args)
      assert False, "tendria que haber lanzado ValueError"
    except ValueError:
      pass


# --- DFS ---------------------------------------------------------------------------

def test_dfs_visita_toda_la_componente_sin_repetir():
  g = _grafo(*GRAFO_CHICO)
  orden = dfs(g, "A")
  assert orden[0] == "A"
  assert sorted(orden) == ["A", "B", "C", "D"]
  assert len(orden) == len(set(orden))
  assert sorted(dfs(g, "E")) == ["E", "F"]


def test_dfs_desde_un_vertice_aislado():
  g = _grafo(*GRAFO_CHICO)
  assert dfs(g, "G") == ["G"]


def test_dfs_baja_por_una_rama_antes_de_retroceder():
  #   1 - 2 - 4      DFS desde 1: 1, 2, 4 (baja por la rama) y recien despues 3
  #   |
  #   3
  g = _grafo([1, 2, 3, 4], [(1, 2), (1, 3), (2, 4)])
  assert dfs(g, 1) == [1, 2, 4, 3]


def test_dfs_caso_que_fallaba_si_se_marcaba_al_apilar():
  # Con este grafo, marcar los vecinos como visitados al apilarlos daba
  # 0, 6, 5, 2, 1, 4, 3: despues del 2 salta al 1, que no es vecino del 2.
  adyacencia = {0: [3, 6], 1: [4, 5], 2: [4, 5], 3: [4, 5], 4: [6], 5: [6]}
  aristas = [(a, b) for a, vecinos in adyacencia.items() for b in vecinos]
  g = _grafo(range(7), aristas)
  orden = dfs(g, 0)
  assert sorted(orden) == list(range(7))
  assert _es_preorden_dfs(g, orden), orden


def test_dfs_es_un_preorden_valido_en_grafos_al_azar():
  azar = random.Random(7)
  for _ in range(300):
    n = azar.randint(2, 9)
    aristas = [par for par in combinations(range(n), 2) if azar.random() < 0.35]
    g = _grafo(range(n), aristas)
    orden = dfs(g, 0)
    assert len(orden) == len(set(orden))
    assert set(orden) == set(_alcanzables(g, 0))
    assert _es_preorden_dfs(g, orden), (aristas, orden)


def test_dfs_origen_inexistente():
  g = _grafo(*GRAFO_CHICO)
  try:
    dfs(g, "Z")
    assert False, "tendria que haber lanzado ValueError"
  except ValueError:
    pass


def test_dfs_no_tiene_limite_de_recursion():
  # un camino de 5.000 vertices: una version recursiva superaria el limite de Python (1.000)
  n = 5000
  g = _grafo(range(n), [(i, i + 1) for i in range(n - 1)])
  assert dfs(g, 0) == list(range(n))
  assert bfs(g, 0)[1][n - 1] == n - 1


# --- BFS y DFS juntos, contra referencias independientes --------------------------------

def test_bfs_y_dfs_alcanzan_lo_mismo_y_bfs_da_la_distancia_minima():
  azar = random.Random(11)
  for _ in range(200):
    n = azar.randint(2, 10)
    aristas = [par for par in combinations(range(n), 2) if azar.random() < 0.25]
    g = _grafo(range(n), aristas)
    origen = azar.randrange(n)
    referencia = _alcanzables(g, origen)
    orden, distancias, _ = bfs(g, origen)
    assert distancias == referencia
    assert set(orden) == set(dfs(g, origen)) == set(referencia)


def test_con_el_catalogo_real():
  for archivo, minimo in (("VideoGames.JSON", 2), ("VideoGames1000.json", 4)):
    juegos = cargar_juegos(DATOS / archivo)
    g = construir_grafo(juegos, minimo)
    azar = random.Random(3)
    origenes = azar.sample(juegos, 8) + [max(juegos, key=g.grado)]
    for origen in origenes:
      referencia = _alcanzables(g, origen)
      orden, distancias, padres = bfs(g, origen)
      assert distancias == {g.clave(v): d for v, d in referencia.items()}
      assert set(dfs(g, origen)) == set(referencia)
      assert _es_preorden_dfs(g, dfs(g, origen))
      # el camino mas corto a cualquier alcanzable tiene la distancia de BFS y usa aristas reales
      for destino in azar.sample(list(referencia), min(5, len(referencia))):
        camino, distancia = camino_mas_corto(g, origen, destino)
        assert distancia == referencia[destino] == len(camino) - 1
        assert camino[0] is origen and camino[-1] is destino
        for a, b in zip(camino, camino[1:]):
          assert g.existe_arista(a, b)


if __name__ == "__main__":
  pruebas = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
  for prueba in pruebas:
    prueba()
  print("Todas las pruebas de BFS y DFS pasaron OK")
