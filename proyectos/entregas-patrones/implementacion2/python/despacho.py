#!/usr/bin/env python3
"""
MALA PRÁCTICA a propósito.

Mismo trámite que el proyecto con patrones (registrar pedido, oír a la IA,
planear la entrega). Aquí no hay Strategy, ni Adapter, ni Factory Method.

Todo vive en una función: el JSON/XML de la IA, el if del medio y el
cálculo del plan. Si mañana llega un triciclo o el proveedor cambia
route_hint por vehicle, hay que abrir ESTE archivo otra vez.
"""


def registrar_pedido(origen, destino, peso, distancia, urgente, trafico, lluvia, proveedor):
    cabe = False
    minutos = 0
    costo = 0
    detalle = ""
    medio = ""
    motivo = ""

    if proveedor == "openai":
        if peso <= 3 and distancia <= 12 and not lluvia:
            hint = "drone"
            score = 91
            why = "FASTEST"
        elif peso <= 5 and distancia <= 8:
            hint = "bike"
            score = 80
            why = "SHORT_HOP"
        elif peso <= 15:
            hint = "moto"
            score = 74
            why = "CITY"
        else:
            hint = "van"
            score = 60
            why = "HEAVY"
        motivo = why + " (score " + str(score) + ")"

        if hint == "drone":
            medio = "dron"
            cabe = peso <= 3 and distancia <= 12 and not lluvia
            minutos = int(distancia * 2)
            costo = 70
            detalle = "rápido; no vuela con lluvia ni con mucho peso"
        elif hint == "bike":
            medio = "bicicleta"
            cabe = peso <= 5 and distancia <= 8
            minutos = int(distancia * 6)
            if trafico:
                minutos = int(minutos * 1.1)
            costo = 25
            detalle = "paquete chico, tramo corto"
        elif hint == "moto":
            medio = "motocicleta"
            cabe = peso <= 15
            minutos = int(distancia * 3)
            if trafico:
                minutos = int(minutos * 1.4)
            costo = 45
            if urgente:
                costo = costo + 20
            detalle = "ciudad, paquete mediano"
        elif hint == "van":
            medio = "camioneta"
            cabe = True
            minutos = int(distancia * 4.5)
            if trafico:
                minutos = int(minutos * 1.6)
            costo = 90 + peso * 2
            detalle = "carga amplia, más lenta en ciudad"
        else:
            print("hint desconocido, toca editar registrar_pedido")

    elif proveedor == "xml":
        if urgente and peso <= 3 and not lluvia:
            xml = '<reco vehicle="drone"><note>xml-vendor</note></reco>'
        elif peso > 15:
            xml = '<reco vehicle="van"><note>xml-vendor</note></reco>'
        else:
            xml = '<reco vehicle="moto"><note>xml-vendor</note></reco>'

        if 'vehicle="drone"' in xml:
            hint = "drone"
        elif 'vehicle="bike"' in xml:
            hint = "bike"
        elif 'vehicle="moto"' in xml:
            hint = "moto"
        elif 'vehicle="van"' in xml:
            hint = "van"
        else:
            hint = "?"
        motivo = "proveedor XML (xml-vendor)"

        # Las mismas reglas, copiadas. Un cambio de costo obliga a tocar
        # el bloque de openai Y este.
        if hint == "drone":
            medio = "dron"
            cabe = peso <= 3 and distancia <= 12 and not lluvia
            minutos = int(distancia * 2)
            costo = 70
            detalle = "rápido; no vuela con lluvia ni con mucho peso"
        elif hint == "bike":
            medio = "bicicleta"
            cabe = peso <= 5 and distancia <= 8
            minutos = int(distancia * 6)
            if trafico:
                minutos = int(minutos * 1.1)
            costo = 25
            detalle = "paquete chico, tramo corto"
        elif hint == "moto":
            medio = "motocicleta"
            cabe = peso <= 15
            minutos = int(distancia * 3)
            if trafico:
                minutos = int(minutos * 1.4)
            costo = 45
            if urgente:
                costo = costo + 20
            detalle = "ciudad, paquete mediano"
        elif hint == "van":
            medio = "camioneta"
            cabe = True
            minutos = int(distancia * 4.5)
            if trafico:
                minutos = int(minutos * 1.6)
            costo = 90 + peso * 2
            detalle = "carga amplia, más lenta en ciudad"
    else:
        print("proveedor nuevo: hay que agregar otro elif aquí")

    print("")
    print("Pedido:", origen, "→", destino, "(", peso, "kg,", distancia, "km)")
    print("IA (idioma ajeno, sin traducir del todo):", motivo)
    print("Medio:", medio, " cabe=", cabe, " ", minutos, " min  $", int(costo))
    print(" ", detalle)
    if not cabe:
        print("  El medio no cabe; el if de arriba ya mezcló IA y plan.")


if __name__ == "__main__":
    print("Plataforma de entregas — SIN patrones (mala práctica)")
    print("Un solo método: JSON/XML + if de medios + plan. Copiar y rezar.")

    print("\n=== Pedido ligero + JSON de OpenAI ===")
    registrar_pedido("Centro", "Roma Norte", 1.2, 4.0, True, True, False, "openai")

    print("\n=== Pedido pesado + XML de otro proveedor ===")
    registrar_pedido("Bodega Norte", "Iztapalapa", 28.0, 18.0, False, True, False, "xml")
