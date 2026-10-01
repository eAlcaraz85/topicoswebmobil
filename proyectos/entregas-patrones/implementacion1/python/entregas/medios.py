"""Strategy: varias formas de planear la misma entrega."""

from abc import ABC, abstractmethod

from .dominio import ContextoViaje, Pedido, Plan


class MedioDeEntrega(ABC):
    @abstractmethod
    def planear(self, pedido: Pedido, ctx: ContextoViaje) -> Plan:
        """¿Cabe? ¿Cuánto tarda? ¿Cuánto cuesta?"""


class EntregaBicicleta(MedioDeEntrega):
    def planear(self, pedido: Pedido, ctx: ContextoViaje) -> Plan:
        cabe = pedido.peso_kg <= 5 and pedido.distancia_km <= 8
        minutos = int(pedido.distancia_km * 6)
        if ctx.trafico_alto:
            minutos = int(minutos * 1.1)
        return Plan("bicicleta", cabe, minutos, 25.0, "paquete chico, tramo corto")


class EntregaMotocicleta(MedioDeEntrega):
    def planear(self, pedido: Pedido, ctx: ContextoViaje) -> Plan:
        cabe = pedido.peso_kg <= 15
        minutos = int(pedido.distancia_km * 3)
        if ctx.trafico_alto:
            minutos = int(minutos * 1.4)
        costo = 45.0 + (20.0 if pedido.urgente else 0.0)
        return Plan("motocicleta", cabe, minutos, costo, "ciudad, paquete mediano")


class EntregaCamioneta(MedioDeEntrega):
    def planear(self, pedido: Pedido, ctx: ContextoViaje) -> Plan:
        minutos = int(pedido.distancia_km * 4.5)
        if ctx.trafico_alto:
            minutos = int(minutos * 1.6)
        costo = 90.0 + pedido.peso_kg * 2
        return Plan("camioneta", True, minutos, costo, "carga amplia, más lenta en ciudad")


class EntregaDron(MedioDeEntrega):
    def planear(self, pedido: Pedido, ctx: ContextoViaje) -> Plan:
        cabe = pedido.peso_kg <= 3 and pedido.distancia_km <= 12 and not ctx.lluvia
        minutos = int(pedido.distancia_km * 2)
        return Plan("dron", cabe, minutos, 70.0, "rápido; no vuela con lluvia ni con mucho peso")
