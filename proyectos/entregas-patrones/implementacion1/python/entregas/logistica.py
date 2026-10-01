"""Factory Method: el trámite despacha; las subclases fabrican el medio."""

from abc import ABC, abstractmethod

from .dominio import ContextoViaje, Pedido, Plan, Sugerencia
from .medios import (
    EntregaBicicleta,
    EntregaCamioneta,
    EntregaDron,
    EntregaMotocicleta,
    MedioDeEntrega,
)


class Logistica(ABC):
    @abstractmethod
    def crear_medio(self) -> MedioDeEntrega:
        """Gancho: las subclases eligen el producto."""

    def despachar(self, pedido: Pedido, ctx: ContextoViaje) -> Plan:
        medio = self.crear_medio()
        return medio.planear(pedido, ctx)


class LogisticaTerrestre(Logistica):
    def crear_medio(self) -> MedioDeEntrega:
        return EntregaCamioneta()


class LogisticaUrbana(Logistica):
    def crear_medio(self) -> MedioDeEntrega:
        return EntregaMotocicleta()


class LogisticaCorta(Logistica):
    def crear_medio(self) -> MedioDeEntrega:
        return EntregaBicicleta()


class LogisticaAerea(Logistica):
    def crear_medio(self) -> MedioDeEntrega:
        return EntregaDron()


def logistica_para(sugerencia: Sugerencia) -> Logistica:
    """Quién instancia la subclase (configuración). A partir de aquí se habla de Logistica."""
    por_medio = {
        "camioneta": LogisticaTerrestre,
        "motocicleta": LogisticaUrbana,
        "bicicleta": LogisticaCorta,
        "dron": LogisticaAerea,
    }
    return por_medio[sugerencia.medio]()
