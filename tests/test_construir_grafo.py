"""Pruebas de la construccion del grafo desde el catalogo (TP7)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from algoritmos.construir_grafo import construir_grafo, peso_de_relacion
from modelos.VideoGames import VideoJuego
from servicios.index import cargar_juegos

DATOS = Path(__file__).resolve().parent.parent / "datos"


def _juego(id_, generos, plataformas=("PC",)):
  return VideoJuego(id_=id_, name=f"Juego {id_}", img="", release_date="2020-01-01",
                    rating=4.0, platform=list(plataformas), genres=list(generos))


def _por_fuerza_bruta(juegos, minimo):
  """Referencia lenta: compara todos contra todos."""
  aristas = {}
  for i in range(len(juegos)):
    for k in range(i + 1, len(juegos)):
      if len(set(juegos[i].genres) & set(juegos[k].genres)) >= minimo:
        aristas[frozenset((juegos[i].id, juegos[k].id))] = peso_de_relacion(juegos[i], juegos[k])
  return aristas


def _aristas_del_grafo(grafo):
  return {frozenset((a.id, b.id)): p for a, b, p in grafo.aristas()}


# --- peso ----------------------------------------------------------------------

def test_peso_es_generos_mas_plataformas_en_comun():
  a = _juego(1, ["Action", "RPG", "Indie"], ["PC", "PS4", "Xbox"])
  b = _juego(2, ["Action", "RPG"], ["PC", "Xbox", "Switch"])
  assert peso_de_relacion(a, b) == 2 + 2
  assert peso_de_relacion(a, b) == peso_de_relacion(b, a)


# --- caso chico conocido -------------------------------------------------------

def test_caso_chico_con_aristas_conocidas():
  a = _juego(1, ["Action", "RPG"], ["PC"])
  b = _juego(2, ["Action", "RPG", "Indie"], ["PC", "PS4"])
  c = _juego(3, ["Action"], ["PS4"])
  d = _juego(4, ["Puzzle"], ["Switch"])
  g = construir_grafo([a, b, c, d], min_generos_comunes=2)
  assert g.cantidad_vertices() == 4
  assert g.cantidad_aristas() == 1
  assert g.existe_arista(a, b) and g.existe_arista(b, a)
  assert g.peso(a, b) == 2 + 1          # 2 generos + 1 plataforma (PC)
  assert g.grado(c) == 0 and g.grado(d) == 0


def test_con_minimo_1_alcanza_con_un_genero():
  a = _juego(1, ["Action"])
  b = _juego(2, ["Action", "RPG"])
  c = _juego(3, ["RPG"])
  g = construir_grafo([a, b, c], min_generos_comunes=1)
  assert g.existe_arista(a, b) and g.existe_arista(b, c)
  assert not g.existe_arista(a, c)
  assert g.cantidad_aristas() == 2


def test_juegos_con_menos_generos_que_el_minimo_quedan_aislados():
  a = _juego(1, ["Action"])
  b = _juego(2, ["Action"])
  g = construir_grafo([a, b], min_generos_comunes=2)
  assert g.cantidad_vertices() == 2
  assert g.cantidad_aristas() == 0


def test_catalogo_vacio_y_juegos_sin_generos():
  assert construir_grafo([]).cantidad_vertices() == 0
  g = construir_grafo([_juego(1, []), _juego(2, [])], min_generos_comunes=1)
  assert g.cantidad_vertices() == 2 and g.cantidad_aristas() == 0


def test_minimo_invalido():
  try:
    construir_grafo([_juego(1, ["Action"])], min_generos_comunes=0)
    assert False, "tendria que haber lanzado ValueError"
  except ValueError:
    pass


# --- contra la fuerza bruta con el catalogo real ---------------------------------

def test_igual_a_la_fuerza_bruta_con_el_catalogo_real():
  for archivo in ("VideoGames.JSON", "VideoGames1000.json"):
    juegos = cargar_juegos(DATOS / archivo)
    for minimo in (1, 2, 3, 4):
      grafo = construir_grafo(juegos, minimo)
      assert grafo.cantidad_vertices() == len(juegos)
      assert _aristas_del_grafo(grafo) == _por_fuerza_bruta(juegos, minimo), (archivo, minimo)


def test_el_grafo_es_simetrico_y_los_grados_suman_el_doble_de_aristas():
  juegos = cargar_juegos()
  g = construir_grafo(juegos)
  assert sum(g.grado(j) for j in juegos) == 2 * g.cantidad_aristas()
  for a, b, p in g.aristas():
    assert g.peso(b, a) == p


if __name__ == "__main__":
  pruebas = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
  for prueba in pruebas:
    prueba()
  print("Todas las pruebas de la construccion del grafo pasaron OK")
