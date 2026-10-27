"""Microservicio de recomendación: solo habla de medios y probabilidades."""

from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, jsonify, request

from reglas import es_posible

CAMPOS = [
    "distancia_km", "peso_kg", "largo_cm", "ancho_cm", "alto_cm", "volumen_l",
    "fragil", "refrigerado", "valor_declarado_mxn", "hora_salida",
    "prioridad", "zona_destino", "clima", "trafico",
]
CAMPOS_NUMERICOS = CAMPOS[:10]
RUTA_MODELO = Path(__file__).resolve().parent / "modelo" / "modelo_medios.joblib"

app = Flask(__name__)


@lru_cache(maxsize=1)
def cargar_modelo():
    return joblib.load(RUTA_MODELO)


@app.get("/salud")
def salud():
    return jsonify({"servicio": "recomendar", "estado": "ok"})


@app.post("/sugerir")
def sugerir():
    paquete = request.get_json(silent=True)
    if not isinstance(paquete, dict):
        return jsonify({"error": "el cuerpo debe ser JSON"}), 400

    faltantes = [c for c in CAMPOS if c not in paquete]
    if faltantes:
        return jsonify({"error": "faltan campos", "campos": faltantes}), 400

    try:
        for campo in CAMPOS_NUMERICOS:
            paquete[campo] = float(paquete[campo])
    except (TypeError, ValueError):
        return jsonify({"error": f"el campo {campo} debe ser un número"}), 400

    modelo = cargar_modelo()
    datos = pd.DataFrame([paquete], columns=CAMPOS)
    ranking = sorted(
        zip(modelo.classes_, modelo.predict_proba(datos)[0]),
        key=lambda par: -par[1],
    )
    preferido = ranking[0][0]
    descartados = []
    elegido = None
    confianza = 0.0
    for medio, prob in ranking:
        if es_posible(medio, paquete):
            elegido = medio
            confianza = float(prob)
            break
        descartados.append(medio)

    if elegido is None:
        elegido = "camioneta"
        motivo = "ningún medio sugerido era posible"
        corregido = True
    else:
        motivo = f"árbol de decisión, confianza {confianza:.0%}"
        corregido = elegido != preferido
        if corregido:
            motivo += f"; se descartó {preferido} por las reglas del negocio"

    return jsonify({
        "servicio": "recomendar",
        "medio": elegido,
        "motivo": motivo,
        "preferido_por_modelo": preferido,
        "corregido_por_reglas": corregido,
        "descartados": descartados,
        "ranking": [
            {"medio": m, "confianza": round(float(p), 3)} for m, p in ranking
        ],
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002)
