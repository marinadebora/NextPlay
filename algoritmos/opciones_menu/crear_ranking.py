from estructuras.heap import Heap

def crear_ranking(juegos):
  ranking = Heap.desde_lista(juegos, prioridad, True  )
  return ranking

def prioridad(juego):
    return juego._rating

def mostrar_ranking(juegos):
  ranking = crear_ranking(juegos)
  top_5 = ranking.top_n(5)
  print("=========== NextPlay ===========")
  print("TOP 5 \n")
  dic_posicion = {1:"🥇", 2:"🥈",3:"🥉",4:" 4",5:" 5"}
  for indice,juego in enumerate(top_5, start=1):
      print(f"{dic_posicion[indice]} {juego._name: <35} {juego._rating}")
