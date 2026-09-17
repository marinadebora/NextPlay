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

Al iniciar la aplicación, se mostrará el siguiente menú:
```bash
===== NEXTPLAY =====

1. Buscar videojuegos por nombre
2. Listar todos los videojuegos
3. Filtrar por género / plataforma / rating mínimo
4. Ver detalle de un videojuego
5. Comparar dos videojuegos
0. Salir
```

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
│   └── 05-gestion-proyecto.md
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