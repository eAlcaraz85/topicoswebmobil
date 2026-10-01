from dataclasses import dataclass


@dataclass(frozen=True)
class Pedido:
    origen: str
    destino: str
    peso_kg: float
    distancia_km: float
    urgente: bool = False


@dataclass(frozen=True)
class ContextoViaje:
    trafico_alto: bool
    lluvia: bool


@dataclass(frozen=True)
class Sugerencia:
    """Lo que el dominio entiende. El JSON/XML ajeno no entra aquí."""

    medio: str
    motivo: str


@dataclass(frozen=True)
class Plan:
    medio: str
    cabe: bool
    minutos: int
    costo: float
    detalle: str
