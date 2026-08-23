from datetime import date, timedelta
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from . import futbol_api
from .modelo import probabilidades_partido

app = FastAPI(title="Predicción de resultados de fútbol")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


@app.get("/api/ligas")
def api_buscar_ligas(pais: str | None = None, nombre: str | None = None):
    """Busca ligas de cualquier país del mundo por país y/o nombre. Al menos uno es obligatorio."""
    if not pais and not nombre:
        raise HTTPException(status_code=400, detail="Pasá 'pais' y/o 'nombre' para buscar.")
    try:
        return futbol_api.buscar_ligas(pais=pais, nombre=nombre)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@app.get("/api/equipos")
def api_buscar_equipo(league_id: int, season: int, nombre: str):
    try:
        return futbol_api.buscar_equipo(league_id, season, nombre)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@app.get("/api/fixtures")
def api_fixtures(league_id: int, season: int, dias: int = 7):
    """Partidos programados de una liga desde hoy hasta 'dias' días adelante (default 7 = una semana)."""
    hoy = date.today()
    hasta = hoy + timedelta(days=dias)
    try:
        return futbol_api.fixtures_en_rango(league_id, season, hoy.isoformat(), hasta.isoformat())
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@app.get("/api/prediccion")
def api_prediccion(league_id: int, season: int, local_id: int, visita_id: int):
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
