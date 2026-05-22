import pandas as pd
from faker import Faker
import random

fake = Faker('es_ES')

# =========================
# 1. DIMENSIONES NORMALIZADAS (SNOWFLAKE)
# =========================

# --- DIM REGIONES ---
regiones = ["Occidente", "Centro", "Oriente", "Norte", "Sur"]
dim_regiones = pd.DataFrame({
    "id_region": range(1, len(regiones) + 1),
    "nombre_region": regiones
})

# --- DIM SEDES (Conectada a Regiones) ---
sedes = ["San Salvador", "Santa Ana", "San Miguel", "Soyapango", "La Libertad"]
dim_sedes = pd.DataFrame({
    "id_sede": range(1, len(sedes) + 1),
    "nombre_sede": sedes,
    "id_region": [2, 1, 3, 2, 4] # FK hacia regiones
})

# --- DIM DEPARTAMENTOS ---
departamentos = ["IT", "Recursos Humanos", "Finanzas", "Operaciones", "Ventas"]
dim_departamentos = pd.DataFrame({
    "id_departamento": range(1, len(departamentos) + 1),
    "nombre_departamento": departamentos
})

# --- DIM PUESTOS (Conectada a Departamentos) ---
puestos = ["Desarrollador", "Reclutador", "Contador", "Supervisor", "Ejecutivo de Ventas"]
dim_puestos = pd.DataFrame({
    "id_puesto": range(1, len(puestos) + 1),
    "nombre_puesto": puestos,
    "id_departamento": [1, 2, 3, 4, 5] # FK hacia departamentos
})

# --- DIM EMPLEADOS (Conectada a Puestos y Sedes) ---
empleados_data = []
for i in range(1, 151): # 150 Empleados únicos
    empleados_data.append({
        "id_empleado": i,
        "nombre_empleado": fake.name(),
        "id_sede": random.randint(1, len(sedes)),
        "id_puesto": random.randint(1, len(puestos))
    })
dim_empleados = pd.DataFrame(empleados_data)

# --- DIM TIEMPO ---
tiempo_data = []
for mes in range(1, 11): # 10 meses simulados
    tiempo_data.append({
        "id_tiempo": mes,
        "mes": mes,
        "anio": 2026
    })
dim_tiempo = pd.DataFrame(tiempo_data)

# =========================
# 2. FACT TABLE (SALARIOS)
# =========================
# 150 empleados * 10 meses = 1500 registros exactos (Cumple el requerimiento)
salarios_data = []
id_salario_contador = 1

for empleado in empleados_data:
    # Salario base fijo por empleado para dar lógica a los datos
    salario_base = random.randint(800, 4500) 
    
    for mes in tiempo_data:
        # Variación mensual pequeña (bonos/descuentos)
        salario_final = salario_base + random.randint(-50, 200)
        
        salarios_data.append({
            "id_salario": id_salario_contador,
            "id_empleado": empleado["id_empleado"], # FK hacia Empleados
            "id_tiempo": mes["id_tiempo"],          # FK hacia Tiempo
            "salario": salario_final
        })
        id_salario_contador += 1

fact_salarios = pd.DataFrame(salarios_data)

print("=== MUESTRA FACT SALARIOS ===")
print(fact_salarios.head())
print(f"Total registros generados: {len(fact_salarios)}\n")

# =========================
# 3. SNOWFLAKE MODEL (JOINS)
# =========================
# Paso 1: Unir Hechos con Dimensiones directas (Empleados y Tiempo)
modelo = fact_salarios.merge(dim_empleados, on="id_empleado").merge(dim_tiempo, on="id_tiempo")

# Paso 2: Normalización Snowflake (Expandir Empleados hacia Sedes y Puestos)
modelo = modelo.merge(dim_sedes, on="id_sede").merge(dim_puestos, on="id_puesto")

# Paso 3: Normalización Profunda Snowflake (Expandir hacia Regiones y Departamentos)
modelo = modelo.merge(dim_regiones, on="id_region").merge(dim_departamentos, on="id_departamento")

# =========================
# 4. ANÁLISIS Y MOSTRAR 
# =========================

print("\n=== 4.1 SALARIOS POR REGIÓN (Promedio) ===")
df_region = modelo[["nombre_region", "salario"]].groupby("nombre_region").mean().reset_index()
df_region = df_region.sort_values("salario", ascending=False).reset_index(drop=True)
df_region.index = df_region.index + 1
print(df_region)

print("\n=== 4.2 SALARIOS POR PUESTO (Promedio) ===")
df_puesto = modelo[["nombre_puesto", "salario"]].groupby("nombre_puesto").mean().reset_index()
df_puesto = df_puesto.sort_values("salario", ascending=False).reset_index(drop=True)
df_puesto.index = df_puesto.index + 1
print(df_puesto)git
