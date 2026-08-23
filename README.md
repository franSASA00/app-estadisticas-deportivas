# Predicción de resultados de fútbol

App local (FastAPI + web simple) para calcular probabilidades de victoria / empate /
derrota de partidos de club de **cualquier liga del mundo**, usando estadísticas reales
(goles a favor/en contra, tarjetas) y un modelo de Poisson.

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate  # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# editar .env y pegar tu API key de https://dashboard.api-football.com
```

## Usar

1. Corré la app: `uvicorn app.main:app --reload`
2. Abrí `http://localhost:8000` en el navegador.
3. Buscá una liga por nombre o por país (ej: "Premier League", "Argentina", "Serie A").
4. Elegí una de las ligas encontradas — se detecta sola la temporada activa.
5. Vas a ver los partidos programados para los próximos 7 días, agrupados por día.
6. Click en un partido para ver la predicción (% victoria local / empate / victoria visitante).

## Estructura

```
app/
  main.py        # endpoints FastAPI + sirve el frontend
  futbol_api.py  # llamadas a API-Football (ligas, equipos, stats, fixtures)
  modelo.py      # modelo de Poisson
frontend/
  index.html     # UI con buscador de ligas y Chart.js
```

## Notas

- El plan free de API-Football tiene un límite de 100 requests/día — cada predicción
  hace 2 llamadas (stats de cada equipo), así que alcanza para ~40-50 predicciones diarias.
- Si una liga no tiene "temporada activa" en este momento (fuera de calendario), no se
  va a poder consultar hasta que arranque la temporada.
