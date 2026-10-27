from estructuras.heap import Heap

def crear_ranking(juegos,func,maximo):
  ranking = Heap.desde_lista(juegos, func, maximo )
  return ranking

def prioridad(juego):
    return juego._rating

def mostrar_ranking(juegos,func,maximo,n):
  ranking = crear_ranking(juegos,func,maximo)
  top_5 = ranking.top_n(n)
  print(f"\n=================== NextPlay ========= TOP {n} ===\n")
  dic_posicion = {1:"🥇", 2:"🥈",3:"🥉"}
  for indice,juego in enumerate(top_5, start=1):
      if indice <=3:
        print(f"{dic_posicion[indice]} {juego._name: <40} {juego._rating}")
      elif indice >=10:
        print(f"{indice} {juego._name: <40} {juego._rating}")
      else:
        print(f" {indice} {juego._name: <40} {juego._rating}")
  print("================================================")

