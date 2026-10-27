"""Punto de entrada de NextPlay."""
from servicios.index import cargar_juegos
from ui.index import iniciar
from ui.menu import MENU_MAIN as MENU
from ui.version2 import iniciar_version_2
from ui.version3 import iniciar_version_3
from ui.version4 import iniciar_version_4


def main():
    juegos = cargar_juegos()
    print("Bienvenido a NextPlay!")
    print(MENU)
    opcion = input("Elegi una opcion: ").strip()
    if opcion == "1":
        print("Iniciando version 1.0...")
        iniciar(juegos)
    elif opcion == "2":
        print("Iniciando version 2.0...")
        iniciar_version_2(juegos)
    elif opcion == "3":
        print("Iniciando version 3.0...")
        iniciar_version_3(juegos)
    elif opcion == "4":
        print("Iniciando version 4.0...")
        iniciar_version_4(juegos)
    
    elif opcion == "0":
        print("Hasta la proxima!")
        return
   

if __name__ == "__main__":
    main()
