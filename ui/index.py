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
            nombre = input("Ingresa el nombre del videojuego: ").strip()
            resultados = buscar_por_nombre(juegos, nombre)

            if not resultados:
                print("No se encontro ningun videojuego con ese nombre.")
            else:
                juego = resultados[0]
                generos = ", ".join(juego.genres)
                plataformas = ", ".join(juego.platform)

                print("\n--- Detalle del videojuego ---")
                print(f"Nombre: {juego.name}")
                print(f"Rating: {juego.rating}")
                print(f"Fecha de lanzamiento: {juego.release_date}")
                print(f"Plataformas: {plataformas}")
                print(f"Generos: {generos}")

        elif opcion == "5":
            nombre1 = input("Nombre del primer videojuego: ").strip()
            nombre2 = input("Nombre del segundo videojuego: ").strip()

            resultado1 = buscar_por_nombre(juegos, nombre1)
            resultado2 = buscar_por_nombre(juegos, nombre2)

            if not resultado1 or not resultado2:
                if not resultado1:
                    print(f"No se encontro '{nombre1}'.")
                if not resultado2:
                    print(f"No se encontro '{nombre2}'.")
            else:
                juego1 = resultado1[0]
                juego2 = resultado2[0]

                print(f"\n{juego1.name}: rating {juego1.rating}")
                print(f"{juego2.name}: rating {juego2.rating}")

                if juego1.rating > juego2.rating:
                    print(f"\n{juego1.name} tiene mejor rating.")
                elif juego2.rating > juego1.rating:
                    print(f"\n{juego2.name} tiene mejor rating.")
                else:
                    print("\nEstan empatados en rating.")

        elif opcion == "0":
            print("Hasta la proxima!")
            break

        else:
            print("Opcion invalida.")
