"""Completá LIGAS con los league_id reales una vez que los encuentres con /api/ligas.

Ejemplo de flujo:
  1. Corré la app y andá a /api/ligas?pais=Argentina (y lo mismo para los otros 4 países)
  2. Copiá el league_id de la liga de primera división de cada uno
  3. Pegalos acá abajo
"""

SEASON = 2025

LIGAS = {
    "Argentina": None,  # Liga Profesional Argentina
    "Ireland": None,    # Premier Division
    "England": None,    # Premier League
    "Spain": None,       # La Liga
    "USA": None,         # MLS
}
