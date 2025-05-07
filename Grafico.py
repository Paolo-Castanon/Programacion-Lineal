import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull

def determinante(x1, y1, x2, y2):
    return (x1 * y2) - (y1 * x2)

def input_recta():
    X, Y, C = [], [], []
    while True:
        try:
            x = float(input("Coeficiente de X: "))
            y = float(input("Coeficiente de Y: "))
            c = float(input("Constante: "))
            ask = input("Es <=? (si/no): ").strip().lower()
            if ask == "no":
                x, y, c = -x, -y, -c
            X.append(x)
            Y.append(y)
            C.append(c)
        except ValueError:
            print("Entrada inválida. Inténtelo de nuevo.")
        cont = input("¿Agregar otra restricción? (si/no): ").strip().lower()
        if cont == "no":
            break

    return X, Y, C

def calcular_intersecciones(X, Y, C):
    intersecciones = []
    n = len(X)
    for i in range(n):
        for j in range(i+1, n):
            det = determinante(X[i], Y[i], X[j], Y[j])
            if det != 0:  # Verifica que no sean paralelas
                x_inter = determinante(C[i], Y[i], C[j], Y[j]) / det
                y_inter = determinante(X[i], C[i], X[j], C[j]) / det
                intersecciones.append((x_inter, y_inter))
    return intersecciones

def filtrar_puntos_factibles(intersecciones, X, Y, C):
    puntos_factibles = []
    for x, y in intersecciones:
        factible = all(X[i] * x + Y[i] * y <= C[i] for i in range(len(X)))
        if factible:
            puntos_factibles.append((x, y))
    return puntos_factibles

def funcion_objetivo(puntos_factibles):
    coef_x = float(input("Coeficiente de X en la función objetivo: "))
    coef_y = float(input("Coeficiente de Y en la función objetivo: "))
    MaxMin = int(input("¿Desea minimizar (1) o maximizar (2)? "))
    
    if MaxMin not in [1, 2]:
        print("Entrada inválida. Debe ingresar 1 o 2.")
        return
    
    valores = [(x, y, coef_x*x + coef_y*y) for x, y in puntos_factibles]
    
    if MaxMin == 1:
        mejor_punto = min(valores, key=lambda p: p[2])
        print(f"Mínimo en: {mejor_punto[:2]} con valor {mejor_punto[2]}")
    else:
        mejor_punto = max(valores, key=lambda p: p[2])
        print(f"Máximo en: {mejor_punto[:2]} con valor {mejor_punto[2]}")
    return (mejor_punto[:2], coef_x, coef_y, mejor_punto[2])

def graficar_restricciones(X, Y, C, puntos_factibles, res):
    plt.figure()
    x_vals = np.linspace(-1000, 1000, 400)
    
    for i in range(len(X)):
        if Y[i] != 0:
            y_vals = (C[i] - X[i] * x_vals) / Y[i]
            plt.plot(x_vals, y_vals, label=f'{X[i]}x + {Y[i]}y <= {C[i]}')
        else:
            plt.axvline(x=C[i]/X[i], label=f'{X[i]}x <= {C[i]}')
    
    if puntos_factibles:     
        puntos = np.array(puntos_factibles)
        if len(puntos) >= 3:
            hull = ConvexHull(puntos)
            for simplex in hull.simplices:
                plt.plot(puntos[simplex, 0], puntos[simplex, 1], 'k-')
            plt.fill(puntos[hull.vertices,0], puntos[hull.vertices,1], 'red', alpha=0.5, label="Zona Factible")
        
        # Puntos factibles
        x_pf, y_pf = zip(*puntos_factibles)
        plt.scatter(x_pf, y_pf, color='red', zorder=3, label="Puntos Factibles")
    
    plt.plot(x_vals, ((res[3] - res[1] * x_vals) / res[2]), label=f'{res[1]}x + {res[2]}y = {res[3]}', linestyle='--')

    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.legend()
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.show()

# Flujo principal del programa
X, Y, C = input_recta()
intersecciones = calcular_intersecciones(X, Y, C)
puntos_factibles = filtrar_puntos_factibles(intersecciones, X, Y, C)
resultado = funcion_objetivo(puntos_factibles)
graficar_restricciones(X, Y, C, puntos_factibles, resultado)