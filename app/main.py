from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from . import futbol_api, config
from .modelo import probabilidades_partido

app = FastAPI(title="Predicción de resultados de fútbol")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


@app.get("/api/config")
def obtener_config():
    """Devuelve las ligas configuradas (país -> league_id) y la temporada."""
    return {"season": config.SEASON, "ligas": config.LIGAS}


@app.get("/api/ligas")
def api_buscar_ligas(pais: str):
    """Ayuda a encontrar el league_id de un país (usar una sola vez para completar config.py)."""
    try:
        return futbol_api.buscar_ligas(pais)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@app.get("/api/equipos")
def api_buscar_equipo(league_id: int, nombre: str, season: int = config.SEASON):
    try:
        return futbol_api.buscar_equipo(league_id, season, nombre)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@app.get("/api/fixtures")
def api_fixtures(fecha: str, league_id: int, season: int = config.SEASON):
    """fecha en formato YYYY-MM-DD. Ej: mañana."""
    try:
        return futbol_api.fixtures_por_fecha(fecha, league_id, season)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@app.get("/api/prediccion")
def api_prediccion(league_id: int, local_id: int, visita_id: int, season: int = config.SEASON):
    try:
        stats_local = futbol_api.stats_equipo(league_id, season, local_id)
        stats_visita = futbol_api.stats_equipo(league_id, season, visita_id)
        resultado = probabilidades_partido(stats_local, stats_visita)
        resultado["stats_local"] = stats_local
        resultado["stats_visita"] = stats_visita
        return resultado
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


# Servir el frontend (index.html + estáticos)
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
def index():
    return FileResponse(FRONTEND_DIR / "index.html")
