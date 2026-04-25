# build_mongo_collections.py
import json
from pathlib import Path

D = Path("json_output")

def load(name):
    p = D / f"{name}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else []

# Cargar todas las tablas
mundiales   = {r["id_mu"]: r for r in load("4mundial")}
paises      = {r["id_pa"]: r for r in load("5pais")}
fases       = {r["id_fa"]: r["nombre_fa"] for r in load("1fase")}
grupos      = {r["id_gr"]: r["nombre_gr"].strip() for r in load("2grupo")}
tipos_pre   = {r["id_ti_pre"]: r["nombre_ti_pre"] for r in load("6tipo_premio")}
tipos_tar   = {r["id_ti_ta"]: r["color_tarjeta"] for r in load("7tipo_tarjeta")}
plantillas  = {r["id_pla"]: r for r in load("10plantilla")}
jugadores_d = {r["id_ju"]: r for r in load("3jugador")}
redes       = load("9red_social")
partidos    = {r["id_ev_pa"]: r for r in load("12evento_partido")}
pp          = load("17partido_plantilla")   # Partido_Plantilla
pcm         = load("14pais_clasificado_mundial")
premios     = load("8premios")
prem_jug    = load("19premios_jugador")
goles       = load("16evento_gol")
faltas      = load("15evento_falta")
ecj         = {r["id_ev_ca_ju"]: r for r in load("13evento_cambio_jugador")}
cambios     = load("20cambio_jugador")
posiciones  = load("18posicionjugador")

# ─── COLECCIÓN: jugadores ───────────────────────────────────────────────────
redes_por_jugador = {}
for r in redes:
    redes_por_jugador.setdefault(r["Jugador_id_ju"], []).append({
        "usuario": r["nombre_red_so"],
        "tipo": r["tipo_red_sp"]
    })

col_jugadores = []
for j in jugadores_d.values():
    col_jugadores.append({
        "_id": j["id_ju"],
        "nombre": j["nombre_ju"],
        "fecha_nacimiento": j.get("fecha_nacimiento_ju"),
        "lugar_nacimiento": j.get("lugar_nacimiento_ju"),
        "altura": j.get("altura_ju"),
        "apodo": j.get("apodo_ju"),
        "pagina_web": j.get("pagina_web_ju"),
        "redes_sociales": redes_por_jugador.get(j["id_ju"], [])
    })

# ─── COLECCIÓN: mundiales ───────────────────────────────────────────────────
# Mapas auxiliares

# Mapa (pais_id, mundial_id) -> director_tecnico
# Se construye pasando por partido_plantilla -> evento_partido -> mundial
dt_por_pais_mundial = {}
for pp_entry in pp:
    pla_id = pp_entry["Plantilla_id_pla"]
    partido_id = pp_entry["Evento_Partido_id_ev_pa"]
    pla = plantillas.get(pla_id)
    partido = partidos.get(partido_id)
    if pla and partido:
        key = (pla["Pais_id_pa"], partido["Llave_Mundial_id_mu"])
        if key not in dt_por_pais_mundial:
            dt_por_pais_mundial[key] = pla["director_tecnico_pla"]

pla_por_partido = {}   # partido_id -> [plantilla_id, ...]
for x in pp:
    pla_por_partido.setdefault(x["Evento_Partido_id_ev_pa"], []).append(x["Plantilla_id_pla"])

goles_por_partido = {}
for g in goles:
    goles_por_partido.setdefault(g["Evento_Partido_id_ev_pa"], []).append(g)

faltas_por_partido = {}
for f in faltas:
    faltas_por_partido.setdefault(f["Evento_Partido_id_ev_pa"], []).append(f)

cambios_por_partido = {}
for c in cambios:
    ev = ecj.get(c["Evento_Cambio_Jugador_id_ev_ca_ju"], {})
    pid = ev.get("Evento_Partido_id_ev_pa")
    if pid:
        cambios_por_partido.setdefault(pid, []).append(c)

prem_jug_por_premio = {}
for pj in prem_jug:
    prem_jug_por_premio.setdefault(pj["Premio_id_pre"], []).append(pj["Jugador_id_ju"])

pcm_por_mundial = {}
for x in pcm:
    pcm_por_mundial.setdefault(x["Mundial_id_mu"], []).append(x)

premios_por_mundial = {}
for x in premios:
    premios_por_mundial.setdefault(x["Mundial_id_mu"], []).append(x)

partidos_por_mundial = {}
for ep in partidos.values():
    mid = ep["Llave_Mundial_id_mu"]
    partidos_por_mundial.setdefault(mid, []).append(ep)

col_mundiales = []
for mu_id, mu in mundiales.items():
    # Grupos y selecciones
    grupos_doc = {}
    for x in pcm_por_mundial.get(mu_id, []):
        g_nombre = grupos.get(x["Grupo_id_gr"], "?")
        pla_dt = dt_por_pais_mundial.get((x["Pais_id_pa"], mu_id))
        grupos_doc.setdefault(g_nombre, []).append({
            "pais_id": x["Pais_id_pa"],
            "pais": paises.get(x["Pais_id_pa"], {}).get("name_pa", "?"),
            "director_tecnico": pla_dt
        })
    grupos_list = [{"nombre": k, "selecciones": v} for k, v in sorted(grupos_doc.items())]

    # Partidos
    partidos_list = []
    for ep in partidos_por_mundial.get(mu_id, []):
        pid = ep["id_ev_pa"]
        fase_nombre = fases.get(ep["Llave_Mundial_id_fa"], "?")
        plas = pla_por_partido.get(pid, [])
        eq1_id = plas[0] if len(plas) > 0 else None
        eq2_id = plas[1] if len(plas) > 1 else None

        def equipo_doc(pla_id):
            if not pla_id: return {}
            pla = plantillas.get(pla_id, {})
            pa  = paises.get(pla.get("Pais_id_pa"), {})
            return {"pais_id": pla.get("Pais_id_pa"), "pais": pa.get("name_pa","?"), "plantilla_id": pla_id}

        # Jugadores por plantilla (para nombre en goles/tarjetas)
        jug_pla = {}
        for pos in posiciones:
            if pos["Plantilla_id_pla"] in (eq1_id, eq2_id):
                jid = pos["Jugador_id_ju"]
                jug_pla[jid] = jugadores_d.get(jid, {}).get("nombre_ju", "?")

        goles_doc = [{"jugador_id": g["Jugador_id_ju"],
                      "jugador": jugadores_d.get(g["Jugador_id_ju"],{}).get("nombre_ju","?"),
                      "minuto": g["tiempo_gol"], "penal": bool(g.get("penal")),
                      "entre_tiempo": bool(g.get("entre_tiempo_ev_go"))}
                     for g in goles_por_partido.get(pid, [])]

        tarjetas_doc = [{"jugador_id": None,
                         "tipo": tipos_tar.get(f["Tipo_Tarjeta_id_ti_ta"],"?"),
                         "minuto": f["minuto_falta"],
                         "entre_tiempo": bool(f.get("entre_tiempo"))}
                        for f in faltas_por_partido.get(pid, [])]

        cambios_doc = []
        for c in cambios_por_partido.get(pid, []):
            cambios_doc.append({
                "jugador_sale_id": c["Jugador_id_ju"],
                "jugador_sale": jugadores_d.get(c["Jugador_id_ju"],{}).get("nombre_ju","?"),
                "minuto": c.get("tiempo_ca_ju")
            })

        partidos_list.append({
            "id_partido": pid,
            "fecha": ep["fecha_ev_pa"],
            "fase": fase_nombre,
            "equipo1": equipo_doc(eq1_id),
            "equipo2": equipo_doc(eq2_id),
            "goles": goles_doc,
            "tarjetas": tarjetas_doc,
            "cambios": cambios_doc
        })

    # Premios
    premios_list = []
    for pr in premios_por_mundial.get(mu_id, []):
        jugs_names = [jugadores_d.get(jid,{}).get("nombre_ju","?")
                      for jid in prem_jug_por_premio.get(pr["id_pre"],[])]
        premios_list.append({
            "tipo": tipos_pre.get(pr["Tipo_Premio_id_ti_pre"],"?"),
            "pais": pr.get("pais_pre"),
            "entrenador": pr.get("entrenador_pre"),
            "jugadores": jugs_names
        })

    col_mundiales.append({
        "_id": mu_id,
        "anio": mu["anio_mu"],
        "organizador": mu["organizador_mu"],
        "grupos": grupos_list,
        "partidos": partidos_list,
        "premios": premios_list
    })

# ─── COLECCIÓN: paises ──────────────────────────────────────────────────────
sedes_por_pais = {}
for mu in mundiales.values():
    org = mu["organizador_mu"]
    for pa_id, pa in paises.items():
        if pa["name_pa"].lower() in org.lower():
            sedes_por_pais.setdefault(pa["name_pa"], []).append(mu["anio_mu"])

part_por_pais = {}
for x in pcm:
    part_por_pais.setdefault(x["Pais_id_pa"], []).append(x)

col_paises = []
for pa_id, pa in paises.items():
    participaciones = []
    for x in part_por_pais.get(pa_id, []):
        mu = mundiales.get(x["Mundial_id_mu"], {})
        pla_dt = dt_por_pais_mundial.get((pa_id, x["Mundial_id_mu"]))
        participaciones.append({
            "mundial_id": x["Mundial_id_mu"],
            "anio": mu.get("anio_mu"),
            "grupo": grupos.get(x["Grupo_id_gr"], "?"),
            "director_tecnico": pla_dt,
            "fue_sede": pa["name_pa"] in sedes_por_pais,
            "anios_sede": sedes_por_pais.get(pa["name_pa"], [])
        })
    col_paises.append({
        "_id": pa_id,
        "nombre": pa["name_pa"],
        "participaciones": participaciones
    })

# ─── GUARDAR ────────────────────────────────────────────────────────────────
out = Path("json_output")
(out / "col_mundiales.json").write_text(json.dumps(col_mundiales, ensure_ascii=False, indent=2), encoding="utf-8")
(out / "col_jugadores.json").write_text(json.dumps(col_jugadores, ensure_ascii=False, indent=2), encoding="utf-8")
(out / "col_paises.json").write_text(json.dumps(col_paises, ensure_ascii=False, indent=2), encoding="utf-8")

print("Colecciones generadas:")
print(f"  mundiales: {len(col_mundiales)} documentos")
print(f"  jugadores: {len(col_jugadores)} documentos")
print(f"  paises:    {len(col_paises)} documentos")