# Predicción de resultados de fútbol

App local (FastAPI + web simple) para calcular probabilidades de victoria / empate /
derrota de partidos de clubes en Argentina, Irlanda, Inglaterra, España y Estados Unidos,
usando estadísticas reales (goles a favor/en contra, tarjetas) y un modelo de Poisson.

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate  # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# editar .env y pegar tu API key de https://dashboard.api-football.com
```

## Configurar las ligas (una sola vez)

1. Corré la app: `uvicorn app.main:app --reload`
2. Andá a `http://localhost:8000/api/ligas?pais=Argentina` (y repetí para Ireland, England,
   Spain, USA) para ver los `league_id` disponibles.
3. Completá `app/config.py` con el `league_id` de la primera división de cada país.
4. Reiniciá la app.

## Usar

1. Abrí `http://localhost:8000` en el navegador.
2. Elegí liga y fecha (por defecto, mañana).
3. Buscá los partidos programados y hacé click en uno para ver la predicción.

## Estructura

```
app/
  main.py        # endpoints FastAPI + sirve el frontend
  futbol_api.py  # llamadas a API-Football
  modelo.py      # modelo de Poisson
  config.py      # league_id de cada país + temporada
frontend/
  index.html     # UI simple con Chart.js
```
