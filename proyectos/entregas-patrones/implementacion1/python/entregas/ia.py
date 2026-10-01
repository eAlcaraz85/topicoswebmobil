"""Adapter: la IA habla otro idioma; el dominio habla Sugerencia."""

from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET

from typing import Optional

from .dominio import ContextoViaje, Pedido, Sugerencia


class RecomendadorIA(ABC):
    @abstractmethod
    def sugerir(self, pedido: Pedido, ctx: ContextoViaje) -> Sugerencia:
        pass


class ClienteOpenAI:
    """Simula un proveedor que responde JSON propio (route_hint, score)."""

    def completar(self, pedido: Pedido, ctx: ContextoViaje) -> dict:
        if pedido.peso_kg <= 3 and pedido.distancia_km <= 12 and not ctx.lluvia:
            return {"route_hint": "drone", "score": 91, "why": "FASTEST"}
        if pedido.peso_kg <= 5 and pedido.distancia_km <= 8:
            return {"route_hint": "bike", "score": 80, "why": "SHORT_HOP"}
        if pedido.peso_kg <= 15:
            return {"route_hint": "moto", "score": 74, "why": "CITY"}
        return {"route_hint": "van", "score": 60, "why": "HEAVY"}


class ClienteXml:
    """Otro proveedor: XML con atributo vehicle."""

    def consultar(self, pedido: Pedido, ctx: ContextoViaje) -> str:
        if pedido.urgente and pedido.peso_kg <= 3 and not ctx.lluvia:
            vehicle = "drone"
        elif pedido.peso_kg > 15:
            vehicle = "van"
        else:
            vehicle = "moto"
        return f'<reco vehicle="{vehicle}"><note>xml-vendor</note></reco>'


_HINTS = {
    "drone": "dron",
    "bike": "bicicleta",
    "moto": "motocicleta",
    "van": "camioneta",
}


class AdaptadorOpenAI(RecomendadorIA):
    def __init__(self, cliente: Optional[ClienteOpenAI] = None):
        self.cliente = cliente or ClienteOpenAI()

    def sugerir(self, pedido: Pedido, ctx: ContextoViaje) -> Sugerencia:
        crudo = self.cliente.completar(pedido, ctx)
        medio = _HINTS[crudo["route_hint"]]
        motivo = f'{crudo["why"]} (score {crudo["score"]})'
        return Sugerencia(medio, motivo)


class AdaptadorXml(RecomendadorIA):
    def __init__(self, cliente: Optional[ClienteXml] = None):
        self.cliente = cliente or ClienteXml()

    def sugerir(self, pedido: Pedido, ctx: ContextoViaje) -> Sugerencia:
        xml = self.cliente.consultar(pedido, ctx)
        raiz = ET.fromstring(xml)
        medio = _HINTS[raiz.attrib["vehicle"]]
        nota = raiz.findtext("note", "")
        return Sugerencia(medio, f"proveedor XML ({nota})")
