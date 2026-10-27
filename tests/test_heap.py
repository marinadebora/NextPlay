"""Pruebas de la heap binaria (TP6)."""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from estructuras.heap import Heap
from modelos.VideoGames import VideoJuego
from servicios.index import cargar_juegos


def _cumple_la_regla(heap):
  """Todo elemento tiene que ir antes (o empatar) con sus dos hijos."""
  n = len(heap.items)
  for i in range(n):
    for hijo in (2 * i + 1, 2 * i + 2):
      if hijo < n:
        assert not heap._va_antes(heap.items[hijo], heap.items[i]), f"se rompe la regla en {i}"


def _juego(id_, name, rating):
  return VideoJuego(id_=id_, name=name, img="", release_date="2020-01-01",
                    rating=rating, platform=["PC"], genres=["Action"])


# --- insertar / ver_raiz / extraer ---------------------------------------------

def test_heap_vacia():
  heap = Heap()
  assert heap.esta_vacia()
  assert len(heap) == 0
  assert heap.ver_raiz() is None
  assert heap.extraer() is None
  assert heap.top_n(5) == []


def test_insertar_deja_el_mayor_en_la_raiz():
  heap = Heap()
  for numero in [5, 3, 9, 1, 7]:
    heap.insertar(numero)
    _cumple_la_regla(heap)
  assert heap.ver_raiz() == 9
  assert len(heap) == 5


def test_ver_raiz_no_saca_nada():
  heap = Heap.desde_lista([4, 8, 2])
  assert heap.ver_raiz() == 8
  assert heap.ver_raiz() == 8
  assert len(heap) == 3


def test_extraer_devuelve_de_mayor_a_menor():
  datos = [5, 3, 9, 1, 7, 7, 2]
  heap = Heap.desde_lista(datos)
  salida = []
  while not heap.esta_vacia():
    salida.append(heap.extraer())
    _cumple_la_regla(heap)
  assert salida == sorted(datos, reverse=True)


def test_heap_de_minimos():
  heap = Heap(maximo=False)
  for numero in [5, 3, 9, 1, 7]:
    heap.insertar(numero)
  assert heap.ver_raiz() == 1
  assert [heap.extraer() for _ in range(5)] == [1, 3, 5, 7, 9]


def test_con_un_solo_elemento_y_con_repetidos():
  heap = Heap()
  heap.insertar(4)
  assert heap.extraer() == 4
  assert heap.extraer() is None
  for numero in [2, 2, 2]:
    heap.insertar(numero)
  assert [heap.extraer() for _ in range(3)] == [2, 2, 2]


# --- desde_lista ---------------------------------------------------------------

def test_desde_lista_cumple_la_regla_y_no_modifica_la_lista_original():
  datos = [random.Random(1).randint(0, 100) for _ in range(200)]
  copia = list(datos)
  heap = Heap.desde_lista(datos)
  _cumple_la_regla(heap)
  assert datos == copia
  assert len(heap) == 200
  assert heap.ver_raiz() == max(datos)


# --- top_n ---------------------------------------------------------------------

def test_top_n_coincide_con_ordenar_toda_la_lista():
  azar = random.Random(7)
  datos = [azar.randint(0, 50) for _ in range(300)]
  heap = Heap.desde_lista(datos)
  for n in (1, 5, 10, 50, 300):
    assert heap.top_n(n) == sorted(datos, reverse=True)[:n]


def test_top_n_no_modifica_la_heap():
  heap = Heap.desde_lista([5, 3, 9, 1, 7])
  antes = list(heap.items)
  heap.top_n(3)
  assert heap.items == antes
  assert len(heap) == 5


def test_top_n_casos_borde():
  heap = Heap.desde_lista([5, 3, 9])
  assert heap.top_n(0) == []
  assert heap.top_n(-2) == []
  assert heap.top_n(10) == [9, 5, 3]     # piden mas de los que hay: devuelve todos


def test_top_n_en_heap_de_minimos():
  heap = Heap.desde_lista([5, 3, 9, 1, 7], maximo=False)
  assert heap.top_n(3) == [1, 3, 5]


# --- con juegos ----------------------------------------------------------------

def test_ranking_de_juegos_por_rating():
  juegos = [_juego(1, "A", 3.5), _juego(2, "B", 4.8), _juego(3, "C", 4.1), _juego(4, "D", 2.0)]
  heap = Heap.desde_lista(juegos, clave=lambda j: j.rating)
  assert [j.name for j in heap.top_n(3)] == ["B", "C", "A"]


def test_catalogo_real_top_10_por_rating():
  juegos = cargar_juegos()
  heap = Heap.desde_lista(juegos, clave=lambda j: j.rating)
  top = heap.top_n(10)
  assert len(top) == 10
  ratings = [j.rating for j in top]
  assert ratings == sorted(ratings, reverse=True)
  # Los ratings del Top 10 son los mismos que si se ordena todo el catalogo.
  assert ratings == sorted((j.rating for j in juegos), reverse=True)[:10]


if __name__ == "__main__":
  test_heap_vacia()
  test_insertar_deja_el_mayor_en_la_raiz()
  test_ver_raiz_no_saca_nada()
  test_extraer_devuelve_de_mayor_a_menor()
  test_heap_de_minimos()
  test_con_un_solo_elemento_y_con_repetidos()
  test_desde_lista_cumple_la_regla_y_no_modifica_la_lista_original()
  test_top_n_coincide_con_ordenar_toda_la_lista()
  test_top_n_no_modifica_la_heap()
  test_top_n_casos_borde()
  test_top_n_en_heap_de_minimos()
  test_ranking_de_juegos_por_rating()
  test_catalogo_real_top_10_por_rating()
  print("Todas las pruebas de la heap pasaron OK")
