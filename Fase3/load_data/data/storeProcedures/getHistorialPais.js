// getHistorialPais.js
function getHistorialPais(nombrePais, anioFiltro = null) {
  const pais = db.paises.findOne({ nombre: { $regex: new RegExp(nombrePais, "i") } });
  if (!pais) { print("País no encontrado: " + nombrePais); return; }

  print("=".repeat(60));
  print("HISTORIAL: " + pais.nombre.toUpperCase());
  print("=".repeat(60));

  const aniosSede = [...new Set(pais.participaciones.filter(p => p.fue_sede).flatMap(p => p.anios_sede))];
  print(aniosSede.length > 0
    ? "Fue sede en: " + aniosSede.join(", ")
    : "Nunca fue sede.");

  let parts = pais.participaciones;
  if (anioFiltro) parts = parts.filter(p => p.anio === anioFiltro);

  print("\nPARTICIPACIONES:");
  parts.sort((a, b) => a.anio - b.anio).forEach(p => {
    print("\n  Año " + p.anio + " — Grupo " + p.grupo + " — DT: " + (p.director_tecnico || "-"));
    // Buscar partidos jugados por este país en ese mundial
    const mundial = db.mundiales.findOne({ _id: p.mundial_id }, { partidos: 1, anio: 1 });
    if (mundial) {
      const partidosPais = mundial.partidos.filter(pa =>
        pa.equipo1.pais?.toLowerCase() === pais.nombre.toLowerCase() ||
        pa.equipo2.pais?.toLowerCase() === pais.nombre.toLowerCase()
      );
      partidosPais.forEach(pa => {
        print("    " + pa.fecha + " [" + pa.fase + "] " + pa.equipo1.pais + " vs " + pa.equipo2.pais);
      });
    }
  });
}

// Uso: getHistorialPais("Brasil")
// Uso con filtro: getHistorialPais("Argentina", 2022)
