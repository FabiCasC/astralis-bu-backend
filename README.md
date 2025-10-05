# Proyecto de Backend Astralis BU

Este proyecto es un servicio de backend desarrollado en Flask. Su propósito principal es interactuar con la API de la NASA para obtener datos sobre Objetos Cercanos a la Tierra (NEO, por sus siglas en inglés). Además, ofrece funcionalidades para calcular y simular trayectorias de estos objetos.

## Endpoints

A continuación se detallan los endpoints disponibles:

---

### 1. Obtener datos de NEOs en un rango de fechas

-   **Descripción:** Recupera datos de objetos cercanos a la Tierra desde la API de la NASA para un rango de fechas específico.
-   **Método:** `GET`
-   **URL:** `/nasa/feed`
-   **Argumentos (Query Params):**
    -   `start_date` (opcional): La fecha de inicio para la búsqueda. Si no se especifica, se utiliza el día anterior a la fecha actual. Formato: `YYYY-MM-DD`.
    -   `end_date` (opcional): La fecha de fin para la búsqueda. Si no se especifica, se utiliza la fecha actual. Formato: `YYYY-MM-DD`.

### 2. Obtener datos de un NEO por su ID

-   **Descripción:** Consulta la información de un objeto cercano a la Tierra específico utilizando su ID de asteroide.
-   **Método:** `GET`
-   **URL:** `/nasa/neo`
-   **Argumentos (Query Params):**
    -   `asteroid_id` (requerido): El ID del asteroide que se desea consultar.

### 3. Obtener una trayectoria simulada (mock)

-   **Descripción:** Devuelve una trayectoria de datos simulada y determinista para un NEO específico, útil para pruebas.
-   **Método:** `GET`
-   **URL:** `/nasa/mock_trajectory/<neo_id>`
-   **Argumentos (Path Params):**
    -   `neo_id` (requerido): El ID del Objeto Cercano a la Tierra.

### 4. Calcular la trayectoria de un NEO

-   **Descripción:** Calcula la trayectoria de un NEO en el campo gravitacional de la Tierra, determinando si impactará y calculando la energía del impacto. Si no se proporcionan la posición y velocidad, se estiman a partir de los datos de aproximación cercana de la NASA.
-   **Método:** `GET`
-   **URL:** `/nasa/trajectory/<neo_id>`
-   **Argumentos:**
    -   **Path Param:**
        -   `neo_id` (requerido): El ID del Objeto Cercano a la Tierra.
    -   **Query Params:**
        -   `position_km` (opcional): El vector de posición inicial en kilómetros. Debe ser una cadena de texto que represente una lista de Python (ej: `"[x, y, z]"`).
        -   `velocity_kms` (opcional): El vector de velocidad inicial en kilómetros por segundo. Debe ser una cadena de texto que represente una lista de Python (ej: `"[vx, vy, vz]"`).
        -   `dt` (opcional): El paso de tiempo para la simulación en segundos. El valor por defecto es `0.5`.
        -   `density_kg_m3` (opcional): La densidad del objeto en kg/m³. Por defecto es `100`.

-   **Estructura de Salida Esperada (JSON):**

    ```json
    {
        "trajectory": [
            {
                "t_s": "float (tiempo en segundos)",
                "x_km": "float",
                "y_km": "float",
                "z_km": "float",
                "r_km": "float (distancia al centro de la Tierra)",
                "v_km_s": "float (magnitud de la velocidad)",
                "velocity_km_s": "[vx, vy, vz] (vector de velocidad)"
            }
        ],
        "mass_kg": "float (masa del NEO)",
        "diameter_m": "float (diámetro del NEO)",
        "density_kg_m3": "float (densidad del NEO)",
        "dt": "float (paso de tiempo de la simulación)",
        "max_time": "float (tiempo máximo de la simulación)",
        "impact": "boolean (indica si hubo impacto)",
        "impact_details": {
            "impact_time_s": "float",
            "impact_speed_km_s": "float",
            "impact_energy_megatons": "float (energía en megatones de TNT)",
            "impact_energy_joules": "float",
            "impact_energy_transferred_joules": "float",
            "impact_energy_transferred_mu_joules": "float",
            "richter_magnitude": "float (magnitud estimada en escala de Richter)",
            "impact_angle_deg": "float (ángulo de impacto en grados)"
        },
        "neo_data": {
            "id": "string",
            "designation": "string",
            "is_potentially_hazardous_asteroid": "boolean",
            "name": "string",
            "orbital_data": "{...} (datos orbitales del NEO)"
        }
    }
    ```

### 5. Obtener IDs de NEOs para Explorar

-   **Descripción:** Devuelve una lista de todos los Objetos Cercanos a la Tierra (NEOs) disponibles a través del endpoint de exploración (`/browse`) de la API de la NASA. Proporciona el ID y el nombre de cada NEO.
-   **Método:** `GET`
-   **URL:** `/nasa/get_browse_ids`
-   **Argumentos:** Ninguno.
-   **Estructura de Salida Esperada (JSON):**

    ```json
    [
        {
            "id": "string",
            "name": "string"
        },
        {
            "id": "string",
            "name": "string"
        }
    ]
    ```