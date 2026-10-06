# NextPlay

**NextPlay** es una aplicación orientada a la recomendación de videojuegos. Su objetivo es ayudar a los usuarios a encontrar videojuegos que se adapten a sus intereses, preferencias y plataforma de juego.

La aplicación utiliza información obtenida de una API especializada en videojuegos. A partir de los datos disponibles, se desarrolló un archivo **JSON** que nos servirá como base de datos para la aplicación.

---
## Integrantes

> **Grupo 8**

- Ragonese Gianluca
- Santini Agustina
- Carabajal Débora

---

## Instrucciones de ejecución

### 1. Clonar el repositorio

Para obtener el proyecto, clonar el repositorio desde GitHub:

```bash
git clone URL_DEL_REPOSITORIO
```
Luego, ingresar a la carpeta del proyecto:
```bash
cd NextPlay
```
### 2. Ejecutar la aplicación

No es necesario instalar dependencias adicionales.

Desde la carpeta del proyecto, ejecutar:
```bash
python main.py
```
### 3. Menú principal

Al iniciar la aplicación, se puede elegir entre la versión 1.0 (TP1/TP2) y la versión 2.0 (TP3, con el árbol binario integrado a la búsqueda y al filtro por rating):
```bash
=== NextPlay ===
1. version 1.0
2. version 2.0
0. Salir
```
Ambas versiones comparten el mismo catálogo de juegos (`datos/VideoGames.JSON`) y el mismo menú de opciones:
```bash
=== NextPlay ===
1. Buscar videojuegos por nombre
2. Listar todos los videojuegos
3. Filtrar por genero / plataforma / rating minimo
4. Ver detalle de un videojuego
5. Comparar dos videojuegos
0. Salir
```

## Estructuras de datos (TP3 — árboles binarios de búsqueda)

A partir del TP3, el proyecto usa dos árboles binarios de búsqueda (`estructuras/`), cada uno con su propia **clave de ordenamiento**:

| Árbol | Archivo | Clave de ordenamiento | Dónde se usa |
|---|---|---|---|
| Por nombre | `estructuras/arbol_busqueda_nombre.py` | `name` (título del juego, alfabético) | Búsqueda exacta por nombre (versión 2, opción 1) y medición de TP2 (`algoritmos/medicion.py`) |
| Por rating | `estructuras/arbol_busqueda_rating.py` | `rating` (numérico) | Filtro por rating mínimo (versión 2, opción 3) |

Ambos árboles se construyen balanceados con `algoritmos/construir_arbol.py` (se ordena la lista de juegos por la clave elegida y se toma siempre el elemento del medio como raíz de cada subárbol), e implementan inserción, búsqueda y los 3 recorridos clásicos (`inorder`, `preorder`, `postorder`). El `inorder` del árbol por nombre devuelve el catálogo completo ordenado alfabéticamente sin necesidad de volver a ordenarlo.

La comparación de rendimiento del árbol por nombre contra la búsqueda secuencial del TP2 está en [`docs/06-analisis-complejidad.md`](./docs/06-analisis-complejidad.md).

## Estructura del repositorio

```text
proyecto/
├── algoritmos/
├── docs/
│   ├──capturas/
│   ├── 01-requerimientos.md
│   ├── 02-casos-de-uso.md
│   ├── 03-diagrama-clases.md
│   ├── 04-diagrama-datos.md
│   ├── 05-gestion-proyecto.md
│   └── 06-analisis-complejidad.md
├── estructuras/
├── datos/
├── modelos/
├── servicios/
├── tests/
├── ui/
├──.gitignore
├── main.py
└── README.md

```
## Documentación

- [Requerimientos](./docs/01-requerimientos.md)
- [Casos de uso](./docs/02-casos-de-uso.md)
- [Diagrama de clases](./docs/03-diagrama-clases.md)
- [Diagrama de datos](./docs/04-diagrama-datos.md)
- [Gestión del proyecto](./docs/05-gestion-proyecto.md)
- [Análisis de complejidad (árbol vs. búsqueda secuencial)](./docs/06-analisis-complejidad.md)