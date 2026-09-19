from servicios.index import cargar_juegos
from algoritmos.busqueda_secuencial import buscar_nombre_exacto
from algoritmos.construir_arbol import construir_arbol

# Este archivo debe ejecutarse desde la raíz del proyecto (NextPlay):
# python -m algoritmos.medicion

# Carga lista con todos los juegos 
lista = cargar_juegos()
# crea el arbol binario.
arbol =construir_arbol(lista)

# Desde esta funcion se continuara con la medicion y comparacion de tiempos.
# Esta funcion ejecuta las dos estrategias de busqueda para comparar sus resultados.
def medir_tipos_de_busqueda(nombre):

  busqueda_secuencial = buscar_nombre_exacto(lista,nombre)
  busqueda_arbol = arbol.buscar(nombre)

  return f'el juego {nombre} buscado de forma secuencial:{busqueda_secuencial}\nel juego {nombre} buscado en el arbol:{busqueda_arbol}'


print(medir_tipos_de_busqueda ("VISCERA CLEANUP DETAIL: SHADOW WARRIOR"))