import pandas as pd
from datetime import datetime as dt

# Carga del archivo en dataframe
caudales = pd.read_csv("/home/rojolot/Downloads/Estacion_16/Estacion_16.csv", encoding='latin1', delimiter=';')

# Carga del dataframe en array
caudales_matriz = caudales.to_numpy()

# Vista de datos en cadena de caracteres y formato original
print(f"Fecha y hora: {caudales_matriz[0, 0]}")
print(f"Caudal: {caudales_matriz[0, 1]}")

formato_fecha = "%d/%m/%Y"

n = caudales_matriz.shape[0]

for i in range(n):
    # Conversión para fecha y hora
    fecha_y_hora = caudales_matriz[i, 0]
    fecha = fecha_y_hora[0:10]
    caudales_matriz[i, 0] = dt.strptime(fecha, formato_fecha).date()
    print(caudales_matriz[i, 0])

    # Conversión para coma decimal en punto decimal
    caudal_medio_mensual = caudales_matriz[i, 1].replace(",", ".")
    caudales_matriz[i, 1] = float(caudal_medio_mensual)
    print(caudales_matriz[i, 1])