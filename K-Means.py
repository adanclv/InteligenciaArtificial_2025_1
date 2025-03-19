import csv
import random as rand

def cargar_instancias():
    with open('./Archivos/dataset1.csv') as file:
        datos = csv.reader(file, delimiter=',')
        header = next(datos)
        instancias = [list(map(int, dato)) for dato in datos]

    return header, instancias

def distancia_manhattan(punto1, punto2):
    return sum(abs(p1 - p2) for p1, p2 in zip(punto1, punto2))

def dist_euclidiana(punto1, punto2):
    return sum((p1 - p2) ** 2 for p1, p2 in zip(punto1, punto2)) ** 0.5

def get_clusters(distancias, clases):
    continuar = False
    new_clases = list()
    for i in range(len(distancias)):
        indice = distancias[i].index(min(distancias[i]))
        new_clases.append(indice)

        if new_clases[i] != clases[i]:
            continuar = True
    return new_clases, continuar

def asignar_clusters(instancias, centroides):
    etiquetas_cluster = list()
    for instancia in instancias:
        distancias = list()
        for centroide in centroides:
            distancias.append(distancia_manhattan(instancia, centroide))
        etiquetas_cluster.append(distancias.index(min(distancias)))
    return etiquetas_cluster

def update_centroides(instancias, etiquetas_cluster, k):
    new_centroides = [[0 for _ in range(len(instancias[0]))] for _ in range(k)]
    contador = [0 for _ in range(k)]
    for i in range(len(instancias)):
        cluster = etiquetas_cluster[i]
        contador[cluster] += 1
        for j in range(len(instancias[i])):
            new_centroides[cluster][j] += instancias[i][j]

    for i in range(k):
        if contador[i] > 0:
            for j in range(len(new_centroides[i])):
                new_centroides[i][j] = round(new_centroides[i][j] / contador[i], 2)
        else:
            new_centroides[i] = rand.choice(instancias)

    return new_centroides

if __name__ == '__main__':
    header, dataset = cargar_instancias()
    instancias = [data[1:-1] for data in dataset]
    k = int(input('K: '))

    centroides = [rand.choice(instancias) for _ in range(k)]
    etiquetas_cluster = [0 for _ in range(len(instancias))]

    continuar = True
    iteraciones = 0
    while continuar and iteraciones < 1000:
        new_etiquetas = asignar_clusters(instancias, centroides)
        continuar = new_etiquetas != etiquetas_cluster
        etiquetas_cluster = new_etiquetas
        centroides = update_centroides(instancias, etiquetas_cluster, k)
        iteraciones += 1
        print(centroides)

    print('Iteraciones:', iteraciones)