
#INGRESA LOS DATOS DE LA FUNCION OBJETIVO Y RESTRICCIONES
def Input_Restricciones():
    restricciones = []
    max_min = int(input("Desea o maximizar o minimizar esta funcion (1 = Min ; 2 = Max)"))
    print("Ingrese los coeficientes de la funcion objetivo de tipo: (Z = ax + by + c):")
    a = float(input("Ingrese coeficiente a de funcion objetivo: "))
    b = float(input("Ingrese coeficiente b de funcion objetivo: "))
    c = 0
    func_objetivo = [a,b,c, max_min]
    num_rest = int(input("Cuantas Restricciones?"))
    for x in range(0, num_rest):
        print("Ingrese los coeficientes de la restricción de tipo: (ax + by <= c o ax + by >= c):")
        x = float(input("Ingrese el coeficiente 'a': "))
        y = float(input("Ingrese el coeficiente 'b': "))
        c = float(input("Ingrese el término independiente 'c': "))
        ask = int(input("Tipo de restriccion (1. <= ; 2. >= ; 3. =)"))
        restricciones.append([x,y,c,ask])
    return Create_Tabla(restricciones), func_objetivo


#CREA LA TABLA CON LAS RESTRICCIONES
def Create_Tabla(restricciones):
    index_Artificiales = []
    index_holguras = []
    holguras = 0
    excesos = 0
    artificiales = 0
    is_porFases = False
    for x, y, c, ask in restricciones:
        if ask == 1:
            holguras += 1
            tabla[0].insert(len(tabla[0]) - 1, f"h{holguras}") #Crea columna hx en fila 0
            index = (len(tabla[0]) - 1)
            index_holguras.append(index - 1) #Guarda el indice de la columna de holguras
            for z in range(1, len(tabla)):
                tabla[z].insert(index, 0) #Rellena con 0 hacia toda la columna hx
            tabla.append([0,x,y]) #Crea nueva fila de la restriccion
            for z in range(3,len(tabla[0])): 
                if z == index-1:
                    tabla[len(tabla)-1].append(1) #Agrega 1 si la columna es hx
                else:
                    tabla[len(tabla)-1].append(0) #Agrega 0 en todo lo demas
        elif ask == 2:
            is_porFases = True
            excesos += 1
            artificiales += 1
            tabla[0].insert(len(tabla[0]) - 1, f"e{excesos}")
            index_e = (len(tabla[0]) - 1)
            tabla[0].insert(len(tabla[0]) - 1, f"a{artificiales}")
            tabla[1].insert(len(tabla[1]) - 1, 0)
            tabla[1].insert(len(tabla[1]) - 1, -1)
            index_Artificiales.append(index_e) #Guarda el indice de la columna de artificiales

            for z in range(2, len(tabla)):
                tabla[z].insert(index_e, 0)
                tabla[z].insert(index_e+1, 0)
            tabla.append([0,x,y])
            for z in range(3,len(tabla[0])):
                if z == index_e-1:
                    tabla[len(tabla)-1].append(-1)
                    tabla[len(tabla)-1].append(1)
                elif z == index_e:
                    pass
                else:
                    tabla[len(tabla)-1].append(0)

        elif ask == 3:
            is_porFases = True
            artificiales += 1
            tabla[0].insert(len(tabla[0]) - 1, f"a{artificiales}")
            index = (len(tabla[0]) - 1)
            tabla[1].insert(len(tabla[1]) - 1, -1)
            index_Artificiales.append(index-1)

            for z in range(2, len(tabla)):
                tabla[z].insert(index, 0)
            tabla.append([0,x,y])
            for z in range(3,len(tabla[0])):
                if z == index-1:
                    tabla[len(tabla)-1].append(1)
                else:
                    tabla[len(tabla)-1].append(0)

    num_restr = 1
    for x, y, c, ask in restricciones:
        num_restr += 1
        tabla[num_restr][-1] = c

    return is_porFases, index_Artificiales, index_holguras

#ELIMINA LAS COLUMNAS DE LAS VARIABLES ARTIFICIALES
def eliminar_columna(tabla):
    for y in range(len(index_artificiales) - 1, -1, -1):
        for i in range(len(tabla)):
            tabla[i].pop(index_artificiales[y])


#FASE 1 DEL SIMPLEX
def Fase1(tabla, index_artificiales):
    func_objetivo[3] = 1
    index_filas= []
    for y in index_artificiales:
        for x in range(2, len(tabla)):
            if tabla[x][y] == 1:
                index_filas.append(x)
                break
    for x in index_filas:
        for y in range(1, len(tabla[0])):
            tabla[1][y] = tabla[1][y] + tabla[x][y]

#FASE 2 DEL SIMPLEX        
#FASE 2 DEL SIMPLEX        
def Fase2(tabla, solucion):
    filas_solucion = []
    columnas_solucion = []
    
    filax1 = None  # Inicializa estas variables para evitar errores
    filax2 = None
    
    # Recorre la lista de soluciones para encontrar las filas de las variables básicas
    for i in range(len(solucion)):
        if tabla[solucion[i]][1] ==1:  # Condición para identificar x1
            filax1 = solucion[i]  # Asigna la fila correspondiente a x1
            columnas_solucion.append(1)
            filas_solucion.append(filax1)
        elif tabla[solucion[i]][2] == 1:  # Condición para identificar x2
            filax2 = solucion[i]  # Asigna la fila correspondiente a x2
            columnas_solucion.append(2)
            filas_solucion.append(filax2)

    # Asegúrate de que las variables filax1 y filax2 estén definidas antes de usarlas
    if filax1 is not None:
        x1 = tabla[1][1]
        while x1 != 0:
            for i in range(len(tabla[filax1])):
                tabla[1][i] -= x1 * tabla[filax1][i]
            x1 = 0
    
    if filax2 is not None:
        x2 = tabla[1][2]
        while x2 != 0:
            for i in range(len(tabla[filax2])):
                tabla[1][i] -= x2 * tabla[filax2][i]
            x2 = 0

    # Verifica si el objetivo es maximizar o minimizar
    if flag:
        func_objetivo[3] = 2

    return filas_solucion, columnas_solucion



#BUSCA LA COLUMNA PIVOT EN CASO DE MAXIMIZAR O MINIMIZAR
def buscar_columna_pivot(tabla, max_min):
    num_columnas = len(tabla[0])-1
    columna_pivot = -1
    if max_min == 1:
        min_valor = float('-inf')
        for i in range(1, num_columnas):
            if tabla[1][i] > min_valor:
                min_valor = tabla[1][i]
                columna_pivot = i
    elif max_min == 2:
        max_valor = float('inf')
        for i in range(1, num_columnas):
            if tabla[1][i] < max_valor:
                max_valor = tabla[1][i]
                columna_pivot = i
    return columna_pivot

#BUSCA LA FILA PIVOT PARA TOD0 CASO
def buscar_fila_pivot(tabla, columna_pivot):
    num_filas = len(tabla)
    min_valor = float('inf')
    fila_pivot = -1
    for i in range(2, num_filas):
        if tabla[i][columna_pivot] > 0:
            if tabla[i][len(tabla[0])-1] / tabla[i][columna_pivot] < min_valor:
                min_valor = tabla[i][len(tabla[0])-1] / tabla[i][columna_pivot]
                fila_pivot = i
    return fila_pivot


#REALIZA EL PIVOTEO EN LA TABLA
def Pivotear(tabla, fila_pivot, columna_pivot):
    valor_pivot = tabla[fila_pivot][columna_pivot]
    num_columnas = len(tabla[0])

    for i in range(num_columnas):
        tabla[fila_pivot][i] /= valor_pivot
        
    for i in range(1, len(tabla)):
        if i != fila_pivot:
            factor = tabla[i][columna_pivot]
            tabla[i] = [x - factor * tabla[fila_pivot][j] for j, x in enumerate(tabla[i])]
            for p in range(0,len(tabla[i])):
                if abs(tabla[i][p]) < 2e-7:
                    tabla[i][p] = 0.0


#REEMPLAZA LA FUNCION OBJETIVO EN LA TABLA
def Remplazar_objetivo(tabla):
    tabla[1][1] = func_objetivo[0]*-1
    tabla[1][2] = func_objetivo[1]*-1
    tabla[1][-1] = func_objetivo[2]


#FUNCION PRINCIPAL DEL SIMPLEX
def Simplex(tabla):
    filas=[]
    columnas = []
    while min(tabla[1][1:-1]) < 0 and func_objetivo[3] == 2 or max(tabla[1][1:-1]) > 0 and func_objetivo[3] == 1:
        columna_pivot = buscar_columna_pivot(tabla, func_objetivo[3])
        fila_pivot = buscar_fila_pivot(tabla, columna_pivot)
        Pivotear(tabla, fila_pivot, columna_pivot)
        filas.append(fila_pivot)
        columnas.append(columna_pivot)

    if func_objetivo[3] == 1:
        if tabla[1][-1] != 0:
            print("No es factible")
            return

    return filas, columnas


#MUESTRA EL RESULTADO FINAL
def MostrarFinal():
    print(20*"-")
    print("Valor óptimo:", round(tabla[1][-1], 2))
    print(f"x1: {x1}")
    print(f"x2: {x2}")
    print(20*"-")
    precio_sombra()
    print(20*"-")
    print("La matriz es la siguiente:")
    for fila in tabla:
        for valor in fila:
            if valor != str(valor):
                print("\t", round(valor, 4), end=" ")
            else:
                print("\t", valor, end=" ")      
        print()

#MUESTRA LA MATRIZ
def Mostrar():
    print("La matriz es la siguiente:")
    for fila in tabla:
        for valor in fila:
            print("\t", valor, end=" ")
        print()

#BUSCA LOS UNOS EN LA TABLA
def buscar_unos(tabla):
    x1 = None
    x2 = None
    for i in range(2, len(tabla)):
        if tabla[i][1] == 1:
            x1 = tabla[i][-1]
        if tabla[i][2] == 1:
            x2 = tabla[i][-1]
            
    return x1, x2

#PRECIO SOMBRA
def precio_sombra():
    h_mayor = float('-inf')
    for i in range(len(tabla[0])):
        if tabla[0][i].startswith("h"):
            if tabla[1][i] > h_mayor:
                h_mayor = tabla[1][i]

    if h_mayor != float('-inf'):
        index_hmayor= tabla[1].index(h_mayor)
        print(f"Precio sombra de la holgura {tabla[0][index_hmayor]}:", h_mayor)
    else:
        print("No hay variables de holgura")

flag = False
tabla =[ ["z", "x1", "x2", "LD"],
        [  0,    0,    0,    0]]

(is_PorFases, index_artificiales, index_holguras), func_objetivo = Input_Restricciones()
Mostrar()

if func_objetivo[3] == 2:
    flag = True

if is_PorFases: #Maximizacion y minimización dos fases
    Fase1(tabla, index_artificiales)
    filas, columnas = Simplex(tabla)
    eliminar_columna(tabla)
    Remplazar_objetivo(tabla)
    Fase2(tabla, filas)
    if func_objetivo[3] == 2:
        Simplex(tabla)
    
else:
    Remplazar_objetivo(tabla) #Maximizacion
    filas, columnas = Simplex(tabla)

x1, x2 = buscar_unos(tabla)

MostrarFinal()


###################################################################