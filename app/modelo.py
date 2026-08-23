"""Modelo de Poisson: probabilidad de victoria / empate / derrota entre dos equipos."""
from scipy.stats import poisson

PROMEDIO_LIGA = 1.3  # goles/partido de referencia, simplificado


def probabilidades_partido(stats_local: dict, stats_visita: dict, max_goles: int = 6) -> dict:
    fuerza_ataque_local = stats_local["goles_favor_prom"] / PROMEDIO_LIGA
    fuerza_defensa_visita = stats_visita["goles_contra_prom"] / PROMEDIO_LIGA
    lambda_local = fuerza_ataque_local * fuerza_defensa_visita * PROMEDIO_LIGA

    fuerza_ataque_visita = stats_visita["goles_favor_prom"] / PROMEDIO_LIGA
    fuerza_defensa_local = stats_local["goles_contra_prom"] / PROMEDIO_LIGA
    lambda_visita = fuerza_ataque_visita * fuerza_defensa_local * PROMEDIO_LIGA

    prob_local_goles = [poisson.pmf(i, lambda_local) for i in range(max_goles + 1)]
    prob_visita_goles = [poisson.pmf(i, lambda_visita) for i in range(max_goles + 1)]

    p_gana_local = p_empate = p_gana_visita = 0.0
    for gl in range(max_goles + 1):
        for gv in range(max_goles + 1):
            p = prob_local_goles[gl] * prob_visita_goles[gv]
            if gl > gv:
                p_gana_local += p
            elif gl == gv:
                p_empate += p
            else:
                p_gana_visita += p

    return {
        "equipo_local": stats_local["nombre"],
        "equipo_visita": stats_visita["nombre"],
        "goles_esperados_local": round(lambda_local, 2),
        "goles_esperados_visita": round(lambda_visita, 2),
        "prob_gana_local": round(p_gana_local * 100, 1),
        "prob_empate": round(p_empate * 100, 1),
        "prob_gana_visita": round(p_gana_visita * 100, 1),
    }
