"""Clases de dominio de NextPlay."""


class VideoJuego:
    """Representa un videojuego del catalogo de NextPlay.

    Encapsula sus atributos (privados, con acceso via @property) y expone
    algunas operaciones de comparacion usadas por los servicios de
    busqueda/filtrado.
    """

    def __init__(self, id_, name, img, release_date, rating, platform, genres):
        self._id = id_
        self._name = name
        self._img = img
        self._release_date = release_date
        self._rating = rating if rating is not None else 0.0
        self._platform = list(platform) if platform else []
        # genres puede venir como [{"name": "Action"}, ...] (formato RAWG) o ["Action", ...]
        self._genres = [g["name"] if isinstance(g, dict) else g for g in (genres or [])]

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def img(self):
        return self._img

    @property
    def release_date(self):
        return self._release_date

    @property
    def rating(self):
        return self._rating

    @property
    def platform(self):
        return list(self._platform)

    @property
    def genres(self):
        return list(self._genres)

    @classmethod
    def from_dict(cls, data: dict) -> "VideoJuego":
        """Construye un VideoJuego a partir de un registro del dataset (datos/VideoGames.JSON)."""
        return cls(
            id_=data.get("id"),
            name=data.get("name", ""),
            img=data.get("img", ""),
            release_date=data.get("Release_date", ""),
            rating=data.get("rating", 0.0),
            platform=data.get("platform", []),
            genres=data.get("genres", []),
        )

    def coincide_con_genero(self, genero: str) -> bool:
        return genero.lower() in [g.lower() for g in self._genres]

    def coincide_con_plataforma(self, plataforma: str) -> bool:
        return plataforma.lower() in [p.lower() for p in self._platform]

    def __repr__(self):
        generos = ", ".join(self._genres)
        plataformas = ", ".join(self._platform)
        return f"{self._name} ({generos}) [{plataformas}] estrellas:{self._rating}"
