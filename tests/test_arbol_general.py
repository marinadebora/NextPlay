"""Pruebas del arbol general de categorias (TP5)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modelos.VideoGames import VideoJuego
from algoritmos.construir_arbol_general import construir_arbol_general
from servicios.index import cargar_juegos


def _juego(id_, name, plataformas, generos):
    return VideoJuego(
        id_=id_,
        name=name,
        img="",
        release_date="2020-01-01",
        rating=4.0,
        platform=plataformas,
        genres=generos,
    )


# Catalogo chico y conocido. Dos generos (Action y RPG); "A" esta en los dos.
A = _juego(1, "A", ["PC"], ["Action", "RPG"])
B = _juego(2, "B", ["PC", "Xbox One"], ["Action"])
C = _juego(3, "C", ["Xbox One"], ["RPG"])
JUEGOS = [A, B, C]


def _arbol_generos():
    return construir_arbol_general("genres", JUEGOS)


# --- construccion ------------------------------------------------------------

def test_raiz_es_el_criterio_y_sus_hijos_son_las_categorias():
    arbol = _arbol_generos()
    assert arbol.raiz.valor == "genres"
    assert [n.valor for n in arbol.raiz.hijos] == ["Action", "RPG"]


def test_un_juego_con_dos_generos_aparece_en_las_dos_categorias():
    arbol = _arbol_generos()
    action = [n.valor for n in arbol.buscar_por_categoria("Action")]
    rpg = [n.valor for n in arbol.buscar_por_categoria("RPG")]
    assert action == [A, B]
    assert rpg == [A, C]


def test_se_reutiliza_el_nodo_de_cada_categoria():
    arbol = _arbol_generos()
    # 2 categorias aunque haya 3 juegos y 4 pertenencias (A->2, B->1, C->1).
    assert len(arbol.raiz.hijos) == 2
    assert len(arbol.categorias) == 2


def test_arbol_por_plataforma():
    arbol = construir_arbol_general("platform", JUEGOS)
    assert arbol.raiz.valor == "platform"
    assert [n.valor for n in arbol.buscar_por_categoria("PC")] == [A, B]
    assert [n.valor for n in arbol.buscar_por_categoria("Xbox One")] == [B, C]


# --- busqueda ----------------------------------------------------------------

def test_buscar_categoria_inexistente_da_none():
    assert _arbol_generos().buscar_por_categoria("Racing") is None


def test_arbol_sin_juegos():
    arbol = construir_arbol_general("genres", [])
    assert arbol.buscar_por_categoria("Action") is None
    assert arbol.preorder() == ["genres"]


# --- recorridos --------------------------------------------------------------
# Arbol de los datos de arriba:
#
#   genres
#   |- Action -> A, B
#   |- RPG    -> A, C

def test_preorder_visita_primero_la_raiz_y_cada_categoria_con_sus_juegos():
    assert _arbol_generos().preorder() == ["genres", "Action", A, B, "RPG", A, C]


def test_postorder_visita_los_hijos_antes_que_el_padre():
    assert _arbol_generos().postorder() == [A, B, "Action", A, C, "RPG", "genres"]


def test_por_nivel_recorre_nivel_por_nivel():
    assert _arbol_generos().por_nivel() == ["genres", "Action", "RPG", A, B, A, C]


def test_inorder_primer_hijo_raiz_y_hijos_restantes():
    # Convencion para arboles generales: primer hijo, luego el nodo, luego el resto.
    assert _arbol_generos().inorder() == [A, "Action", B, "genres", A, "RPG", C]


def test_todos_los_recorridos_visitan_la_misma_cantidad_de_nodos():
    arbol = _arbol_generos()
    # 1 raiz + 2 categorias + 4 pertenencias de juego = 7 nodos.
    assert len(arbol.preorder()) == 7
    assert len(arbol.inorder()) == 7
    assert len(arbol.postorder()) == 7
    assert len(arbol.por_nivel()) == 7


# --- con el catalogo real ----------------------------------------------------

def test_catalogo_real_cada_juego_esta_en_todas_sus_categorias():
    juegos = cargar_juegos()
    arbol = construir_arbol_general("genres", juegos)
    for juego in juegos:
        for genero in juego.genres:
            en_categoria = [n.valor for n in arbol.buscar_por_categoria(genero)]
            assert juego in en_categoria
    # Cantidad de nodos juego = suma de generos de todos los juegos.
    total_pertenencias = sum(len(j.genres) for j in juegos)
    assert sum(len(n.hijos) for n in arbol.raiz.hijos) == total_pertenencias


def test_el_arbol_devuelve_lo_mismo_que_el_filtro_lineal():
    from servicios.index import filtrar
    juegos = cargar_juegos()
    arbol = construir_arbol_general("genres", juegos)
    for genero in arbol.categorias:
        con_arbol = sorted(n.valor.name for n in arbol.buscar_por_categoria(genero))
        con_filtro = sorted(j.name for j in filtrar(juegos, genero=genero))
        assert con_arbol == con_filtro, genero


if __name__ == "__main__":
    test_raiz_es_el_criterio_y_sus_hijos_son_las_categorias()
    test_un_juego_con_dos_generos_aparece_en_las_dos_categorias()
    test_se_reutiliza_el_nodo_de_cada_categoria()
    test_arbol_por_plataforma()
    test_buscar_categoria_inexistente_da_none()
    test_arbol_sin_juegos()
    test_preorder_visita_primero_la_raiz_y_cada_categoria_con_sus_juegos()
    test_postorder_visita_los_hijos_antes_que_el_padre()
    test_por_nivel_recorre_nivel_por_nivel()
    test_inorder_primer_hijo_raiz_y_hijos_restantes()
    test_todos_los_recorridos_visitan_la_misma_cantidad_de_nodos()
    test_catalogo_real_cada_juego_esta_en_todas_sus_categorias()
    test_el_arbol_devuelve_lo_mismo_que_el_filtro_lineal()
    print("Todas las pruebas del arbol general pasaron OK")
