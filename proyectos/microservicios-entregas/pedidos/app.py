"""Microservicio de pedidos: orquesta; no carga el modelo."""

import os
import uuid
from datetime import datetime, timezone

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

RECOMENDAR_URL = os.environ.get("RECOMENDAR_URL", "http://recomendar:8002").rstrip("/")
TIMEOUT = float(os.environ.get("RECOMENDAR_TIMEOUT", "3"))

# Memoria del proceso: cada réplica tendría la suya; aquí sirve para la demo.
PEDIDOS = []


@app.get("/salud")
def salud():
    return jsonify({
        "servicio": "pedidos",
        "estado": "ok",
        "recomendar_url": RECOMENDAR_URL,
        "pedidos_en_memoria": len(PEDIDOS),
    })


@app.get("/pedidos")
def listar():
    return jsonify({"servicio": "pedidos", "pedidos": PEDIDOS})


@app.post("/pedidos")
def crear():
    paquete = request.get_json(silent=True)
    if not isinstance(paquete, dict):
        return jsonify({"error": "el cuerpo debe ser JSON"}), 400

    try:
        respuesta = requests.post(
            f"{RECOMENDAR_URL}/sugerir",
            json=paquete,
            timeout=TIMEOUT,
        )
    except requests.RequestException as error:
        # Fallo parcial: Pedidos sigue vivo; no pudo obtener sugerencia.
        return jsonify({
            "error": "el servicio recomendar no respondió",
            "detalle": str(error),
            "servicio": "pedidos",
            "plan_b": {
                "medio": "moto",
                "motivo": "fallback local: recomendar no está disponible",
            },
        }), 503

    if respuesta.status_code >= 400:
        return jsonify({
            "error": "recomendar rechazó el paquete",
            "detalle": respuesta.json() if respuesta.content else respuesta.text,
            "servicio": "pedidos",
        }), 502

    sugerencia = respuesta.json()
    folio = f"ENV-{uuid.uuid4().hex[:8].upper()}"
    pedido = {
        "folio": folio,
        "creado": datetime.now(timezone.utc).isoformat(),
        "medio": sugerencia.get("medio"),
        "motivo": sugerencia.get("motivo"),
        "sugerencia": sugerencia,
        "paquete": paquete,
    }
    PEDIDOS.append(pedido)
    return jsonify({
        "servicio": "pedidos",
        "folio": folio,
        "medio": pedido["medio"],
        "motivo": pedido["motivo"],
        "llamada_a": f"{RECOMENDAR_URL}/sugerir",
        "sugerencia": sugerencia,
    }), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
