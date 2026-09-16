"""Punto de entrada de NextPlay."""
from servicios.index import cargar_juegos
from ui.index import iniciar


def main():
    juegos = cargar_juegos()
    iniciar(juegos)


if __name__ == "__main__":
    main()
