"""Wrapper de la API-Football: ligas, equipos, estadísticas y fixtures por fecha."""
import os
import requests

BASE_URL = "https://v3.football.api-sports.io"


def _headers() -> dict:
    api_key = os.environ.get("API_FOOTBALL_KEY")
    if not api_key:
        raise RuntimeError(
            "Falta la variable de entorno API_FOOTBALL_KEY. "
            "Creá un archivo .env (ver .env.example) con tu API key."
        )
    return {"x-apisports-key": api_key}


def buscar_ligas(pais: str) -> list[dict]:
    resp = requests.get(f"{BASE_URL}/leagues", headers=_headers(), params={"country": pais})
    resp.raise_for_status()
    data = resp.json()["response"]
    return [
        {"league_id": item["league"]["id"], "nombre": item["league"]["name"], "tipo": item["league"]["type"]}
        for item in data
    ]


def buscar_equipo(league_id: int, season: int, nombre_equipo: str) -> list[dict]:
    resp = requests.get(
        f"{BASE_URL}/teams",
        headers=_headers(),
        params={"league": league_id, "season": season, "search": nombre_equipo},
    )
    resp.raise_for_status()
    data = resp.json()["response"]
    return [{"team_id": item["team"]["id"], "nombre": item["team"]["name"]} for item in data]


def stats_equipo(league_id: int, season: int, team_id: int) -> dict:
    resp = requests.get(
        f"{BASE_URL}/teams/statistics",
        headers=_headers(),
        params={"league": league_id, "season": season, "team": team_id},
    )
    resp.raise_for_status()
    d = resp.json()["response"]

    goles_favor_prom = float(d["goals"]["for"]["average"]["total"])
    goles_contra_prom = float(d["goals"]["against"]["average"]["total"])
    amarillas = sum(v["total"] or 0 for v in d["cards"]["yellow"].values())
    rojas = sum(v["total"] or 0 for v in d["cards"]["red"].values())
    partidos_jugados = d["fixtures"]["played"]["total"]

    return {
        "team_id": team_id,
        "nombre": d["team"]["name"],
        "goles_favor_prom": goles_favor_prom,
        "goles_contra_prom": goles_contra_prom,
        "amarillas_total": amarillas,
        "rojas_total": rojas,
        "amarillas_prom": amarillas / partidos_jugados if partidos_jugados else 0,
        "rojas_prom": rojas / partidos_jugados if partidos_jugados else 0,
        "partidos_jugados": partidos_jugados,
    }


def fixtures_por_fecha(fecha: str, league_id: int, season: int) -> list[dict]:
    """fecha en formato YYYY-MM-DD. Devuelve los partidos programados de esa liga ese día."""
    resp = requests.get(
        f"{BASE_URL}/fixtures",
        headers=_headers(),
        params={"date": fecha, "league": league_id, "season": season},
    )
    resp.raise_for_status()
    data = resp.json()["response"]
    return [
        {
            "fixture_id": item["fixture"]["id"],
            "fecha": item["fixture"]["date"],
            "estado": item["fixture"]["status"]["short"],
            "local_id": item["teams"]["home"]["id"],
            "local_nombre": item["teams"]["home"]["name"],
            "visita_id": item["teams"]["away"]["id"],
            "visita_nombre": item["teams"]["away"]["name"],
        }
        for item in data
    ]
