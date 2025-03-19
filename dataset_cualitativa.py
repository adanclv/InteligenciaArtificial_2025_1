'''
Servicio entrega a domicilio:
Puntualidad: Excelente, Buena, Regular, Mala.
Estado del Producto: Perfecto, Bueno, Dañado.
Servicio al Cliente: Excelente, Muy Bueno, Bueno, Regular, Malo.
Precio: Alto, Medio, Bajo.
'''

import pandas as pd

def puntualidad(valor):
    if valor == 10:
        return 'Excelente'
    elif valor >= 8:
        return 'Regular'
    elif valor >= 6:
        return 'Buena'
    return 'Mala'

def servicio_cliente(valor):
    if valor == 10:
        return 'Excelente'
    elif valor >= 8:
        return 'Muy Bueno'
    elif valor >= 6:
        return 'Bueno'
    elif valor >= 4:
        return 'Regular'
    return 'Malo'

def estado_producto(valor):
    if valor >= 8:
        return 'Perfecto'
    elif valor >= 4:
        return 'Bueno'
    return 'Defectuoso'

def precio(valor):
    if valor >= 8:
        return 'Alto'
    elif valor >= 5:
        return 'Medio'
    return 'Bajo'

if __name__ == '__main__':
    df = pd.read_csv('./Archivos/dataset1.csv')

    df['v1'] = df['v1'].apply(lambda x: puntualidad(x))
    df['v2'] = df['v2'].apply(lambda x: estado_producto(x))
    df['v3'] = df['v3'].apply(lambda x: servicio_cliente(x))
    df['v4'] = df['v4'].apply(lambda x: precio(x))
    df['respuesta'] = df['respuesta'].apply(lambda x: 'Si' if x == 1 else 'No')
    df.drop(columns=['id', 'v5', 'v6', 'v7'], inplace=True)
    df.columns = ['Puntualidad', 'Estado del Producto', 'Servicio al Cliente', 'Precio', 'Respuesta']

    # Guardar el DataFrame modificado en un nuevo archivo CSV
    df.to_csv('./Archivos/dataset3.csv', index=False)
    print(df)