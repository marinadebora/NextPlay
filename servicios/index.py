"""Servicios (capa de orquestacion) de NextPlay.

Carga el catalogo desde datos/VideoGames.JSON y expone las operaciones
minimas que pide TP1: Buscar, Listar, Filtrar.
"""
import json
from pathlib import Path

from modelos.VideoGames import VideoJuego

DATA_PATH = Path(__file__).resolve().parent.parent / "datos" / "VideoGames.JSON"


def cargar_juegos(path: Path = DATA_PATH):
    """Carga el catalogo de juegos desde el JSON propio (importado una vez de RAWG)."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return [VideoJuego.from_dict(item) for item in data]


def buscar_por_nombre(juegos, nombre: str):
    """Busqueda parcial (case-insensitive) por nombre."""
    nombre = nombre.strip().lower()
    return [j for j in juegos if nombre in j.name.lower()]


def listar(juegos, orden: str = "name"):
    """Lista los juegos ordenados por 'name', 'rating' (descendente) o 'release_date'."""
    claves = {
        "name": lambda j: j.name.lower(),
        "rating": lambda j: -j.rating,
        "release_date": lambda j: j.release_date or "",
    }
    key = claves.get(orden, claves["name"])
    return sorted(juegos, key=key)


def filtrar(juegos, genero: str = None, plataforma: str = None, rating_min: float = None):
    """Filtra por genero y/o plataforma y/o rating minimo (todos opcionales, se combinan con AND)."""
    resultado = juegos
    if genero:
        resultado = [j for j in resultado if j.coincide_con_genero(genero)]
    if plataforma:
        resultado = [j for j in resultado if j.coincide_con_plataforma(plataforma)]
    if rating_min is not None:
        resultado = [j for j in resultado if j.rating >= rating_min]
    return resultado
