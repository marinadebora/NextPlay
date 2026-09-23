import time
import random
from pathlib import Path

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


# ------------------------------------------------------------------------- #
# TP2 - Medicion de tiempos real (busqueda secuencial vs arbol de busqueda).
# ------------------------------------------------------------------------- #

# Carpeta datos/, para armar las rutas de los 3 catalogos de prueba.
DATOS_DIR = Path(__file__).resolve().parent.parent / "datos"

# Los 3 tamaños de entrada que pide la consigna del TP2.
DATASETS = {
	120: DATOS_DIR / "VideoGames.JSON",
	980: DATOS_DIR / "VideoGames1000.json",
	8980: DATOS_DIR / "VideoGames10.000.json",
}

# Nombre que no existe en ningun catalogo: fuerza el peor caso en ambas
# estrategias (recorrer toda la lista / llegar hasta una hoja del arbol).
NOMBRE_INEXISTENTE = "JUEGO INEXISTENTE PARA PEOR CASO XYZ"


def medir_tiempo(funcion_busqueda, *args, repeticiones=200):
	"""Corre 'funcion_busqueda(*args)' varias veces y devuelve el tiempo
	promedio de UNA busqueda, en segundos.

	Se repite muchas veces y se promedia porque una sola busqueda puede tardar
	microsegundos: medirla una sola vez mezclaria el tiempo de la busqueda con
	el "ruido" propio de medir (precision del reloj, otras tareas del SO, etc).
	"""
	inicio = time.perf_counter()
	for _ in range(repeticiones):
		funcion_busqueda(*args)
	fin = time.perf_counter()
	return (fin - inicio) / repeticiones


def benchmark(repeticiones=200, semilla=42):
	"""Mide, para cada tamaño de catalogo, el tiempo promedio de busqueda de
	la busqueda secuencial y del arbol de busqueda, en dos escenarios:

	- promedio: se busca un juego que SI esta en el catalogo, elegido al azar.
	- peor_caso: se busca un nombre que NO esta en el catalogo (obliga a
	  recorrer toda la lista en la secuencial, y a bajar hasta una hoja en
	  el arbol).

	Devuelve una lista de diccionarios, uno por tamaño de catalogo, lista
	para armar la tabla de resultados de docs/06-analisis-complejidad.md.
	"""
	random.seed(semilla)  # Para que el juego "al azar" sea reproducible entre corridas.
	resultados = []

	for tamaño, ruta in DATASETS.items():
		juegos = cargar_juegos(ruta)
		arbol_prueba = construir_arbol(juegos)

		nombre_existente = random.choice(juegos).name

		t_secuencial_prom = medir_tiempo(buscar_nombre_exacto, juegos, nombre_existente, repeticiones=repeticiones)
		t_arbol_prom = medir_tiempo(arbol_prueba.buscar, nombre_existente, repeticiones=repeticiones)

		t_secuencial_peor = medir_tiempo(buscar_nombre_exacto, juegos, NOMBRE_INEXISTENTE, repeticiones=repeticiones)
		t_arbol_peor = medir_tiempo(arbol_prueba.buscar, NOMBRE_INEXISTENTE, repeticiones=repeticiones)

		resultados.append({
			"tamaño": tamaño,
			"secuencial_promedio_ms": t_secuencial_prom * 1000,
			"arbol_promedio_ms": t_arbol_prom * 1000,
			"secuencial_peor_ms": t_secuencial_peor * 1000,
			"arbol_peor_ms": t_arbol_peor * 1000,
		})

	return resultados


def imprimir_tabla(resultados):
	"""Imprime los resultados del benchmark como tabla en formato Markdown."""
	print("| Tamaño catálogo | Secuencial (caso promedio) | Árbol (caso promedio) | Secuencial (peor caso) | Árbol (peor caso) |")
	print("|---|---|---|---|---|")
	for fila in resultados:
		print(
			f"| {fila['tamaño']} | {fila['secuencial_promedio_ms']:.5f} ms "
			f"| {fila['arbol_promedio_ms']:.5f} ms "
			f"| {fila['secuencial_peor_ms']:.5f} ms "
			f"| {fila['arbol_peor_ms']:.5f} ms |"
		)


if __name__ == "__main__":
	print(medir_tipos_de_busqueda("VISCERA CLEANUP DETAIL: SHADOW WARRIOR"))
	print()
	print("Midiendo tiempos de busqueda (esto puede tardar unos segundos)...")
	print()
	imprimir_tabla(benchmark())
