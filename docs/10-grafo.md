# TP7 — Grafo de juegos relacionados (versión 5)

Este documento describe el grafo que se incorporó en el TP7: qué representa cada vértice y cada arista, por qué es no dirigido y pesado, por qué se eligió lista de adyacencia, qué complejidad tienen sus operaciones y cómo se construye a partir del catálogo.

Código involucrado:

| Archivo | Qué es |
|---|---|
| `estructuras/grafo.py` | La clase `Grafo` (implementada a mano, lista de adyacencia). |
| `algoritmos/construir_grafo.py` | Arma el grafo a partir de los juegos cargados desde el JSON. |
| `tests/test_grafo.py` | Pruebas de la estructura. |
| `tests/test_construir_grafo.py` | Pruebas de la construcción (incluye comparación contra fuerza bruta). |

## 1. El modelo

| Pregunta | Respuesta |
|---|---|
| ¿Qué es un vértice? | Un videojuego del catálogo, identificado por su `id`. |
| ¿Qué es una arista? | Dos juegos están conectados si **comparten al menos 2 géneros** (el mínimo es un parámetro). |
| ¿Dirigido o no? | **No dirigido**: "se parece a" es simétrico. Si A se parece a B, B se parece a A. |
| ¿Pesado o no? | **Pesado**: el peso es la cantidad de géneros más la cantidad de plataformas que los dos juegos tienen en común. |
| ¿Representación? | **Lista de adyacencia** (un diccionario por vértice con sus vecinos). |

El flujo de datos es: JSON → objetos `VideoJuego` → `construir_grafo(juegos)` → `Grafo`.

El peso sirve para ordenar: dado un juego, los "más relacionados" son los vecinos de mayor peso (esa consulta se resuelve con el Top-N de la heap, ver sección 6). Que sea pesado también deja el grafo preparado para los recorridos del TP8.

## 2. Qué regla de conexión usar (y por qué depende del catálogo)

La regla de la arista determina cuán denso queda el grafo. Se midió con los tres catálogos qué porcentaje de todos los pares de juegos quedaría conectado:

| Comparten al menos… | 120 juegos | 980 juegos | 8.980 juegos |
|---|---|---|---|
| 1 género | 66 % | 63 % | 59 % |
| 2 géneros | 18 % | 21 % | 20 % |
| 3 géneros | 1 % | 3 % | 4 % |

Con **1 género** el grafo es casi completo: casi todo se parece a casi todo y no aporta información. Entre 2 y 3 géneros hay un compromiso:

| Catálogo y regla | Aristas | Juegos sin ningún vecino | Grado promedio | Tiempo de armado | Memoria del grafo |
|---|---|---|---|---|---|
| 120 juegos, ≥ 2 géneros | 1.256 | 25 de 120 | 20,9 | 0,011 s | 0,1 MB |
| 120 juegos, ≥ 3 géneros | 71 | **87 de 120** | 1,2 | 0,002 s | 0,0 MB |
| 980 juegos, ≥ 2 géneros | 99.073 | 147 de 980 | 202 | 0,83 s | 7,7 MB |
| 980 juegos, ≥ 3 géneros | 15.185 | 524 de 980 | 31 | 0,15 s | 1,3 MB |
| 8.980 juegos, ≥ 3 géneros | 1.539.052 | — | 343 | 16,4 s | 120 MB |
| 8.980 juegos, ≥ 4 géneros | 203.541 | — | 45 | 3,2 s | 16 MB |

(Con 8.980 juegos y ≥ 2 géneros habría unos 8 millones de aristas: no se construyó porque tardaría minutos y ocuparía cientos de MB.)

Conclusiones:

- Con el catálogo chico (120 juegos, el que carga la aplicación por defecto) pedir 3 géneros deja **87 de 120 juegos aislados**: el grafo no sirve para recomendar. Por eso el valor por defecto es **2 géneros**.
- Con catálogos grandes, 2 géneros produce demasiadas aristas; ahí se sube el mínimo a 3 o 4 (`construir_grafo(juegos, min_generos_comunes=3)`).
- La regla es un parámetro y no está "cableada" en la estructura: el `Grafo` no sabe qué significa una arista. El criterio vive en `algoritmos/construir_grafo.py`.

## 3. Lista de adyacencia vs. matriz de adyacencia

| | Lista de adyacencia | Matriz de adyacencia |
|---|---|---|
| Espacio | O(V + E) | O(V²) |
| ¿Existe la arista a–b? | O(1) con diccionarios | O(1) |
| Vecinos de un vértice | O(grado) | O(V) (recorrer toda la fila) |
| Recorrer todo el grafo (BFS/DFS, TP8) | O(V + E) | O(V²) |
| Agregar un vértice | O(1) | O(V²) (reconstruir la matriz) |

Celdas que ocuparía la matriz frente a las entradas de la lista (2·E, porque cada arista se guarda en los dos sentidos):

| Catálogo y regla | Matriz (V²) | Lista (2·E) |
|---|---|---|
| 120 juegos, ≥ 2 géneros | 14.400 | 2.512 |
| 980 juegos, ≥ 2 géneros | 960.400 | 198.146 |
| 8.980 juegos, ≥ 4 géneros | 80.640.400 | 407.082 |

Con ≥ 2 géneros la densidad ronda el 20 %, así que "el grafo es ralo" **no** es el argumento principal. Se eligió la lista porque:

1. Ocupa menos aun con esa densidad, y muchísimo menos cuando se endurece la regla.
2. La operación más usada por la aplicación es "dame los vecinos de este juego" (relacionados), que en la lista cuesta O(grado) y en la matriz O(V).
3. Los recorridos del TP8 (BFS y DFS) son O(V + E) con lista y O(V²) con matriz.
4. La única ventaja de la matriz, consultar una arista en O(1), también la tiene la lista si cada vértice guarda sus vecinos en un diccionario.
5. El catálogo puede crecer: agregar un juego en la lista no obliga a rehacer nada.

## 4. Complejidad de las operaciones (`Grafo`)

V = vértices, E = aristas, g = grado del vértice consultado.

| Operación | Complejidad | Tiempo medido* |
|---|---|---|
| `agregar_vertice(v)` | O(1) | — |
| `agregar_arista(a, b, peso)` | O(1) | — |
| `existe_arista(a, b)` / `peso(a, b)` | O(1) en promedio | 0,12 µs |
| `grado(v)` | O(1) | 0,12 µs |
| `vecinos(v)` | O(g) | 2,3 µs (g = 67, 120 juegos) · 25 µs (g = 665, 980 juegos) · 84 µs (g = 1.901, 8.980 juegos) |
| `aristas()` | O(E) | — |
| `densidad()` | O(1) | — |
| Armar todo el grafo (`construir_grafo`) | ver sección 5 | tabla de la sección 2 |

\*Medido con `perf_counter`, promedio de 2.000 repeticiones.

El tiempo de `existe_arista` no cambia con el tamaño del grafo, mientras que `vecinos` crece con el grado, como indica la teoría.

## 5. Cómo se construye el grafo sin comparar todos contra todos

La forma directa es comparar cada par de juegos: O(n²) comparaciones (40 millones con 8.980 juegos). En su lugar:

1. Se arma un índice **género → juegos que lo tienen** (una pasada, O(n)).
2. Si un juego tiene `k` géneros y para conectar se piden `m` en común, entonces **entre cualquier subconjunto de `k − m + 1` de sus géneros hay al menos uno compartido** (principio del palomar: si no compartiera ninguno de esos, compartiría como mucho `m − 1`).
3. Alcanza entonces con tomar los `k − m + 1` géneros **menos frecuentes** del juego, juntar los candidatos de esos géneros y verificar el mínimo exacto con la intersección.
4. Los juegos con menos de `m` géneros no pueden tener vecinos y se saltean.

Esto produce exactamente las mismas aristas que la comparación de todos contra todos: `tests/test_construir_grafo.py` lo verifica contra una versión de fuerza bruta con los catálogos de 120 y 980 juegos y mínimos de 1 a 4 géneros (y también con el de 8.980 para ≥ 4, en una corrida aparte).

El costo real depende de cuántos candidatos produce el género menos frecuente de cada juego y de cuántas aristas resultan: con 8.980 juegos y ≥ 3 géneros hay 1,5 millones de aristas y el armado tarda 16 s, mientras que con ≥ 4 géneros hay 200 mil y tarda 3 s.

## 6. Ejemplos de consultas

Catálogo de 120 juegos, regla por defecto (≥ 2 géneros): 120 vértices, 1.256 aristas, densidad 17,6 %.

```python
from algoritmos.construir_grafo import construir_grafo
from estructuras.heap import Heap

grafo = construir_grafo(juegos)

# "Ver elementos relacionados": vecinos de un juego, de mayor a menor peso
juego = ...  # HALF-LIFE: BLUE SHIFT  (Action, Shooter · Linux, macOS, PC, Dreamcast)
grafo.grado(juego)                                # 31 juegos relacionados
relacionados = Heap.desde_lista(grafo.vecinos(juego), clave=lambda par: par[1])
relacionados.top_n(5)
```

Resultado (los cinco empatan en peso 5, así que el orden entre ellos es arbitrario):

```text
HOTLINE MIAMI 2: WRONG NUMBER   Action, Shooter, Arcade, Indie          peso 5
HALF-LIFE: OPPOSING FORCE       Action, Shooter                         peso 5
TEAM FORTRESS CLASSIC           Action, Shooter, Massively Multiplayer  peso 5
POSTAL 2                        Action, Shooter, Adventure, Indie       peso 5
SUPERHOT                        Action, Shooter, Indie                  peso 5
```

```python
grafo.existe_arista(blue_shift, opposing_force)   # True
grafo.peso(blue_shift, opposing_force)            # 5  (2 géneros + 3 plataformas)
grafo.peso(opposing_force, blue_shift)            # 5  (no dirigido)
grafo.grado(total_war_shogun_2)                   # 0  (tiene un solo género: no puede compartir 2 con nadie)
```

La consulta "relacionados" reutiliza la heap del TP6: el grafo da los vecinos y la heap devuelve los N más parecidos en O(N·log N) sin ordenar todos.

## 7. Preguntas de defensa

- **¿Qué representa cada vértice? ¿Y cada arista?** Un vértice es un videojuego. Una arista une dos juegos que comparten al menos dos géneros.
- **¿Por qué es no dirigido?** Porque la relación "se parece a" es simétrica; guardar un solo sentido perdería información y obligaría a buscar en dos lados.
- **¿Por qué es pesado?** Porque no todas las relaciones valen lo mismo: dos juegos con tres géneros y dos plataformas en común están más cerca que dos que sólo comparten dos géneros. El peso permite mostrar primero los más relacionados.
- **¿Por qué lista y no matriz?** Menos espacio (O(V + E) contra O(V²)), vecinos en O(grado), recorridos O(V + E), y la consulta de arista sigue siendo O(1) con diccionarios. Ver sección 3.
- **¿Qué pasa si se cambia la regla de conexión?** Solo cambia el parámetro `min_generos_comunes` de `construir_grafo`; la estructura no se toca.
- **¿Dónde está en el código y cómo se integra?** `estructuras/grafo.py` (estructura), `algoritmos/construir_grafo.py` (construcción desde el catálogo) y la versión 5 de la aplicación (`ui/version5.py`) para "Ver elementos relacionados" y "Explorar conexiones".
