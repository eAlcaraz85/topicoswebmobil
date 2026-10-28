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
CARPETA = Path(__file__).resolve().parent / "modelo"

MODELOS = {
    "arbol": {
        "archivo": "modelo_medios.joblib",
        "nombre": "Árbol de decisión",
        "etiqueta": "árbol de decisión",
    },
    "bosque": {
        "archivo": "modelo_bosque.joblib",
        "nombre": "Random Forest",
        "etiqueta": "random forest",
    },
    "red": {
        "archivo": "modelo_red.joblib",
        "nombre": "Red neuronal (MLP)",
        "etiqueta": "red neuronal",
    },
}

app = Flask(__name__)


@lru_cache(maxsize=8)
def cargar_modelo(clave: str):
    info = MODELOS[clave]
    ruta = CARPETA / info["archivo"]
    if not ruta.exists():
        raise FileNotFoundError(f"No está {ruta.name} en el servicio recomendar")
    return joblib.load(ruta), info


def modelos_disponibles():
    return [
        {
            "id": clave,
            "nombre": info["nombre"],
            "listo": (CARPETA / info["archivo"]).exists(),
        }
        for clave, info in MODELOS.items()
    ]


@app.get("/salud")
def salud():
    return jsonify({
        "servicio": "recomendar",
        "estado": "ok",
        "modelos": modelos_disponibles(),
    })


@app.get("/modelos")
def listar_modelos():
    return jsonify({"servicio": "recomendar", "modelos": modelos_disponibles()})


@app.post("/sugerir")
def sugerir():
    cuerpo = request.get_json(silent=True)
    if not isinstance(cuerpo, dict):
        return jsonify({"error": "el cuerpo debe ser JSON"}), 400

    modelo_id = cuerpo.pop("modelo", "arbol") or "arbol"
    if modelo_id not in MODELOS:
        return jsonify({
            "error": "modelo desconocido",
            "modelos": list(MODELOS.keys()),
        }), 400

    faltantes = [c for c in CAMPOS if c not in cuerpo]
    if faltantes:
        return jsonify({"error": "faltan campos", "campos": faltantes}), 400

    try:
        for campo in CAMPOS_NUMERICOS:
            cuerpo[campo] = float(cuerpo[campo])
    except (TypeError, ValueError):
        return jsonify({"error": f"el campo {campo} debe ser un número"}), 400

    try:
        modelo, info = cargar_modelo(modelo_id)
    except FileNotFoundError as error:
        return jsonify({"error": str(error)}), 503

    datos = pd.DataFrame([cuerpo], columns=CAMPOS)
    ranking = sorted(
        zip(modelo.classes_, modelo.predict_proba(datos)[0]),
        key=lambda par: -par[1],
    )
    preferido = ranking[0][0]
    descartados = []
    elegido = None
    confianza = 0.0
    for medio, prob in ranking:
        if es_posible(medio, cuerpo):
            elegido = medio
            confianza = float(prob)
            break
        descartados.append(medio)

    if elegido is None:
        elegido = "camioneta"
        motivo = "ningún medio sugerido era posible"
        corregido = True
    else:
        motivo = f"{info['etiqueta']}, confianza {confianza:.0%}"
        corregido = elegido != preferido
        if corregido:
            motivo += f"; se descartó {preferido} por las reglas del negocio"

    return jsonify({
        "servicio": "recomendar",
        "modelo": modelo_id,
        "modelo_nombre": info["nombre"],
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
