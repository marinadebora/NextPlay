# 06 — Análisis de complejidad: Búsqueda por nombre (TP2)

## 1. Operación crítica elegida

**Buscar un juego por nombre exacto en el catálogo.** Es una operación que se repite todo el tiempo (el usuario la usa desde el menú, y también es la base de otras funcionalidades futuras), así que tiene sentido comparar más de una forma de resolverla a medida que el catálogo crece.

Se comparan dos estrategias:

1. **Búsqueda secuencial** (`algoritmos/busqueda_secuencial.py`): recorre la lista de juegos de punta a punta comparando nombres, hasta encontrar una coincidencia exacta o llegar al final.
2. **Árbol binario de búsqueda (BST)** (`estructuras/arbol_busqueda_nombre.py` + `algoritmos/construir_arbol.py`): los juegos se ordenan alfabéticamente por nombre y se arma un árbol **balanceado** eligiendo siempre el elemento del medio como raíz de cada subárbol (en vez de insertarlos uno por uno en el orden en que vienen, que podría desbalancear el árbol). Buscar un nombre implica bajar por el árbol comparando y descartando una de las dos mitades en cada paso.

## 2. Metodología

La medición está implementada en `algoritmos/medicion.py`, función `benchmark()`. Para cada uno de los 3 catálogos de prueba:

- Se mide el **tiempo promedio de una búsqueda** corriendo la misma búsqueda 200 veces seguidas con `time.perf_counter()` y dividiendo el tiempo total por 200. Se promedia porque una sola búsqueda individual tarda microsegundos, un lapso tan chico que se mezclaría con el "ruido" propio de medir (precisión del reloj del sistema, otras tareas corriendo, etc.).
- Se mide en **dos escenarios**:
  - **Caso promedio**: se busca un juego elegido al azar que sí está en el catálogo.
  - **Peor caso**: se busca un nombre que no existe en ningún catálogo. Esto obliga a la secuencial a recorrer la lista completa, y al árbol a bajar hasta una hoja.
- El árbol se reconstruye una vez por cada tamaño de catálogo (con `construir_arbol`, que arma la versión balanceada), y ese mismo árbol se usa para las dos búsquedas de ese tamaño.

Se usan los 3 catálogos ya incorporados al repo por el equipo:

| Catálogo | Cantidad de juegos |
|---|---|
| `datos/VideoGames.JSON` | 120 |
| `datos/VideoGames1000.json` | 980 |
| `datos/VideoGames10.000.json` | 8.980 |

Para reproducir la medición: `python -m algoritmos.medicion` desde la raíz del repo.

## 3. Resultados

| Tamaño catálogo | Secuencial (caso promedio) | Árbol (caso promedio) | Secuencial (peor caso) | Árbol (peor caso) |
|---|---|---|---|---|
| 120 | 0.00819 ms | 0.00105 ms | 0.01209 ms | 0.00159 ms |
| 980 | 0.01387 ms | 0.00230 ms | 0.11920 ms | 0.00232 ms |
| 8.980 | 0.04235 ms | 0.00304 ms | 1.08530 ms | 0.00327 ms |

(Valores de una corrida de referencia; pueden variar levemente entre máquinas, pero la tendencia se mantiene siempre. Entorno usado: CPython 3, sin otras cargas corriendo en simultáneo.)

Dos cosas se ven claramente en la tabla:

- En el **peor caso**, el tiempo de la búsqueda secuencial crece casi en línea recta con el tamaño del catálogo: de 120 a 980 juegos (x8,2) el tiempo se multiplica por ~9,9; de 980 a 8.980 juegos (x9,2) el tiempo se multiplica por ~9,1. El tiempo del árbol, en cambio, apenas se mueve: pasa de 0,0016 ms a 0,0033 ms — se duplica, no se multiplica por 9, a pesar de que el catálogo creció casi 75 veces.
- En el **caso promedio** la diferencia es menos dramática (porque en promedio la secuencial no tiene que recorrer todo el catálogo, solo la mitad), pero la tendencia es la misma: la secuencial crece con el tamaño, el árbol prácticamente no.

## 4. Análisis teórico de complejidad

### 4.1 Búsqueda secuencial

Recorre la lista elemento por elemento comparando el nombre buscado contra `juego.name`, hasta encontrar coincidencia o llegar al final.

- **Mejor caso — Ω(1):** el juego buscado es el primero de la lista.
- **Peor caso — O(n):** el juego buscado es el último, o no está en el catálogo — hay que recorrer los `n` elementos.
- **Caso promedio — Θ(n):** en promedio hay que recorrer la mitad de la lista (`n/2`), que sigue siendo del orden de `n` (las constantes no cambian la clase de complejidad).

En cualquier caso que no sea "está al principio", el trabajo crece **linealmente** con la cantidad de juegos: duplicar el catálogo duplica (en el peor caso) el tiempo de búsqueda.

### 4.2 Árbol binario de búsqueda balanceado

En cada nodo se compara el nombre buscado contra el nombre del nodo y, según sea menor o mayor, se descarta una de las dos mitades del árbol y se sigue solo por la otra rama. Como el árbol se construye siempre a partir del elemento del medio (`construir_arbol`), queda balanceado: la altura del árbol es proporcional a `log₂(n)`.

- **Mejor caso — Ω(1):** el juego buscado es la raíz del árbol.
- **Peor caso — O(log n):** el juego buscado está en una de las hojas (o no existe), y hay que bajar por toda la altura del árbol, que en un árbol balanceado es `log₂(n)`.
- **Caso promedio — Θ(log n):** en promedio también es proporcional a la altura del árbol, por lo tanto del orden de `log₂(n)`.

**Importante:** esta complejidad logarítmica depende de que el árbol esté **balanceado**. Si los juegos se insertaran uno por uno con `Arbol.agregar()` en el orden en que ya vienen en el archivo (que no está ordenado alfabéticamente al azar, sino en el orden en que RAWG los devuelve), el árbol podría desbalancearse y degradar a O(n) en el peor caso, igual que la secuencial. Por eso `construir_arbol.py` arma el árbol a partir de la lista ya ordenada, eligiendo siempre el elemento central como raíz de cada subárbol — así se garantiza el balance y la complejidad logarítmica.

### 4.3 Por qué los tiempos medidos confirman el análisis teórico

`log₂(120) ≈ 6,9`, `log₂(980) ≈ 9,9`, `log₂(8.980) ≈ 13,1`. La razón entre estos valores (9,9/6,9 ≈ 1,4 y 13,1/9,9 ≈ 1,3) es muy parecida a la razón entre los tiempos medidos del árbol en el peor caso (0,00232/0,00159 ≈ 1,5 y 0,00327/0,00232 ≈ 1,4) — el crecimiento es logarítmico, tal como predice la teoría. En cambio, la razón entre los tiempos de la secuencial en el peor caso (0,1192/0,01209 ≈ 9,9 y 1,0853/0,1192 ≈ 9,1) es prácticamente igual a la razón entre los tamaños de los catálogos (980/120 ≈ 8,2 y 8.980/980 ≈ 9,2) — el crecimiento es lineal, también tal como predice la teoría.

## 5. Conclusión

Para un catálogo chico (120 juegos), ambas estrategias responden en fracciones de milisegundo — la diferencia no se nota en el uso real del programa, y la búsqueda secuencial es más que suficiente (además de más simple).

A medida que el catálogo crece, la búsqueda secuencial se vuelve cada vez más lenta de forma proporcional al tamaño del catálogo (O(n)), mientras que el árbol de búsqueda se mantiene prácticamente constante (O(log n)). Con el catálogo de referencia de la cátedra (creciendo desde cientos hasta miles de elementos), la diferencia ya es medible incluso con un catálogo de ~1.000 juegos, y se vuelve claramente significativa a partir de unos pocos miles de juegos (con 8.980 juegos, el peor caso de la secuencial ya es más de 300 veces más lento que el del árbol).

**Conviene usar el árbol de búsqueda balanceado en cuanto el catálogo deja de ser chico** (a partir de, aproximadamente, unos cientos de juegos en adelante), porque su ventaja crece exactamente en el escenario que más importa: cuando el catálogo es grande y la búsqueda se ejecuta muchas veces (por ejemplo, cada vez que un usuario busca un juego desde el menú). El costo de mantener el árbol (construirlo una vez, balanceado, a partir de la lista) es una inversión única que se paga sola apenas el catálogo supera un tamaño moderado.
