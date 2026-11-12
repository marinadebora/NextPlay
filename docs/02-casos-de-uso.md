# Casos de uso

## Actor principal

**Usuario:** persona que utiliza NextPlay para buscar, consultar, filtrar y comparar videojuegos.

## Buscar videojuegos por nombre

- **Actor:** Usuario.
- **Objetivo:** Encontrar un videojuego por su nombre.
- **Precondición:** La aplicación está iniciada y los videojuegos están cargados.
- **Flujo principal:**
  1. El usuario selecciona la opción de búsqueda por nombre.
  2. Elige buscar por nombre exacto o por coincidencia parcial.
  3. Ingresa el nombre o texto que desea buscar.
  4. El sistema realiza la búsqueda y muestra los resultados.
- **Flujo alternativo:** Si no se encuentran resultados, el sistema informa que no hay coincidencias.

## Listar todos los videojuegos

- **Actor:** Usuario.
- **Objetivo:** Consultar el listado completo de videojuegos.
- **Precondición:** La aplicación está iniciada y los videojuegos están cargados.
- **Flujo principal:**
  1. El usuario selecciona la opción de listar videojuegos.
  2. El sistema muestra los videojuegos disponibles.

## Filtrar videojuegos

- **Actor:** Usuario.
- **Objetivo:** Encontrar videojuegos según determinados criterios.
- **Precondición:** La aplicación está iniciada y los videojuegos están cargados.
- **Flujo principal:**
  1. El usuario selecciona la opción de filtrado.
  2. Elige filtrar por género, plataforma o rating mínimo.
  3. Ingresa o selecciona el criterio correspondiente.
  4. El sistema muestra los videojuegos que cumplen con el filtro.
- **Flujo alternativo:** Si no hay videojuegos que cumplan con el criterio, el sistema informa que no hay coincidencias.

## Ver detalle de un videojuego

- **Actor:** Usuario.
- **Objetivo:** Consultar la información de un videojuego.
- **Precondición:** La aplicación está iniciada y los videojuegos están cargados.
- **Flujo principal:**
  1. El usuario selecciona la opción de ver detalle.
  2. Selecciona o busca el videojuego que desea consultar.
  3. El sistema muestra la información disponible del videojuego.

## Comparar dos videojuegos

- **Actor:** Usuario.
- **Objetivo:** Consultar y comparar la información de dos videojuegos.
- **Precondición:** La aplicación está iniciada y los videojuegos están cargados.
- **Flujo principal:**
  1. El usuario selecciona la opción de comparar videojuegos.
  2. Selecciona el primer videojuego.
  3. Selecciona el segundo videojuego.
  4. El sistema muestra la información de ambos para facilitar su comparación.

## Crear nuevo ranking

- **Actor:** Usuario.
- **Objetivo:** Generar un ranking de videojuegos según su rating.
- **Precondición:** La aplicación está iniciada y los videojuegos están cargados.
- **Flujo principal:**
  1. El usuario selecciona la opción de crear un nuevo ranking.
  2. Elige el orden del ranking: de mayor a menor o de menor a mayor rating.
  3. El sistema solicita la cantidad de videojuegos que desea incluir.
  4. El usuario ingresa la cantidad.
  5. El sistema genera y muestra el ranking solicitado.
- **Flujo alternativo:** Si la cantidad ingresada no es válida, el sistema solicita un nuevo valor.

## Ver videojuegos relacionados

- **Actor:** Usuario.
- **Objetivo:** Consultar los videojuegos relacionados con un videojuego seleccionado.
- **Precondición:** La aplicación está iniciada, los videojuegos están cargados y el grafo de relaciones está construido.
- **Flujo principal:**
  1. El usuario selecciona la opción de ver videojuegos relacionados.
  2. Ingresa el nombre exacto del videojuego que desea consultar.
  3. El sistema busca el videojuego y realiza un recorrido BFS sobre el grafo.
  4. El sistema muestra los videojuegos relacionados encontrados.
- **Flujo alternativo:** Si el videojuego no existe, el sistema informa que no fue encontrado. Si no tiene videojuegos relacionados, informa que no se encontraron conexiones.

## Ver camino más corto entre dos videojuegos

- **Actor:** Usuario.
- **Objetivo:** Encontrar el camino con menor cantidad de aristas entre dos videojuegos.
- **Precondición:** La aplicación está iniciada, los videojuegos están cargados y el grafo de relaciones está construido.
- **Flujo principal:**
  1. El usuario selecciona la opción de ver camino más corto.
  2. Ingresa el nombre exacto del videojuego de origen.
  3. Ingresa el nombre exacto del videojuego de destino.
  4. El sistema busca ambos videojuegos.
  5. El sistema utiliza BFS para encontrar el camino con menor cantidad de aristas.
  6. El sistema muestra los videojuegos que forman el camino y la distancia en cantidad de aristas.
- **Flujo alternativo:** Si alguno de los videojuegos no existe, el sistema informa que no fue encontrado. Si no existe un camino entre ambos, informa que no hay conexión.

## Explorar conexiones entre videojuegos

- **Actor:** Usuario.
- **Objetivo:** Explorar los videojuegos conectados a uno seleccionado mediante una búsqueda en profundidad.
- **Precondición:** La aplicación está iniciada, los videojuegos están cargados y el grafo de relaciones está construido.
- **Flujo principal:**
  1. El usuario selecciona la opción de explorar conexiones entre videojuegos.
  2. Ingresa el nombre exacto del videojuego desde el cual desea comenzar.
  3. El sistema busca el videojuego y realiza un recorrido DFS sobre el grafo.
  4. El sistema muestra los videojuegos alcanzados durante el recorrido, en el orden de visita.
- **Flujo alternativo:** Si el videojuego no existe, el sistema informa que no fue encontrado. Sino tiene conexiones, informa que no se encontraron videojuegos relacionados.