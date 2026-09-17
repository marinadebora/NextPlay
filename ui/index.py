"""Interfaz de terminal (CLI) de NextPlay."""
from servicios.index import buscar_por_nombre, listar, filtrar

MENU = """
=== NextPlay ===
1. Buscar videojuegos por nombre
2. Listar todos los videojuegos
3. Filtrar por genero / plataforma / rating minimo
4. Ver detalle de un videojuego
5. Comparar dos videojuegos
0. Salir
"""


def _mostrar(resultados):
    if not resultados:
        print("No se encontraron videojuegos.")
        return
    for juego in resultados:
        print(juego)


def _pedir_float_opcional(mensaje):
    valor = input(mensaje).strip()
    if not valor:
        return None
    try:
        return float(valor)
    except ValueError:
        print("Valor invalido, se ignora ese filtro.")
        return None


def iniciar(juegos):
    while True:
        print(MENU)
        opcion = input("Elegi una opcion: ").strip()

        if opcion == "1":
            nombre = input("Ingresa el nombre (o parte del nombre): ").strip()
            _mostrar(buscar_por_nombre(juegos, nombre))

        elif opcion == "2":
            _mostrar(listar(juegos, orden="rating"))

        elif opcion == "3":
            genero = input("Genero (enter para omitir): ").strip() or None
            plataforma = input("Plataforma (enter para omitir): ").strip() or None
            rating_min = _pedir_float_opcional("Rating minimo (enter para omitir): ")
            _mostrar(filtrar(juegos, genero=genero, plataforma=plataforma, rating_min=rating_min))

        elif opcion == "4":
            # TODO (Agustina): pedir nombre, buscar el juego exacto y mostrar TODOS sus datos
            # (name, rating, release_date, platform, genres) con formato lindo.
            pass

        elif opcion == "5":
            # TODO (Agustina): pedir dos nombres, buscar cada uno con buscar_por_nombre,
            # y mostrar cual tiene mejor rating (o avisar si no se encontro alguno).
            pass

        elif opcion == "0":
            print("Hasta la proxima!")
            break

        else:
            print("Opcion invalida.")
