from estructuras.arbol_genral import Arbol as Arbol_general

# recibe por parametro jerarquia (genres o platform) que sera la raiz y la lista de videogames
def construir_arbol_general(jerarquia ,juegos):
  arbol = Arbol_general(jerarquia)
  for juego in juegos:
    arbol.agregar_hijo(juego) 
  return arbol

def buscar_por_categoria (arbol, categoria):
  resultado = arbol.buscar_por_categoria(categoria)
  if resultado is not None:
    print(f"Resultsdo de la busqueda por categoria: {categoria}")
    for nodo in resultado:
        print(nodo.valor)
  else:
    print("No se encontraron resultados")

def retorna_categoria(arbol, categoria):
  lista_games=[]
  resultado = arbol.buscar_por_categoria(categoria)
  if resultado is not None:
    for nodo in resultado:
      lista_games.append(nodo.valor)
  else:
    return {"respuesta":[],"msg":"No se encontraron resultados "}
  return {"respuesta":lista_games, "msg":"Resultsdo de la busqueda por categoria: "}