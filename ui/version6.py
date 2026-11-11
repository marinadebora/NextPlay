import time

from ui.menu import MENU_V6, MENU_NOMBRE, MENU_FILTRO_V4
from algoritmos import crear_arboles, filtrar, busqueda_por_nombre, detalle, comparar_2_videoGames,listar_todos,mostrar_ranking,prioridad, nuevo_ranking,construir_grafo,ver_videoGame_relacionados,caminos_entre_dos_videojuegos, explorar_conexiones,bfs

def iniciar_version_6(juegos):

  arboles = crear_arboles(juegos)
  if len(juegos) > 8000:
    grafo = construir_grafo(juegos, 3)
  elif len(juegos) > 120:
    grafo = construir_grafo(juegos, 3)
  else:
    grafo = construir_grafo(juegos)
  
  inicio = time.perf_counter()


  fin = time.perf_counter()

  print(f"Tiempo de construcción: {fin - inicio:.2f} segundos")
  vertices = list(grafo.vertices())

  aislados = 0
  conectados = 0

  for videojuego in vertices:
    if len(grafo.vecinos(videojuego)) == 0:
        aislados += 1
    else:
        conectados += 1

  print("Total de videojuegos:", len(vertices))
  print("Videojuegos aislados:", aislados)
  print("Videojuegos conectados:", conectados)

  for videojuego in vertices:
    if grafo.vecinos(videojuego):
        origen = videojuego
        break

  orden, distancias, padres = bfs(grafo, origen)

  print("Origen:", origen.name)
  print("Videojuegos alcanzables:", len(distancias))
  print("Distancia máxima:", max(distancias.values()))
  print("Distancias encontradas:", set(distancias.values()))
  sin_generos = sum(1 for juego in juegos if not juego.genres)

  print("Videojuegos sin géneros:", sin_generos)
  while True:
    mostrar_ranking(juegos,prioridad,True,5)
    print(MENU_V6)
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
      
      elif opcion == "6":
        nuevo_ranking(juegos)
      
      elif opcion =="7":
        ver_videoGame_relacionados(grafo, arboles["arbol_avl"])
      
      elif opcion == "8":
        caminos_entre_dos_videojuegos(arboles["arbol_avl"], grafo)
      
      elif opcion == "9":
        explorar_conexiones(arboles["arbol_avl"], grafo)
      
      elif opcion == "0":
        print("Hasta la proxima!")
        break
      
      else:
        print("Entrada inválida. Ingresá un número.")

    except ValueError:
      print("Entrada inválida. Ingresá un número.")