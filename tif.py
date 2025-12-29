import numpy as np

# 1. DEFINICIÓN DE DATOS
# Nombres de los sectores (Ordenados según tu lista)
sectores = [
    "Agri/Ganad/Pesca", "Minería", "Manufactura", 
    "Elec/Gas/Agua", "Construcción", "Comercio", 
    "Transporte", "Telecomu.", "Otros Servicios"
]

# Tu VAB (Datos originales)
VAB = np.array([1.683, 10.126, 3.277, 0.585, 2.530, 3.237, 1.417, 1.228, 5.364])

# Tu Matriz de Coeficientes (Datos ingresados manualmente)
# Nota: Esta matriz cruda tiene columnas que suman > 1, lo cual es imposible económicamente.
A_raw = np.array([
    [0.15, 0.10, 0.20, 0.08, 0.05, 0.12, 0.18, 0.15, 0.13],
    [0.08, 0.25, 0.12, 0.10, 0.15, 0.08, 0.12, 0.10, 0.09],
    [0.25, 0.18, 0.35, 0.20, 0.22, 0.25, 0.22, 0.20, 0.18],
    [0.05, 0.06, 0.08, 0.18, 0.10, 0.05, 0.08, 0.07, 0.06],
    [0.12, 0.14, 0.15, 0.12, 0.20, 0.15, 0.18, 0.14, 0.13],
    [0.10, 0.09, 0.10, 0.09, 0.12, 0.15, 0.10, 0.11, 0.10],
    [0.15, 0.16, 0.16, 0.15, 0.16, 0.14, 0.18, 0.15, 0.14],
    [0.08, 0.07, 0.08, 0.07, 0.08, 0.09, 0.08, 0.12, 0.08],
    [0.20, 0.20, 0.20, 0.20, 0.20, 0.20, 0.20, 0.20, 0.25]
])

# 2. CORRECCIÓN DE ESTABILIDAD (Crucial para evitar negativos)
# Escalamos los datos para que la suma de insumos sea < 1 (aprox 0.85 promedio)
sumas_columna = A_raw.sum(axis=0)
A = A_raw / sumas_columna * 0.85 

print("--- DIAGNÓSTICO DEL MODELO ---")
print(f"Suma columnas original (Error > 1): {np.round(sumas_columna, 2)}")
print(f"Suma columnas corregida (Viable):   {np.round(A.sum(axis=0), 2)}")
print("-" * 30)

# 3. CÁLCULO DE LA INVERSA DE LEONTIEF (L)
I = np.eye(9)
# L = (I - A)^-1
L = np.linalg.inv(I - A)

print("\n--- MATRIZ INVERSA DE LEONTIEF (L) ---")
# Mostramos solo los multiplicadores de Minería (Sector índice 1)
print(f"Impactos por cada S/1 extra en {sectores[1]}:")
for i, sector in enumerate(sectores):
    print(f"  -> {sector}: {L[i, 1]:.3f}")

# 4. SIMULACIÓN DE IMPACTO: Aumento de S/ 1,000 Millones en Minería
delta_demanda = np.zeros(9)
delta_demanda[1] = 1000  # 1000 millones en Minería (índice 1)

# Formula: Delta Producción = L * Delta Demanda
nuevo_impacto = L @ delta_demanda

print("\n" + "="*40)
print(" RESULTADOS SIMULACIÓN: SHOCK MINERO (+1000)")
print("="*40)

print(f"{'SECTOR':<20} | {'IMPACTO (S/ Millones)':>20}")
print("-" * 45)

for i, valor in enumerate(nuevo_impacto):
    print(f"{sectores[i]:<20} | S/ {valor:,.2f}")

print("-" * 45)
total_impacto = nuevo_impacto.sum()
print(f"{'TOTAL ECONOMÍA':<20} | S/ {total_impacto:,.2f}")
print(f"Multiplicador Final: {total_impacto/1000:.2f}x (Por cada S/1 invertido)")