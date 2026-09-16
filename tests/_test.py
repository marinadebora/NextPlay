"""Pruebas basicas de los servicios de NextPlay (TP1)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from servicios.index import cargar_juegos, buscar_por_nombre, listar, filtrar


def test_cargar_juegos():
    juegos = cargar_juegos()
    assert len(juegos) > 0, "El catalogo no deberia estar vacio"


def test_buscar_por_nombre():
    juegos = cargar_juegos()
    resultado = buscar_por_nombre(juegos, "the")
    assert all("the" in j.name.lower() for j in resultado)


def test_listar_por_rating_desc():
    juegos = cargar_juegos()
    ordenado = listar(juegos, orden="rating")
    ratings = [j.rating for j in ordenado]
    assert ratings == sorted(ratings, reverse=True)


def test_filtrar_por_genero():
    juegos = cargar_juegos()
    accion = filtrar(juegos, genero="Action")
    assert all(j.coincide_con_genero("Action") for j in accion)


def test_filtrar_por_rating_minimo():
    juegos = cargar_juegos()
    buenos = filtrar(juegos, rating_min=4.0)
    assert all(j.rating >= 4.0 for j in buenos)


if __name__ == "__main__":
    test_cargar_juegos()
    test_buscar_por_nombre()
    test_listar_por_rating_desc()
    test_filtrar_por_genero()
    test_filtrar_por_rating_minimo()
    print("Todas las pruebas pasaron OK")
