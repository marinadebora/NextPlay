"""Pruebas del grafo (TP7)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from estructuras.grafo import Grafo
from modelos.VideoGames import VideoJuego
from servicios.index import cargar_juegos


def _juego(id_, name="x", genres=("Action",)):
  return VideoJuego(id_=id_, name=name, img="", release_date="2020-01-01",
                    rating=4.0, platform=["PC"], genres=list(genres))


def _grafo_de_juegos(dirigido=False):
  return Grafo(clave=lambda j: j.id, dirigido=dirigido)


# --- grafo vacio y vertices --------------------------------------------------

def test_grafo_vacio():
  g = Grafo()
  assert g.cantidad_vertices() == 0
  assert g.cantidad_aristas() == 0
  assert len(g) == 0
  assert g.vertices() == []
  assert g.densidad() == 0.0
  assert g.aristas() == []


def test_agregar_vertice():
  g = Grafo()
  assert g.agregar_vertice("a") is True
  assert g.agregar_vertice("b") is True
  assert g.cantidad_vertices() == 2
  assert g.tiene_vertice("a")
  assert not g.tiene_vertice("z")
  assert sorted(g.vertices()) == ["a", "b"]


def test_vertice_repetido_no_se_duplica():
  g = Grafo()
  assert g.agregar_vertice("a") is True
  assert g.agregar_vertice("a") is False
  assert g.cantidad_vertices() == 1


def test_vertice_sin_aristas_no_tiene_vecinos():
  g = Grafo()
  g.agregar_vertice("a")
  assert g.vecinos("a") == []
  assert g.grado("a") == 0


# --- aristas -----------------------------------------------------------------

def test_arista_no_dirigida_va_en_los_dos_sentidos():
  g = Grafo()
  g.agregar_vertice("a")
  g.agregar_vertice("b")
  g.agregar_arista("a", "b", 3)
  assert g.existe_arista("a", "b")
  assert g.existe_arista("b", "a")
  assert g.peso("a", "b") == 3
  assert g.peso("b", "a") == 3
  assert g.cantidad_aristas() == 1


def test_arista_dirigida_va_en_un_solo_sentido():
  g = Grafo(dirigido=True)
  g.agregar_vertice("a")
  g.agregar_vertice("b")
  g.agregar_arista("a", "b", 2)
  assert g.existe_arista("a", "b")
  assert not g.existe_arista("b", "a")
  assert g.peso("b", "a") is None
  assert g.vecinos("b") == []
  assert g.cantidad_aristas() == 1


def test_peso_por_defecto_es_1():
  g = Grafo()
  g.agregar_vertice("a")
  g.agregar_vertice("b")
  g.agregar_arista("a", "b")
  assert g.peso("a", "b") == 1


def test_arista_repetida_actualiza_el_peso_sin_duplicar():
  g = Grafo()
  g.agregar_vertice("a")
  g.agregar_vertice("b")
  g.agregar_arista("a", "b", 1)
  g.agregar_arista("b", "a", 5)
  assert g.cantidad_aristas() == 1
  assert g.peso("a", "b") == 5
  assert g.peso("b", "a") == 5
  assert g.grado("a") == 1


def test_arista_inexistente():
  g = Grafo()
  g.agregar_vertice("a")
  g.agregar_vertice("b")
  assert not g.existe_arista("a", "b")
  assert g.peso("a", "b") is None
  # preguntar por un vertice que no esta no rompe
  assert not g.existe_arista("a", "z")
  assert g.peso("z", "a") is None


def test_errores_con_vertices_que_no_estan():
  g = Grafo()
  g.agregar_vertice("a")
  for accion in (lambda: g.agregar_arista("a", "z"),
                 lambda: g.agregar_arista("z", "a"),
                 lambda: g.vecinos("z"),
                 lambda: g.grado("z")):
    try:
      accion()
      assert False, "tendria que haber lanzado ValueError"
    except ValueError:
      pass
  assert g.cantidad_aristas() == 0


def test_no_se_permiten_lazos():
  g = Grafo()
  g.agregar_vertice("a")
  try:
    g.agregar_arista("a", "a")
    assert False, "tendria que haber lanzado ValueError"
  except ValueError:
    pass
  assert g.cantidad_aristas() == 0


# --- vecinos, grados, aristas y densidad --------------------------------------

def test_vecinos_y_grados():
  g = Grafo()
  for v in "abcd":
    g.agregar_vertice(v)
  g.agregar_arista("a", "b", 1)
  g.agregar_arista("a", "c", 2)
  g.agregar_arista("a", "d", 3)
  assert sorted(g.vecinos("a")) == [("b", 1), ("c", 2), ("d", 3)]
  assert g.grado("a") == 3
  assert g.grado("b") == 1
  assert g.vecinos("b") == [("a", 1)]


def test_vecinos_devuelve_una_copia():
  g = Grafo()
  g.agregar_vertice("a")
  g.agregar_vertice("b")
  g.agregar_arista("a", "b")
  lista = g.vecinos("a")
  lista.clear()
  assert g.vecinos("a") == [("b", 1)]


def test_aristas_no_dirigidas_aparecen_una_vez():
  g = Grafo()
  for v in "abc":
    g.agregar_vertice(v)
  g.agregar_arista("a", "b", 1)
  g.agregar_arista("b", "c", 2)
  lista = g.aristas()
  assert len(lista) == 2
  assert {frozenset((x, y)): p for x, y, p in lista} == {frozenset("ab"): 1, frozenset("bc"): 2}


def test_aristas_dirigidas():
  g = Grafo(dirigido=True)
  for v in "ab":
    g.agregar_vertice(v)
  g.agregar_arista("a", "b", 1)
  g.agregar_arista("b", "a", 2)
  assert sorted(g.aristas()) == [("a", "b", 1), ("b", "a", 2)]
  assert g.cantidad_aristas() == 2


def test_densidad():
  g = Grafo()
  for v in "abcd":
    g.agregar_vertice(v)
  assert g.densidad() == 0.0
  g.agregar_arista("a", "b")
  assert g.densidad() == 1 / 6          # 1 de 6 aristas posibles
  for x, y in (("a", "c"), ("a", "d"), ("b", "c"), ("b", "d"), ("c", "d")):
    g.agregar_arista(x, y)
  assert g.densidad() == 1.0            # grafo completo


# --- con objetos del dominio ---------------------------------------------------

def test_vertices_son_juegos_identificados_por_id():
  g = _grafo_de_juegos()
  a, b, c = _juego(1, "A"), _juego(2, "B"), _juego(3, "C")
  for j in (a, b, c):
    g.agregar_vertice(j)
  g.agregar_arista(a, b, 2)
  g.agregar_arista(a, c, 5)
  # un juego distinto con el mismo id es el mismo vertice
  assert g.agregar_vertice(_juego(1, "otro nombre")) is False
  assert g.existe_arista(b, a)
  vecinos = dict((j.name, p) for j, p in g.vecinos(a))
  assert vecinos == {"B": 2, "C": 5}
  # los vecinos son los objetos originales, no copias
  assert any(j is b for j, _ in g.vecinos(a))


def test_con_el_catalogo_real():
  juegos = cargar_juegos()
  g = _grafo_de_juegos()
  for j in juegos:
    g.agregar_vertice(j)
  assert g.cantidad_vertices() == len(juegos)
  # conectar cada juego con el siguiente y verificar la simetria
  for a, b in zip(juegos, juegos[1:]):
    g.agregar_arista(a, b, 1)
  assert g.cantidad_aristas() == len(juegos) - 1
  assert sum(g.grado(j) for j in juegos) == 2 * g.cantidad_aristas()
  for a, b, p in g.aristas():
    assert g.existe_arista(b, a)


if __name__ == "__main__":
  pruebas = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
  for prueba in pruebas:
    prueba()
  print("Todas las pruebas del grafo pasaron OK")
