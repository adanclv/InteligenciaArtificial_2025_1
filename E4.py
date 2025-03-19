import random as rand
import pandas as pd
import csv

def cargar_instancias():
    with open('Archivos/dataset1.csv') as file:
        datos = csv.reader(file, delimiter=',')
        header = next(datos)
        instancias = [list(map(int, dato)) for dato in datos]

    return header, instancias

def dist_manhattan(instancias, vp):
    dist = list()
    for instancia in instancias:
        distancia = sum(abs(vp[x] - instancia[x]) for x in range(1, len(instancia)-1))
        dist.append([instancia[0], distancia])

    return dist

def dist_euclidiana(instancias, vp):
    dist = list()
    for instancia in instancias:
        distancia = sum((vp[x] - instancia[x]) ** 2 for x in range(1, len(instancia)-1))
        dist.append([instancia[0], round(distancia ** 0.5, 2)])

    return dist

def dist_euclidiana_normalizada(instancias, vp):
    dist = list()
    for instancia in instancias:
        distancia = sum((vp[x]**2) - 2 * (vp[x] * instancia[x]) + instancia[x]**2 for x in range(1, len(instancia)-1))
        dist.append([instancia[0], distancia])

    return dist

def dist_coseno(instancias, vp):
    dist = list()
    for instancia in instancias:
        numerador = sum(vp[x] * instancia[x] for x in range(1, len(instancia)-1))
        denominador = sum(vp[x]**2 for x in range(1, len(instancia)-1))
        denominador *= sum(instancia[x]**2 for x in range(1, len(instancia)-1))
        distancia = numerador / denominador ** 0.5
        dist.append([instancia[0], round(distancia, 4)])

    return dist

def dist_jaccard(instancias, vp):
    dist = []
    for instancia in instancias:
        numerador = sum(vp[x] * instancia[x] for x in range(1, len(instancia)-1))  # Producto punto
        denominador = sum(vp[x] ** 2 for x in range(1, len(instancia)-1)) + sum(instancia[x] ** 2 for x in range(1, len(instancia)-1)) - numerador
        distancia = 1 - (numerador / denominador) if denominador != 0 else 1  # Convertir similitud a distancia
        dist.append([instancia[0], round(distancia, 4)])
    return dist


def dist_sorensen_dice(instancias, vp):
    dist = []
    for instancia in instancias:
        numerador = 2 * sum(vp[x] * instancia[x] for x in range(1, len(instancia)-1))
        denominador = sum(vp[x]**2 for x in range(1, len(instancia)-1)) + sum(instancia[x]**2 for x in range(1, len(instancia)-1))
        similitud = numerador / denominador if denominador != 0 else 0
        distancia = 1 - similitud  # Convertimos la similitud en distancia
        dist.append([instancia[0], round(distancia, 4)])
    return dist

def definir_clase(cercanos, inst_entrenamiento):
    response = list()
    for cercano in cercanos: # buscar los cercanos por su index en la lista de entrenamiento -> [index, valor]
        for i in range(len(inst_entrenamiento)):
            if inst_entrenamiento[i][0] == cercano[0]:
                response.append(inst_entrenamiento[i][-1])
                break

    # Moda
    moda = response.count(1)
    clase = 1 if moda > int(len(response) / 2) else 2
    return clase


if __name__ == '__main__':
    splits = [0.70, 0.80, 0.90]
    metricas = {
        'Manhattan': dist_manhattan,
        'Euclidiana': dist_euclidiana,
        'E. Normalizada': dist_euclidiana_normalizada,
        'Coseno': dist_coseno,
        'Jaccard': dist_jaccard,
        'Sorense': dist_sorensen_dice
    }
    header, dataset = cargar_instancias()
    num_instancias = len(dataset)

    resultados_dict = {key: [] for key in metricas}
    matrices_dict = {key: [] for key in metricas}
    for split in splits:
        instancias = dataset.copy()
        rand.shuffle(instancias)
        for key, fn in metricas.items():
            inst_entrenamiento = instancias[:int(num_instancias*split)]
            inst_prueba = instancias[int(num_instancias*split):]

            resultados = list()
            matriz_confusion = [[0, 0], [0, 0]]

            for prueba in inst_prueba:
                dist = fn(inst_entrenamiento, prueba)
                dist.sort(key=lambda x: int(x[1]))
                clase = definir_clase(dist[:int(len(dist)*0.20)], inst_entrenamiento)
                resultados.append([prueba[-1], clase])

            for real, predicho in resultados:
                i = 0 if real == 1 else 1
                j = 0 if predicho == 1 else 1
                matriz_confusion[i][j] += 1

            precision = (matriz_confusion[0][0] + matriz_confusion[1][1]) / sum(sum(row) for row in matriz_confusion)
            resultados_dict[key].append(round(precision, 4))
            matrices_dict[key].append(matriz_confusion)

    df = pd.DataFrame(resultados_dict, index=[f'{int(s * 100)}/{int(100 - (s * 100))}' for s in splits]).T
    df_matrices = pd.DataFrame(matrices_dict, index=[f'{int(s * 100)}/{int(100 - (s * 100))}' for s in splits]).T

    # Imprimir la tabla
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    pd.set_option('display.colheader_justify', 'center')
    print("\nPrecision")
    print(df)
    print("\nMatriz de confusion")
    print(df_matrices)