from ui.menu import RANKING_ORDEN
from algoritmos.crear_ranking import mostrar_ranking, prioridad

def nuevo_ranking(juegos):
    try:
      valor = int(input("Ingresa un valor :").strip()) 
      if valor <= 100 and valor > 0:
        print(RANKING_ORDEN)
        opcion = int(input("Elegí una opción: ").strip())
        if opcion == 1:
          mostrar_ranking(juegos,prioridad,True,valor)
        elif opcion == 2:
          mostrar_ranking(juegos,prioridad,False,valor)
        elif opcion == 0:
          print("Volviendo al menu anteriror...")
        else:
          print("Elegí una opción correcta.")
      else:
        print("Entrada inválida. Ingresá un número menor que 100")
   
    except ValueError:
      print("Entrada inválida. Ingresá un número.")

  
