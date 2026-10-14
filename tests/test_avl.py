"""Pruebas del arbol AVL y de la altura del BST (TP4)."""
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modelos.VideoGames import VideoJuego
from estructuras.arbol_avl import Arbol as ArbolAVL
from estructuras.arbol_busqueda_nombre import Arbol as ArbolBST


def _juego(name):
    return VideoJuego(
        id_=1,
        name=name,
        img="",
        release_date="2020-01-01",
        rating=4.0,
        platform=["PC"],
        genres=["Action"],
    )


def _avl_con(nombres):
    arbol = ArbolAVL()
    for nombre in nombres:
        arbol.agregar(_juego(nombre))
    return arbol


def _verificar_balance(arbol, nodo):
    """Recorre todo el arbol y comprueba que cada nodo cumple la regla del AVL:
    |factor de balance| <= 1, y que la altura guardada en el nodo es la real."""
    if nodo is None:
        return 0
    altura_izq = _verificar_balance(arbol, nodo.izquierda)
    altura_der = _verificar_balance(arbol, nodo.derecha)
    assert abs(altura_izq - altura_der) <= 1, f"desbalanceado en {nodo.valor.name}"
    assert nodo.altura == 1 + max(altura_izq, altura_der), f"altura mal guardada en {nodo.valor.name}"
    return nodo.altura


# --- operaciones basicas ---------------------------------------------------------

def test_avl_agregar_y_buscar():
    arbol = _avl_con(["Zelda", "Mario", "Halo", "Portal", "Celeste"])
    for nombre in ["Zelda", "Mario", "Halo", "Portal", "Celeste"]:
        assert arbol.buscar(nombre).name == nombre


def test_avl_buscar_insensible_a_mayusculas():
    arbol = _avl_con(["Zelda", "Mario"])
    assert arbol.buscar("zElDa").name == "Zelda"


def test_avl_buscar_inexistente_da_none():
    arbol = _avl_con(["Zelda", "Mario"])
    assert arbol.buscar("No existe") is None


def test_avl_arbol_vacio():
    arbol = ArbolAVL()
    assert arbol.buscar("Zelda") is None
    assert arbol.altura() == 0
    assert arbol.inorder(arbol.raiz) == []


# --- las 4 rotaciones ------------------------------------------------------------
# En los 4 casos se insertan 3 nombres que dejarian el arbol como una "L"; despues
# de la rotacion la raiz tiene que ser el del medio ("b") con "a" y "c" de hijos.

def _verificar_forma_balanceada(arbol):
    assert arbol.raiz.valor.name == "b"
    assert arbol.raiz.izquierda.valor.name == "a"
    assert arbol.raiz.derecha.valor.name == "c"
    assert arbol.altura() == 2


def test_avl_rotacion_simple_derecha():       # caso izquierda-izquierda
    _verificar_forma_balanceada(_avl_con(["c", "b", "a"]))


def test_avl_rotacion_simple_izquierda():     # caso derecha-derecha
    _verificar_forma_balanceada(_avl_con(["a", "b", "c"]))


def test_avl_rotacion_doble_izquierda_derecha():   # caso izquierda-derecha
    _verificar_forma_balanceada(_avl_con(["c", "a", "b"]))


def test_avl_rotacion_doble_derecha_izquierda():   # caso derecha-izquierda
    _verificar_forma_balanceada(_avl_con(["a", "c", "b"]))


# --- propiedades del AVL ---------------------------------------------------------

def test_avl_inorder_siempre_esta_ordenado():
    nombres = [f"juego {n:03d}" for n in range(200)]
    random.Random(1).shuffle(nombres)
    arbol = _avl_con(nombres)
    resultado = [j.name for j in arbol.inorder(arbol.raiz)]
    assert resultado == sorted(nombres)


def test_avl_cumple_balance_con_orden_aleatorio():
    nombres = [f"juego {n:03d}" for n in range(300)]
    random.Random(2).shuffle(nombres)
    arbol = _avl_con(nombres)
    _verificar_balance(arbol, arbol.raiz)


def test_avl_con_nombres_ordenados_mantiene_altura_logaritmica():
    # El caso que destruye a un BST comun: todos los nombres entran ya ordenados.
    n = 1000
    arbol = _avl_con([f"juego {i:04d}" for i in range(n)])
    _verificar_balance(arbol, arbol.raiz)
    # Cota teorica de un AVL: altura < 1.44 * log2(n + 2).
    assert arbol.altura() <= 1.44 * math.log2(n + 2)


def test_avl_con_nombres_repetidos_sigue_balanceado():
    arbol = _avl_con(["a"] * 16)
    _verificar_balance(arbol, arbol.raiz)
    assert arbol.altura() <= 1.44 * math.log2(16 + 2)


# --- comparacion con el BST comun ------------------------------------------------

def test_bst_altura_arbol_vacio_y_con_un_nodo():
    arbol = ArbolBST()
    assert arbol.altura() == 0
    arbol.agregar(_juego("Zelda"))
    assert arbol.altura() == 1


def test_bst_con_nombres_ordenados_se_degenera_en_lista():
    n = 300
    bst = ArbolBST()
    for i in range(n):
        bst.agregar(_juego(f"juego {i:04d}"))
    assert bst.altura() == n          # una lista enlazada: un nivel por juego


def test_avl_es_mucho_mas_bajo_que_el_bst_con_los_mismos_datos():
    n = 300
    nombres = [f"juego {i:04d}" for i in range(n)]
    bst = ArbolBST()
    for nombre in nombres:
        bst.agregar(_juego(nombre))
    avl = _avl_con(nombres)
    assert avl.altura() < bst.altura() / 10
    # Ambos arboles tienen que encontrar lo mismo.
    assert bst.buscar("juego 0299").name == avl.buscar("juego 0299").name


if __name__ == "__main__":
    test_avl_agregar_y_buscar()
    test_avl_buscar_insensible_a_mayusculas()
    test_avl_buscar_inexistente_da_none()
    test_avl_arbol_vacio()
    test_avl_rotacion_simple_derecha()
    test_avl_rotacion_simple_izquierda()
    test_avl_rotacion_doble_izquierda_derecha()
    test_avl_rotacion_doble_derecha_izquierda()
    test_avl_inorder_siempre_esta_ordenado()
    test_avl_cumple_balance_con_orden_aleatorio()
    test_avl_con_nombres_ordenados_mantiene_altura_logaritmica()
    test_avl_con_nombres_repetidos_sigue_balanceado()
    test_bst_altura_arbol_vacio_y_con_un_nodo()
    test_bst_con_nombres_ordenados_se_degenera_en_lista()
    test_avl_es_mucho_mas_bajo_que_el_bst_con_los_mismos_datos()
    print("Todas las pruebas del AVL pasaron OK")
