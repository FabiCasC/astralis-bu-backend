# gravity_impact_sim.py
import numpy as np
from astropy.constants import G
from app.services.nasa import query_neo_by_id
import numpy as np
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


EARTH_MASS = 5.97219e24  # kg
EARTH_RADIUS_KM = 6371.0
G_VALUE = G.value  # m^3 / (kg s^2)
KM_TO_M = 1000.0




def simulate_impact_trajectory(
    neo_id,
    position_km, velocity_kms,
    diameter_m=None, density_kg_m3=None,
    dt=0.1, max_time=3600*3
):
    """
    Simula la trayectoria del asteroide en campo gravitacional de la Tierra
    hasta el impacto con la superficie, usando la fuerza gravitacional explícita.

    Parámetros
    ----------
    position_km : list[float]
        [x, y, z] posición inicial en km (geocéntrica).
    velocity_kms : list[float]
        [vx, vy, vz] velocidad inicial en km/s.
    diameter_m : float, opcional
        Diámetro del asteroide en metros.
    density_kg_m3 : float, opcional
        Densidad del asteroide (kg/m³).
    dt : float
        Paso de integración en segundos.
    max_time : float
        Tiempo máximo de simulación (segundos).

    Retorna
    -------
    dict con:
        - trajectory: lista de {t, x, y, z, r, v}
        - impact: bool
        - impact_time_s
        - impact_speed_km_s
        - impact_energy_megatons (si masa definida)
    """
    logging.info(f"Simulating impact trajectory for NEO {neo_id} with position {position_km} and velocity {velocity_kms}")
    # Convertir unidades iniciales
    r = np.array(position_km, dtype=float) * KM_TO_M      # m
    v = np.array(velocity_kms, dtype=float) * KM_TO_M     # m/s

    t = 0.0
    trajectory = []
    impact = False

    # Calcular masa si hay densidad y diámetro
    mass_kg = None
    if diameter_m is not None and density_kg_m3 is not None:
        radius_m = diameter_m / 2.0
        volume_m3 = (4/3) * np.pi * radius_m**3
        mass_kg = volume_m3 * density_kg_m3
    else:
        # si no hay masa definida, asumimos 1 kg (no afecta la trayectoria)
        mass_kg = 1.0

    while t < max_time:
        r_norm = np.linalg.norm(r)
        if r_norm <= EARTH_RADIUS_KM * KM_TO_M:
            impact = True
            break

        # Fuerza gravitacional: F = -G * M_e * m / r^2 * (r̂)
        F = -G_VALUE * EARTH_MASS * mass_kg * r / (r_norm**3)

        # Aceleración: a = F / m = -G * M_e / r^2 * r̂
        a = F / mass_kg

        # Integración Leapfrog (semiexplícita)
        v_half = v + 0.5 * a * dt
        r = r + v_half * dt
        r_norm_new = np.linalg.norm(r)

        # recalcular aceleración con nueva posición
        F_new = -G_VALUE * EARTH_MASS * mass_kg * r / (r_norm_new**3)
        a_new = F_new / mass_kg
        v = v_half + 0.5 * a_new * dt

        t += dt

        trajectory.append({
            "t_s": t,
            "x_km": r[0] / KM_TO_M,
            "y_km": r[1] / KM_TO_M,
            "z_km": r[2] / KM_TO_M,
            "r_km": r_norm_new / KM_TO_M,
            "v_km_s": float(np.linalg.norm(v) / KM_TO_M)
        })

    result = {
        "impact": impact,
        "trajectory": trajectory,
        "mass_kg": mass_kg,
        "diameter_m": diameter_m,
        "density_kg_m3": density_kg_m3,
        "dt": dt,
        "max_time": max_time,
    }

    if impact:
        impact_speed = np.linalg.norm(v) / KM_TO_M
        result["impact_time_s"] = t
        result["impact_speed_km_s"] = impact_speed
        if mass_kg is not None and diameter_m is not None:
            energy_joules = 0.5 * mass_kg * (impact_speed * 1000)**2
            energy_megatons = energy_joules / 4.184e15
            result["impact_energy_megatons"] = energy_megatons
        logging.info(f"Impact detected for NEO {neo_id}")

    return result

def get_trajectory_by_neoid(id: int, position_km: list[float] = None, velocity_kms: list[float] = None, density_kg_m3: float=100, dt: float=0.5):
    neo_data = query_neo_by_id(id)
    if not position_km:
        position_km = [ float(close_approach["miss_distance"]["kilometers"]) for close_approach in neo_data["close_approach_data"] ]
        avg_position_km = sum(position_km) / len(position_km)
        position_km = np.power([avg_position_km]/3, 1/3)*np.array([1, 1, 1])
    if not velocity_kms:
        velocities = [ float(close_approach["relative_velocity"]["kilometers_per_second"]) for close_approach in neo_data["close_approach_data"] ]
        avg_velocity_kms = sum(velocities) / len(velocities)
        velocity_kms = np.power([avg_velocity_kms]/3, 1/3)*np.array([1, 1, 1])
    
    diameter_m = float(neo_data["estimated_diameter"]["meters"]["estimated_diameter_max"])
    max_time = 4000

    logging.info(f"Getting trajectory for NEO {id} with position {position_km} and velocity {velocity_kms}")


    trajectory_simulated = simulate_impact_trajectory(id, position_km, velocity_kms, diameter_m, density_kg_m3, dt, max_time)
    
    data_keys = ["id", "designation", "is_potentially_hazardous_asteroid", "name", "orbital_data"]
    trajectory_simulated["neo_data"] = {key: neo_data[key] for key in data_keys}
    logging.info(f"Trajectory simulated for NEO {id}")
    return trajectory_simulated




# -------------------------
# Ejemplo de uso
# -------------------------
if __name__ == "__main__":
    # Posición a 8000 km del centro (~1629 km sobre superficie)
    pos0 = [8000, 0, 0]        # km
    # Velocidad inicial con componente tangencial
    vel0 = [0, -5, -1]         # km/s

    out = simulate_impact_trajectory(
        position_km=pos0,
        velocity_kms=vel0,
        diameter_m=50,           # 50 m
        density_kg_m3=100,      # roca típica
        dt=0.5,
        max_time=4000
    )

    print(f"Impacto: {out['impact']}")
    if out['impact']:
        print(f"Tiempo hasta impacto: {out['impact_time_s']:.2f} s")
        print(f"Velocidad de impacto: {out['impact_speed_km_s']:.3f} km/s")
        print(f"Energía: {out['impact_energy_megatons']:.3f} Mt")

    import json
    with open("impact_trajectory.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nTrayectoria guardada en impact_trajectory.json ✅")
