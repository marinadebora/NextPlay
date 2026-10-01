"""Punto de entrada de NextPlay."""
from servicios.index import cargar_juegos
from ui.index import iniciar
from ui.menu import MENU_MAIN as MENU
from ui.version2 import iniciar_version2


def main():
    juegos = cargar_juegos()
    print("Bienvenido a NextPlay!")
    print(MENU)
    opcion = input("Elegi una opcion: ").strip()
    if opcion == "1":
        print("Iniciando version 1.0...")
        iniciar(juegos)
    if opcion == "2":
        print("Iniciando version 2.0...")
        iniciar_version2(juegos)
    if opcion == "0":
        print("Hasta la proxima!")
        return
    else:
        print("Opcion invalida. Saliendo del programa.")
        return

if __name__ == "__main__":
    main()
