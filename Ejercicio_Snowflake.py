import pandas as pd
from faker import Faker
import random

fake = Faker()

# =========================
# DIM REGIONES
# =========================
regiones = ["Occidente", "Centro", "Oriente", "Norte", "Sur"]

dim_regiones = pd.DataFrame({
    "id_region": range(1, len(regiones) + 1),
    "nombre_region": regiones
})

print("\n=== DIM REGIONES ===")
print(dim_regiones.head())

# =========================
# DIM SEDES
# =========================
sedes = ["San Salvador", "Santa Ana", "San Miguel", "Soyapango", "La Libertad"]

dim_sedes = pd.DataFrame({
    "id_sede": range(1, len(sedes) + 1),
    "nombre_sede": sedes,
    "id_region": [2, 1, 3, 2, 4]
})

print("\n=== DIM SEDES ===")
print(dim_sedes.head())

# =========================
# DIM PUESTOS
# =========================
puestos = ["Analista", "Gerente", "Supervisor", "Desarrollador", "RRHH"]

dim_puestos = pd.DataFrame({
    "id_puesto": range(1, len(puestos) + 1),
    "nombre_puesto": puestos
})

print("\n=== DIM PUESTOS ===")
print(dim_puestos.head())

# =========================
# FACT TABLE (EMPLEADOS)
# =========================
empleados = []

for i in range(1500):
    empleados.append({
        "id_empleado": i + 1,
        "nombre": fake.name(),
        "salario": random.randint(500, 5000),
        "id_sede": random.randint(1, len(sedes)),
        "id_puesto": random.randint(1, len(puestos))
    })

fact_empleados = pd.DataFrame(empleados)

print("\n=== FACT EMPLEADOS ===")
print(fact_empleados.head())

# =========================
# SNOWFLAKE MODEL (JOINS)
# =========================
empleados_sedes = fact_empleados.merge(dim_sedes, on="id_sede")
modelo_final = empleados_sedes.merge(dim_puestos, on="id_puesto")

# unir regiones (snowflake real)
modelo_final = modelo_final.merge(dim_regiones, on="id_region")

print("\n=== MODELO FINAL ===")
print(modelo_final.head())

# =========================
# ANALISIS
# =========================
print("\n=== SALARIO PROMEDIO POR PUESTO ===")
print(modelo_final.groupby("nombre_puesto")["salario"].mean())

print("\n=== SALARIO PROMEDIO POR REGION ===")
print(modelo_final.groupby("nombre_region")["salario"].mean())

print("\n✔ PROCESO COMPLETADO EXITOSAMENTE")
