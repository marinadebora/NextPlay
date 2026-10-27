# Diagrama de datos

## Organización de los datos

NextPlay obtiene los datos de los videojuegos desde el archivo `VideoGames.JSON`. A partir de esos registros se construyen objetos de la clase `VideoJuego`, que contienen información como el nombre, el rating, las plataformas y los géneros.

Los objetos se utilizan para construir diferentes estructuras de datos y realizar búsquedas y consultas sobre el catálogo.

## Estructuras y conexiones
## version 1

```mermaid
flowchart TD
    A["VideoGames.JSON"] --> B["Carga y construcción de objetos"]
    B --> C["Objetos VideoJuego"]
    C --> D["Búsquedas secuenciales"]
    D --> G["Búsqueda por nombre parcial"]
    D --> H["Listar todos los Video Juegos"]
    D --> I["Búsqueda y ordenamiento por rating, genero y plataforma"]    
    D --> K["Detalle de un videojuego"]
    D --> L["Comparación de videojuegos"]
```
## Descripción de las estructuras

- **VideoGames.JSON:** archivo que contiene los datos del catálogo de videojuegos.
- **VideoJuego:** clase que representa cada videojuego y sus atributos.
- **Búsquedas secuenciales:** recorren los videojuegos para encontrar los datos necesarios para operaciones como consultar el detalle o comparar videojuegos.

## version 2

```mermaid
flowchart TD
    A["VideoGames.JSON"] --> B["Carga y construcción de objetos"]
    B --> C["Objetos VideoJuego"]

    C --> D["Árbol binario de búsqueda (BST)"]
    C --> E["Árbol AVL"]
    C --> F["Árbol de búsqueda por rating"]

    D --> G["Búsqueda por nombre exacto"]
    E --> H["Búsqueda por nombre exacto"]
    E --> O["Listar ordenado inorder"]
    F --> I["Búsqueda y ordenamiento por rating"]

    C --> J["Búsquedas secuenciales"]
    J --> K["Búsqueda y ordenamiento por rating, genero y plataforma"]
    J --> L["Busqueda por nombre parcial"]
    J --> M["Detalle de un videojuego"]
    J --> N["Comparación de videojuegos"]

```

## Descripción de las estructuras

- **VideoGames.JSON:** archivo que contiene los datos del catálogo de videojuegos.
- **VideoJuego:** clase que representa cada videojuego y sus atributos.
- **Árbol binario de búsqueda (BST):** organiza los videojuegos por nombre y permite realizar búsquedas por nombre exacto.
- **Árbol AVL:** árbol de búsqueda balanceado por nombre que mantiene su altura controlada durante las inserciones organiza los videojuegos por nombre y permite realizar búsquedas por nombre exacto, tambien ordena inorder para listar todos los videojuegos.
- **Árbol de búsqueda por rating:** organiza los videojuegos según su puntuación para facilitar las consultas y el ordenamiento por rating.
- **Búsquedas secuenciales:** recorren los videojuegos para encontrar los datos necesarios para operaciones como consultar el detalle o comparar videojuegos.

Las estructuras utilizan objetos `VideoJuego` como elementos de información. Cada árbol mantiene su propia organización según el criterio de búsqueda correspondiente, mientras que las búsquedas secuenciales recorren los elementos del catálogo según la operación que se necesita realizar.

## version 3
```mermaid
flowchart TD
    A["VideoGames.JSON"] --> B["Carga y construcción de objetos"]
    B --> C["Objetos VideoJuego"]

    C --> D["Árbol BST"]   
    C --> E["Árbol AVL"]   
    C --> F["Árbol General"]
    C --> 0["Búsquedas secuenciales"]

    D --> G["Búsqueda y ordenamiento por rating"]
    D --> H["Búsqueda por nombre exacto"]

    E --> I["Búsqueda por nombre exacto"]
    E --> J["Listar ordenado inorder"]
   
    F --> K["Búsqueda y ordenamiento por genero y plataforma"]
    
    H --> L["Detalle de un videojuego"]
    H --> M["Comparación de videojuegos"]

    O --> P["Búsqueda por nombre parcial"]
```

## Descripción de las estructuras

- **VideoGames.JSON:** archivo que contiene los datos del catálogo de videojuegos.
- **VideoJuego:** clase que representa cada videojuego y sus atributos.
- **Árbol binario de búsqueda (BST):** organiza los videojuegos por nombre y permite realizar búsquedas por nombre exacto, se utiliza para buscar el detalle y para comparar dos videojuegos.
- **Árbol (AVL):** árbol de búsqueda balanceado por nombre que mantiene su altura controlada durante las inserciones organiza los videojuegos por nombre y permite realizar búsquedas por nombre exacto, tambien ordena inorder para listar todos los videojuegos.
- **Árbol de búsqueda por rating (BST):** organiza los videojuegos según su puntuación para facilitar las consultas y el ordenamiento por rating.
- **Árbol General:** organiza los videojuegos por categorias, generos o plataformas.

## version 4
```mermaid
flowchart TD
    A["VideoGames.JSON"] --> B["Carga y construcción de objetos"]
    B --> C["Objetos VideoJuego"]

    C --> D["Árbol BST"]   
    C --> E["Árbol AVL"]   
    C --> F["Árbol General"]
    C --> G["Árbol HEAP"]
    C --> P["Búsquedas secuenciales"]

    D --> H["Búsqueda y ordenamiento por rating"]
    D --> I["Búsqueda por nombre exacto"]

    E --> J["Búsqueda por nombre exacto"]
    E --> K["Listar ordenado inorder"]
   
    F --> L["Búsqueda y ordenamiento por genero y plataforma"]
    
    G --> M["Ranking"]

    I --> N["Detalle de un videojuego"]
    I --> O["Comparación de videojuegos"]

    P --> Q["Búsqueda por nombre parcial"]

```
## Descripción de las estructuras

- **VideoGames.JSON:** archivo que contiene los datos del catálogo de videojuegos.
- **VideoJuego:** clase que representa cada videojuego y sus atributos.
- **Árbol binario de búsqueda (BST):** organiza los videojuegos por nombre y permite realizar búsquedas por nombre exacto, se utiliza para buscar el detalle y para comparar dos videojuegos.
- **Árbol (AVL):** árbol de búsqueda balanceado por nombre que mantiene su altura controlada durante las inserciones organiza los videojuegos por nombre y permite realizar búsquedas por nombre exacto, tambien ordena inorder para listar todos los videojuegos.
- **Árbol de búsqueda por rating (BST):** organiza los videojuegos según su puntuación para facilitar las consultas y el ordenamiento por rating.
- **Árbol General:** organiza los videojuegos por categorias, generos o plataformas.
- **Árbol HEAP:** Crea un ranking de todos los videojuegos por rating.
