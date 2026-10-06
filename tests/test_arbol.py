"""Pruebas del arbol binario de busqueda (TP3)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modelos.VideoGames import VideoJuego
from estructuras.arbol_busqueda_nombre import Arbol as ArbolNombre
from estructuras.arbol_busqueda_rating import Arbol as ArbolRating


def _juego(id_, name, rating):
    return VideoJuego(
        id_=id_,
        name=name,
        img="",
        release_date="2020-01-01",
        rating=rating,
        platform=["PC"],
        genres=["Action"],
    )


# Juegos de prueba, a proposito insertados en un orden que no es alfabetico
# (para no depender de que el arbol quede balanceado por casualidad).
JUEGOS = [
    _juego(1, "Zelda", 4.8),
    _juego(2, "Mario", 4.5),
    _juego(3, "Halo", 4.2),
    _juego(4, "Portal", 4.9),
    _juego(5, "Celeste", 4.7),
]


def _arbol_nombre_con_juegos():
    arbol = ArbolNombre()
    for juego in JUEGOS:
        arbol.agregar(juego)
    return arbol


# --- clave de ordenamiento: name -------------------------------------------------

def test_arbol_nombre_agregar_y_buscar():
    arbol = _arbol_nombre_con_juegos()
    for juego in JUEGOS:
        encontrado = arbol.buscar(juego.name)
        assert encontrado is not None, f"no se encontro '{juego.name}'"
        assert encontrado.name == juego.name


def test_arbol_nombre_buscar_insensible_a_mayusculas():
    arbol = _arbol_nombre_con_juegos()
    assert arbol.buscar("ZELDA") is not None
    assert arbol.buscar("zelda") is not None


def test_arbol_nombre_buscar_inexistente_da_none():
    arbol = _arbol_nombre_con_juegos()
    assert arbol.buscar("Juego Que No Existe") is None


def test_arbol_nombre_arbol_vacio():
    arbol = ArbolNombre()
    assert arbol.buscar("Zelda") is None
    assert arbol.inorder(arbol.raiz) == []


def test_arbol_nombre_inorder_da_orden_alfabetico():
    arbol = _arbol_nombre_con_juegos()
    nombres_inorder = [j.name for j in arbol.inorder(arbol.raiz)]
    assert nombres_inorder == sorted((j.name for j in JUEGOS), key=str.lower)


def test_arbol_nombre_preorder_y_postorder_visitan_todos_los_nodos():
    arbol = _arbol_nombre_con_juegos()
    nombres_esperados = {j.name for j in JUEGOS}

    preorder = arbol.preorder(arbol.raiz)
    postorder = arbol.postorder(arbol.raiz)

    assert len(preorder) == len(JUEGOS)
    assert len(postorder) == len(JUEGOS)
    assert {j.name for j in preorder} == nombres_esperados
    assert {j.name for j in postorder} == nombres_esperados
    # En preorder la raiz es siempre el primer elemento visitado.
    assert preorder[0].name == arbol.raiz.valor.name
    # En postorder la raiz es siempre el ultimo elemento visitado.
    assert postorder[-1].name == arbol.raiz.valor.name


# --- clave de ordenamiento: rating ------------------------------------------------

def _arbol_rating_con_juegos():
    arbol = ArbolRating()
    for juego in JUEGOS:
        arbol.agregar(juego)
    return arbol


def test_arbol_rating_inorder_da_orden_ascendente_por_rating():
    arbol = _arbol_rating_con_juegos()
    ratings_inorder = [j.rating for j in arbol.inorder(arbol.raiz)]
    assert ratings_inorder == sorted(j.rating for j in JUEGOS)


def test_arbol_rating_buscar_desde_respeta_el_minimo():
    arbol = _arbol_rating_con_juegos()
    resultados = arbol.buscar_desde(4.6)
    assert all(j.rating >= 4.6 for j in resultados)
    assert {j.name for j in resultados} == {"Zelda", "Portal", "Celeste"}


if __name__ == "__main__":
    test_arbol_nombre_agregar_y_buscar()
    test_arbol_nombre_buscar_insensible_a_mayusculas()
    test_arbol_nombre_buscar_inexistente_da_none()
    test_arbol_nombre_arbol_vacio()
    test_arbol_nombre_inorder_da_orden_alfabetico()
    test_arbol_nombre_preorder_y_postorder_visitan_todos_los_nodos()
    test_arbol_rating_inorder_da_orden_ascendente_por_rating()
    test_arbol_rating_buscar_desde_respeta_el_minimo()
    print("Todas las pruebas del arbol pasaron OK")
