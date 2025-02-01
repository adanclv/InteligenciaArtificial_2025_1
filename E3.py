import pandas as pd
import random as rand
import csv


def cargar_instancias():
    with open('Archivos/dataset2.csv') as file:
        datos = csv.reader(file, delimiter=',')
        instancias = [list(map(int, dato)) for dato in datos]

    return instancias

def distancia_manhattan(soluciones, vp):
    dist = list()
    for solucion in soluciones:
        distancia = sum(abs(vp[x] - solucion[x]) for x in range(len(solucion)))
        dist.append(distancia)

    return dist

def distancia_euclidiana(soluciones, vp):
    dist = list()
    for solucion in soluciones:
        distancia = sum((vp[x] - solucion[x]) ** 2 for x in range(len(solucion)))
        dist.append(round(distancia ** 0.5, 2))

    return dist

def dist_euclidiana_normalizada(soluciones, vp):
    dist = list()
    for solucion in soluciones:
        distancia = sum((vp[x]**2)-2 * (vp[x] * solucion[x]) + solucion[x]**2 for x in range(len(solucion)))
        dist.append(distancia)

    return dist

def dist_coseno(soluciones, vp):
    dist = list()
    for solucion in soluciones:
        numerador = sum(vp[x] * solucion[x] for x in range(len(solucion)))
        denominador = sum(vp[x]**2 for x in range(len(solucion)))
        denominador *= sum(solucion[x]**2 for x in range(len(solucion)))
        distancia = numerador / denominador ** 0.5
        dist.append(round(distancia, 4))

    return dist

def dist_jaccard(soluciones, vp):
    dist = list()
    n = len(soluciones[0])
    for solucion in soluciones:
        numerador = sum(vp[x] * solucion[x] for x in range(n))
        denominador = sum(vp[x] ** 2 for x in range(n))
        denominador += sum(solucion[x] ** 2 for x in range(n))
        denominador -= sum(vp[x] * solucion[x] for x in range(n))
        distancia = numerador / denominador
        dist.append(round(distancia, 4))

    return dist

def dist_sovence(soluciones, vp):
    pass


if __name__ == '__main__':
    dataset = cargar_instancias()
    instancias = [data[1:-1] for data in dataset]
    vp = [1, 0, 9, 2, 4, 9, 4, 1]
    # vp = [rand.randint(1, 10) for _ in range(7)] + [rand.randint(1, 2)]

    DM = pd.DataFrame(distancia_manhattan(instancias, vp[:-1]))
    DE = pd.DataFrame(distancia_euclidiana(instancias, vp[:-1]))
    DEN = pd.DataFrame(dist_euclidiana_normalizada(instancias, vp[:-1]))
    DC = pd.DataFrame(dist_coseno(instancias, vp[:-1]))
    DJ = pd.DataFrame(dist_jaccard(instancias, vp[:-1]))
    instancias = pd.DataFrame(instancias)

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    pd.set_option('display.colheader_justify', 'center')
    df = pd.DataFrame()
    df = pd.concat([instancias, DM, DE, DEN, DC, DJ], axis=1, ignore_index=True)
    df.columns = ['v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'Manhattan', 'Euclidiana', 'Euclidiana Norm', 'Coseno', 'Jaccard']
    print(df)