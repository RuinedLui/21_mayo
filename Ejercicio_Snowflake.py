import random
import pandas as pd
from datetime import date
from faker import Faker

fake = Faker("es_ES")
random.seed(42)
Faker.seed(42)

# ═══════════════════════════════════════════════════════
#  1. DIMENSIÓN DEPARTAMENTOS  (normalizada)
# ═══════════════════════════════════════════════════════

# ── dim_regiones ──
df_regiones = pd.DataFrame([
    {"nombre_region": "Norte",     "pais": "El Salvador"},
    {"nombre_region": "Sur",       "pais": "El Salvador"},
    {"nombre_region": "Central",   "pais": "El Salvador"},
    {"nombre_region": "Occidente", "pais": "El Salvador"},
    {"nombre_region": "Oriente",   "pais": "El Salvador"},
])
df_regiones.index      = range(1, len(df_regiones) + 1)
df_regiones.index.name = "id_region"

# ── dim_sedes ──
df_sedes = pd.DataFrame([
    {"id_region": 1, "nombre_sede": "Sede Santa Ana",    "ciudad": "Santa Ana"},
    {"id_region": 2, "nombre_sede": "Sede Sonsonate",    "ciudad": "Sonsonate"},
    {"id_region": 3, "nombre_sede": "Sede San Salvador", "ciudad": "San Salvador"},
    {"id_region": 4, "nombre_sede": "Sede Ahuachapán",   "ciudad": "Ahuachapán"},
    {"id_region": 5, "nombre_sede": "Sede San Miguel",   "ciudad": "San Miguel"},
    {"id_region": 3, "nombre_sede": "Sede Mejicanos",    "ciudad": "Mejicanos"},
])
df_sedes.index      = range(1, len(df_sedes) + 1)
df_sedes.index.name = "id_sede"

# ── dim_departamentos ──
df_departamentos = pd.DataFrame([
    {"id_sede": 1, "nombre_depto": "Recursos Humanos",    "presupuesto": 350000.00},
    {"id_sede": 1, "nombre_depto": "Finanzas",            "presupuesto": 420000.00},
    {"id_sede": 2, "nombre_depto": "Tecnología",          "presupuesto": 600000.00},
    {"id_sede": 2, "nombre_depto": "Marketing",           "presupuesto": 280000.00},
    {"id_sede": 3, "nombre_depto": "Operaciones",         "presupuesto": 500000.00},
    {"id_sede": 3, "nombre_depto": "Legal",               "presupuesto": 310000.00},
    {"id_sede": 4, "nombre_depto": "Ventas",              "presupuesto": 390000.00},
    {"id_sede": 5, "nombre_depto": "Logística",           "presupuesto": 460000.00},
    {"id_sede": 6, "nombre_depto": "Administración",      "presupuesto": 275000.00},
    {"id_sede": 6, "nombre_depto": "Atención al Cliente", "presupuesto": 230000.00},
])
df_departamentos.index      = range(1, len(df_departamentos) + 1)
df_departamentos.index.name = "id_departamento"

# ══════════════════════════════════════
#  2. DIMENSIÓN TIEMPO 
# ══════════════════════════════════════

DIAS_ES  = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
MESES_ES = ["","Enero","Febrero","Marzo","Abril","Mayo","Junio",
            "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]

fechas = pd.date_range(start="2020-01-01", end="2024-12-31", freq="D")
df_tiempo = pd.DataFrame({
    "fecha":      fechas.date,
    "dia":        fechas.day,
    "semana":     fechas.isocalendar().week.astype(int),
    "mes":        fechas.month,
    "trimestre":  fechas.quarter,
    "anio":       fechas.year,
    "nombre_dia": [DIAS_ES[d] for d in fechas.weekday],
    "nombre_mes": [MESES_ES[m] for m in fechas.month],
})
df_tiempo.index      = range(1, len(df_tiempo) + 1)
df_tiempo.index.name = "id_tiempo"

# ══════════════════════════════════════
#  3. DIMENSIÓN EMPLEADOS  
# ══════════════════════════════════════

PUESTOS = [
    ("Analista Jr",            "Junior",     900.00),
    ("Analista Sr",            "Senior",    1400.00),
    ("Coordinador",            "Medio",     1800.00),
    ("Gerente de Área",        "Alto",      2800.00),
    ("Director",               "Directivo", 4200.00),
    ("Desarrollador Jr",       "Junior",    1000.00),
    ("Desarrollador Sr",       "Senior",    1700.00),
    ("Arquitecto de Software", "Experto",   2500.00),
    ("Especialista RRHH",      "Medio",     1300.00),
    ("Asesor Legal",           "Senior",    2000.00),
]

empleados = []
emails_usados: set[str] = set()

for i in range(1, 151):
    nombre   = fake.first_name()
    apellido = fake.last_name()
    puesto, nivel, salario_base = random.choice(PUESTOS)

    base  = f"{nombre.lower()}.{apellido.lower()}{i}".replace(" ", "")
    email = f"{base}@empresa.com"
    while email in emails_usados:
        email = f"{base}_{random.randint(1, 999)}@empresa.com"
    emails_usados.add(email)

    fecha_contratacion = fake.date_between(
        start_date=date(2018, 1, 1),
        end_date=date(2023, 12, 31)
    )
    estado = random.choices(["Activo", "Inactivo"], weights=[90, 10])[0]

    empleados.append({
        "nombre":             nombre,
        "apellido":           apellido,
        "puesto":             puesto,
        "nivel":              nivel,
        "salario_base":       salario_base,
        "fecha_contratacion": fecha_contratacion,
        "email":              email,
        "estado":             estado,
    })

df_empleados = pd.DataFrame(empleados)
df_empleados.index      = range(1, len(df_empleados) + 1)
df_empleados.index.name = "id_empleado"

# ═══════════════════════════════════════
#  PREVISUALIZACIÓN
# ═══════════════════════════════════════

print("=" * 52)
print("  SNOWFLAKE SCHEMA — RRHH")
print("=" * 52)

tablas = [
    ("dim_regiones",      df_regiones),
    ("dim_sedes",         df_sedes),
    ("dim_departamentos", df_departamentos),
    ("dim_tiempo",        df_tiempo),
    ("dim_empleados",     df_empleados),
]
for nombre, df in tablas:
    print(f"  {nombre:<25} → {len(df):>5} registros")

print("\n--- dim_departamentos (vista enriquecida) ---")
df_vista = (
    df_departamentos
    .merge(df_sedes[["nombre_sede", "id_region"]], left_on="id_sede", right_index=True)
    .merge(df_regiones[["nombre_region"]], left_on="id_region", right_index=True)
    [["nombre_depto", "nombre_sede", "nombre_region", "presupuesto"]]
)
print(df_vista.to_string())

print("\n--- dim_tiempo (primeras 5 filas) ---")
print(df_tiempo.head().to_string())

print("\n--- dim_empleados (primeras 5 filas) ---")
print(df_empleados.head().to_string())

