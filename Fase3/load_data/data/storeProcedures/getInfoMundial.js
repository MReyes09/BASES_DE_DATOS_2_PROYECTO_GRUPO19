// getInfoMundial.js
function getInfoMundial(anio, filtroGrupo = null, filtroPais = null) {
  const mundial = db.mundiales.findOne({ anio: anio });
  if (!mundial) { print("Mundial no encontrado para el año: " + anio); return; }

  print("=".repeat(60));
  print("MUNDIAL " + mundial.anio + " — " + mundial.organizador);
  print("=".repeat(60));

  let grupos = mundial.grupos;
  if (filtroGrupo) grupos = grupos.filter(g => g.nombre === filtroGrupo);
  if (filtroPais)  grupos = grupos.map(g => ({
    ...g,
    selecciones: g.selecciones.filter(s => s.pais.toLowerCase().includes(filtroPais.toLowerCase()))
  })).filter(g => g.selecciones.length > 0);

  print("\n--- GRUPOS Y SELECCIONES ---");
  grupos.forEach(g => {
    print("Grupo " + g.nombre + ":");
    g.selecciones.forEach(s => print("  " + s.pais + " — DT: " + (s.director_tecnico || "-")));
  });

  print("\n--- PREMIOS ---");
  mundial.premios.forEach(p => {
    print("  " + p.tipo + ": " + (p.jugadores.join(", ") || p.pais || "-"));
  });

  print("\n--- PARTIDOS ---");
  let partidos = mundial.partidos;
  if (filtroPais) partidos = partidos.filter(p =>
    p.equipo1.pais?.toLowerCase().includes(filtroPais.toLowerCase()) ||
    p.equipo2.pais?.toLowerCase().includes(filtroPais.toLowerCase())
  );

  partidos.forEach(p => {
    const g1 = p.goles.filter(g => g.jugador_id && p.equipo1.plantilla_id).length;
    const g2 = p.goles.length - g1;
    print("\n  [" + p.fecha + "] " + p.fase);
    print("  " + p.equipo1.pais + " " + g1 + " - " + g2 + " " + p.equipo2.pais);
    if (p.goles.length > 0) {
      print("  Goles: " + p.goles.map(g => g.jugador + " (" + g.minuto + "'" + (g.penal ? " P" : "") + ")").join(", "));
    }
  });
}

// Uso: getInfoMundial(2022)
// Uso con filtro: getInfoMundial(2022, "A")
// Uso con país:   getInfoMundial(2022, null, "Argentina")