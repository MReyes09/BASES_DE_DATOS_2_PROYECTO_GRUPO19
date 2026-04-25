from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import re

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb://admin:202202233@localhost:27017/")
db = client["mundiales_db"]

# ─── PROCEDIMIENTO 1: getHistorialPais ────────────────────────────────────────
@app.route("/procedimiento1", methods=["GET"])
def get_historial_pais():
    nombre_pais = request.args.get("pais")
    anio_filtro = request.args.get("anio", type=int)

    if not nombre_pais:
        return jsonify({"error": "Parámetro 'pais' requerido"}), 400

    pais = db.paises.find_one({"nombre": {"$regex": re.compile(nombre_pais, re.IGNORECASE)}})
    if not pais:
        return jsonify({"error": f"País no encontrado: {nombre_pais}"}), 404

    pais.pop("_id", None)

    # Años sede
    anios_sede = list(set(
        anio
        for p in pais.get("participaciones", [])
        if p.get("fue_sede")
        for anio in p.get("anios_sede", [])
    ))

    participaciones = pais.get("participaciones", [])
    if anio_filtro:
        participaciones = [p for p in participaciones if p.get("anio") == anio_filtro]

    result_participaciones = []
    for p in sorted(participaciones, key=lambda x: x.get("anio", 0)):
        mundial = db.mundiales.find_one({"_id": p.get("mundial_id")}, {"partidos": 1, "anio": 1})
        partidos_pais = []
        if mundial:
            for pa in mundial.get("partidos", []):
                e1 = (pa.get("equipo1") or {}).get("pais", "") or ""
                e2 = (pa.get("equipo2") or {}).get("pais", "") or ""
                if e1.lower() == pais["nombre"].lower() or e2.lower() == pais["nombre"].lower():
                    partidos_pais.append({
                        "fecha": pa.get("fecha"),
                        "fase": pa.get("fase"),
                        "equipo1": e1,
                        "equipo2": e2,
                        "goles": pa.get("goles", [])
                    })

        result_participaciones.append({
            "anio": p.get("anio"),
            "grupo": p.get("grupo"),
            "director_tecnico": p.get("director_tecnico"),
            "fue_sede": p.get("fue_sede", False),
            "partidos": partidos_pais
        })

    return jsonify({
        "pais": pais["nombre"],
        "anios_sede": sorted(anios_sede),
        "total_participaciones": len(result_participaciones),
        "participaciones": result_participaciones
    })


# ─── PROCEDIMIENTO 2: getInfoMundial ──────────────────────────────────────────
@app.route("/procedimiento2", methods=["GET"])
def get_info_mundial():
    anio = request.args.get("anio", type=int)
    filtro_grupo = request.args.get("grupo")
    filtro_pais = request.args.get("pais")

    if not anio:
        return jsonify({"error": "Parámetro 'anio' requerido"}), 400

    mundial = db.mundiales.find_one({"anio": anio})
    if not mundial:
        return jsonify({"error": f"Mundial no encontrado para el año: {anio}"}), 404

    mundial.pop("_id", None)

    grupos = mundial.get("grupos", [])
    if filtro_grupo:
        grupos = [g for g in grupos if g.get("nombre") == filtro_grupo]
    if filtro_pais:
        grupos = [
            {**g, "selecciones": [s for s in g.get("selecciones", []) if filtro_pais.lower() in s.get("pais", "").lower()]}
            for g in grupos
        ]
        grupos = [g for g in grupos if g["selecciones"]]

    partidos = mundial.get("partidos", [])
    if filtro_pais:
        partidos = [
            p for p in partidos
            if filtro_pais.lower() in ((p.get("equipo1") or {}).get("pais", "") or "").lower()
            or filtro_pais.lower() in ((p.get("equipo2") or {}).get("pais", "") or "").lower()
        ]

    partidos_clean = []
    for p in partidos:
        partidos_clean.append({
            "fecha": p.get("fecha"),
            "fase": p.get("fase"),
            "equipo1": (p.get("equipo1") or {}).get("pais"),
            "equipo2": (p.get("equipo2") or {}).get("pais"),
            "goles": p.get("goles", [])
        })

    return jsonify({
        "anio": mundial.get("anio"),
        "organizador": mundial.get("organizador"),
        "grupos": grupos,
        "premios": mundial.get("premios", []),
        "partidos": partidos_clean
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
