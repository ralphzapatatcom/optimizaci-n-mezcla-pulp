import pulp
import numpy as np
import matplotlib.pyplot as plt

# 1. Datos con NumPy
nutrientes = np.array([
    [0.10, 0.40], # Proteína (Maíz, Soya)
    [0.80, 0.30]  # Fibra (Maíz, Soya)
])
costos = np.array([0.30, 0.90])
minimos = np.array([0.20, 0.50]) # Requerimientos mínimos
ingredientes = ["Maíz", "Soya"]

# 2. Definir el Problema (Minimización)
prob = pulp.LpProblem("Minimizar_Costos_Mezcla", pulp.LpMinimize)

# 3. Variables de Decisión (en Proporción de 0 a 1)
x = [pulp.LpVariable(ingredientes[i], lowBound=0, upBound=1) for i in range(len(ingredientes))]

# El total de la mezcla debe ser el 100% (1.0)
prob += pulp.lpSum(x) == 1.0

# 4. Función Objetivo
prob += pulp.lpSum([costos[i] * x[i] for i in range(len(costos))])

# 5. Restricciones Nutricionales
for i in range(len(minimos)):
    prob += pulp.lpSum([nutrientes[i, j] * x[j] for j in range(len(ingredientes))]) >= minimos[i]

# 6. Resolver
prob.solve(pulp.PULP_CBC_CMD(msg=0))

# 7. Extracción de resultados para graficar
valores_optimos = [v.varValue for v in x]
total_costo = pulp.value(prob.objective)

# 8. Visualización con Matplotlib
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Gráfico de Barras: Composición de la Mezcla
ax1.bar(ingredientes, valores_optimos, color=['gold', 'darkgreen'])
ax1.set_title("Composición Óptima del Saco")
ax1.set_ylabel("Proporción (0.0 a 1.0)")
ax1.set_ylim(0, 1)

# Gráfico de Pastel: Distribución de Costos
costos_por_ingrediente = [valores_optimos[i] * costos[i] for i in range(len(costos))]
ax2.pie(costos_por_ingrediente, labels=ingredientes, autopct='%1.1f%%', startangle=140, colors=['gold', 'darkgreen'])
ax2.set_title(f"Distribución del Costo Total (${total_costo:.2f})")

plt.tight_layout()
plt.show()

print(f"Mezcla óptima: {valores_optimos[0]*100:.1f}% Maíz y {valores_optimos[1]*100:.1f}% Soya.")
print(f"Costo mínimo por unidad: ${total_costo:.4f}")