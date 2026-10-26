from ui.menu import MENU, MENU_NOMBRE, MENU_FILTRO_V4
from algoritmos import crear_arboles, filtrar, busqueda_por_nombre, detalle, comparar_2_videoGames,listar_todos,mostrar_ranking
def iniciar_version_4(juegos):
  arboles = crear_arboles(juegos)
    
  while True:
    mostrar_ranking(juegos)
    print(MENU)
    try:
      opcion = input("Elegí una opción: ").strip()

      if opcion == "1":
        busqueda_por_nombre(MENU_NOMBRE, arboles, juegos)
 
      elif opcion == "2":
        listar_todos(arboles)
  
      elif opcion == "3":
       filtrar(MENU_FILTRO_V4, arboles)
  
      elif opcion == "4":
        detalle(arboles)
  
      elif opcion == "5":
        comparar_2_videoGames(arboles)

      elif opcion == "0":
        print("Hasta la proxima!")
        break
      else:
        print("Entrada inválida. Ingresá un número.")

    except ValueError:
      print("Entrada inválida. Ingresá un número.")
