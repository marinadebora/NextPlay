# TP8 — Recorridos del grafo: BFS y DFS (versión 6)

Este documento describe los dos recorridos que se incorporaron en el TP8 sobre el grafo de juegos relacionados (ver [`docs/10-grafo.md`](./10-grafo.md)): qué hace cada uno, qué consulta real resuelve en la aplicación, qué complejidad tienen, cuánto tardan medidos con los tres catálogos y cuándo conviene usar cada uno.

Código involucrado:

| Archivo | Qué es |
|---|---|
| `algoritmos/recorridos_grafo.py` | `bfs`, `camino_mas_corto` y `dfs`. |
| `algoritmos/opciones_menu/caminos_entre_games.py` | Opción 8 de la versión 6: camino más corto entre dos juegos (BFS). |
| `algoritmos/opciones_menu/explorar_coneccion.py` | Opción 9 de la versión 6: explorar conexiones (DFS). |
| `ui/version6.py` | Versión 6 de la aplicación. |
| `tests/test_recorridos_grafo.py` | Pruebas de los recorridos. |

## 1. Qué hace cada algoritmo

Se usa este grafo de ejemplo (no dirigido; cada letra es un juego y cada línea una relación):

```text
A ─── B ─── C
│           │
└────── D ──┘          E ─── F          G
```

(A–B, B–C, C–D, A–D, E–F; G no tiene vecinos.)

### BFS (búsqueda en anchura)

Visita primero todos los vecinos del origen, después los vecinos de esos vecinos, y así por **niveles**. Usa una **cola**: lo primero que se descubre es lo primero que se explora.

Desde A:

| Paso | Se saca de la cola | Se agregan | Cola después |
|---|---|---|---|
| 1 | A | B, D (distancia 1) | B, D |
| 2 | B | C (distancia 2) | D, C |
| 3 | D | — (A y C ya descubiertos) | C |
| 4 | C | — | vacía |

Resultado: orden A, B, D, C; distancias A=0, B=1, D=1, C=2. Además se guarda de qué vértice se llegó a cada uno (el "padre"), lo que permite reconstruir el camino. E, F y G no se visitan: no son alcanzables desde A.

### DFS (búsqueda en profundidad)

Sigue una rama hasta el fondo antes de retroceder y probar otra. Usa una **pila**: lo último que se descubre es lo primero que se explora.

Desde A (vecinos en el orden en que se agregaron las aristas): A → B → C → D. Cuando D no tiene más vecinos sin visitar, ya se recorrió toda la componente. El orden es A, B, C, D.

## 2. Casos de uso en la aplicación

### Caso 1 — BFS: camino más corto entre dos juegos (opción 8)

Pregunta: *¿cómo se llega del juego A al juego B pasando por juegos relacionados, con la menor cantidad de saltos?*

Se resuelve con `camino_mas_corto(grafo, origen, destino)`, que corre un BFS desde el origen y reconstruye el camino con los padres. Devuelve la lista de juegos y la cantidad de aristas, o `None` si no hay camino.

Ejemplo real (catálogo de 120 juegos, regla por defecto):

```text
POSTAL 2 → DEAD CELLS → SHADOWRUN RETURNS → AGE OF WONDERS III      (3 aristas de distancia)
```

**Por qué BFS:** como explora por niveles, la primera vez que alcanza el destino lo hace con la menor cantidad posible de aristas. Un DFS puede encontrar un camino, pero no tiene por qué ser el más corto.

### Caso 2 — DFS: explorar las conexiones de un juego (opción 9)

Pregunta: *¿qué juegos se pueden alcanzar siguiendo relaciones a partir de este?*

Se resuelve con `dfs(grafo, origen)`, que devuelve todos los juegos alcanzables en orden de visita. Ejemplo real: desde POSTAL 2 se alcanzan 95 juegos (en el catálogo de 120 hay 95 juegos conectados entre sí y 25 aislados).

**Por qué DFS:** acá no importa la distancia sino explorar todo lo que está conectado, y el DFS lo hace con una pila sencilla y sin guardar distancias ni padres. Para sólo obtener el conjunto de alcanzables un BFS daría el mismo resultado; se eligió DFS porque la consulta pide una exploración en profundidad, y porque así el trabajo queda repartido en dos algoritmos con usos distintos.

## 3. Cómo están implementados

- **Recorren la lista de adyacencia** con `grafo.vecinos(v)`, así que cada vértice cuesta O(grado).
- **Visitados:** un conjunto de claves (`id` del juego), con búsqueda y alta en O(1). Evita repetir vértices y que los ciclos hagan un bucle infinito.
- **BFS:** la cola es `collections.deque` (`popleft` en O(1)). Con una lista común, `pop(0)` cuesta O(n) y el recorrido dejaría de ser lineal.
- **DFS iterativo:** usa una pila explícita en lugar de recursión. Una versión recursiva fallaría con `RecursionError` en grafos con caminos de más de unos 1.000 vértices (el límite de Python); una prueba con un camino de 5.000 vértices lo verifica.
- **Cuándo se marca un vértice como visitado en el DFS:** al *sacarlo* de la pila, no al apilarlo. Si se marca al apilar, un paso del recorrido puede saltar a un vértice que no es vecino del último visitado, y eso ya no es un DFS (daba órdenes inválidos en cerca de 1 de cada 5 grafos de prueba). Hay una prueba que verifica que el orden devuelto es un preorden válido de DFS.
- **Errores:** si el origen (o el destino) no está en el grafo, lanzan `ValueError`.
- **No usan ninguna librería de grafos:** sólo `deque` como cola auxiliar.

## 4. Complejidad

V = vértices, E = aristas. Con lista de adyacencia:

| | BFS | DFS |
|---|---|---|
| Tiempo | O(V + E) | O(V + E) |
| Espacio | O(V): visitados, distancias, padres y cola | O(V + E) en el peor caso: puede haber vértices repetidos en la pila (uno por cada vecino visitado antes) |
| Mejor caso | O(1) si el origen no tiene vecinos | O(1) si el origen no tiene vecinos |
| Peor caso | Se recorre toda la componente: O(V + E) | Se recorre toda la componente: O(V + E) |

¿Por qué O(V + E)? Cada vértice se visita una sola vez (O(V)) y, al visitarlo, se recorren todos sus vecinos, así que cada arista se mira dos veces en un grafo no dirigido (O(E)). Con una matriz de adyacencia serían O(V²), porque habría que recorrer una fila completa por vértice.

`camino_mas_corto` es un BFS más la reconstrucción del camino (proporcional a su largo) y el armado de un diccionario con los vértices (O(V)): en total O(V + E).

## 5. Mediciones

Con `perf_counter`, promedio de varias repeticiones, desde el juego con más relaciones. "Todo el grafo" es un DFS desde cada componente, o sea que recorre los V vértices y las E aristas.

| Catálogo y regla | V | E | Alcanzables | BFS | DFS | Camino más corto | Todo el grafo | µs por (V + E) |
|---|---|---|---|---|---|---|---|---|
| 120 juegos, ≥ 2 géneros | 120 | 1.256 | 95 | 0,28 ms | 0,31 ms | 0,24 ms | 0,33 ms | 0,24 |
| 980 juegos, ≥ 4 géneros | 980 | 1.685 | 171 | 0,35 ms | 0,46 ms | 0,42 ms | 0,94 ms | 0,35 |
| 980 juegos, ≥ 3 géneros | 980 | 15.185 | 454 | 3,1 ms | 4,1 ms | 3,0 ms | 4,2 ms | 0,26 |
| 8.980 juegos, ≥ 4 géneros | 8.980 | 203.541 | 1.902 | 38 ms | 52 ms | 42 ms | 63 ms | 0,30 |
| 8.980 juegos, ≥ 3 géneros | 8.980 | 1.539.052 | 4.319 | 310 ms | 428 ms | 349 ms | 454 ms | 0,29 |

Lectura:

- La última columna es casi constante (entre 0,24 y 0,35 µs) aunque V + E crece más de 1.000 veces (de 1.376 a 1,5 millones). Es la señal de que el tiempo crece **linealmente** con V + E, como dice la teoría.
- En la máquina donde se midió, todas las consultas responden en menos de medio segundo, incluso con el catálogo de 8.980 juegos y 1,5 millones de aristas (en otra computadora los tiempos absolutos cambian, la proporción no).
- BFS y DFS tardan parecido; el DFS un poco más porque apila vértices que después descarta al sacarlos de la pila (ya habían sido visitados por otra rama).
- En el catálogo grande el grafo tiene "centros" (por ejemplo ROBLOX, relacionado con 4.318 juegos): desde ahí todo está a un solo salto. Es una característica de los datos, no del algoritmo.

## 6. Cuándo conviene cada uno

| Necesidad | Algoritmo |
|---|---|
| Camino con menos aristas entre dos juegos | **BFS** (explora por niveles) |
| Juegos a una cierta cantidad de saltos (recomendaciones de "segundo nivel") | **BFS** (distancias por nivel) |
| Explorar todo lo conectado a un juego | **DFS** (o BFS: devuelven el mismo conjunto) |
| Saber si dos juegos están en el mismo grupo, o separar el grafo en grupos aislados | **DFS** (o BFS) |
| Camino de menor *costo* considerando los pesos | Ninguno de los dos: haría falta Dijkstra (TP9) |

**Límite del camino más corto:** el BFS cuenta aristas e ignora el peso. "Más corto" acá significa "menos saltos", no "más parecido". Si hay varios caminos con la misma cantidad de saltos, devuelve uno de ellos.

## 7. Preguntas de defensa

- **¿Dónde se usa BFS? ¿Y DFS?** BFS en la opción 8 (camino más corto entre dos juegos) y DFS en la opción 9 (explorar conexiones). Ambos están en `algoritmos/recorridos_grafo.py`.
- **¿Qué complejidad tienen?** O(V + E) en tiempo los dos; se verificó midiendo con tres catálogos.
- **¿Por qué BFS da el camino más corto y DFS no?** El BFS explora por niveles: todos los vértices a distancia *k* antes que ninguno a distancia *k + 1*. El DFS se mete por una rama hasta el fondo y puede llegar al destino por un camino largo.
- **¿Por qué la cola en BFS y la pila en DFS?** La cola (primero en entrar, primero en salir) mantiene el orden por niveles; la pila (último en entrar, primero en salir) hace bajar por una rama.
- **¿Por qué el DFS es iterativo?** Para no depender del límite de recursión de Python en grafos con caminos largos.
- **¿Cuál es el espacio extra de cada uno?** BFS O(V); DFS O(V + E) en el peor caso por los repetidos en la pila.
- **¿Qué pasa si no hay camino?** `camino_mas_corto` devuelve `None` y la aplicación lo informa.
- **¿Y si el grafo fuera con matriz?** Cada recorrido costaría O(V²) en vez de O(V + E).
- **¿Qué cambia si se usa otra regla de conexión?** Cambian las aristas y por lo tanto los tiempos y los caminos, pero no los algoritmos.
