import random as rand
import csv

def cargar_instancias():
    with open('Archivos/dataset2.csv') as file:
        datos = csv.reader(file, delimiter=',')
        instancias = [list(map(int, dato)) for dato in datos]

    return instancias

def dist_manhattan(instancias, vp):
    dist = list()
    for instancia in instancias:
        distancia = sum(abs(vp[x] - instancia[x]) for x in range(1, len(instancia)-1))
        dist.append([instancia[0], distancia])

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
    dataset = cargar_instancias()
    for split in splits:
        instancias = dataset
        num_instancias = len(instancias)
        rand.shuffle(instancias)
        inst_prueba = instancias[int(num_instancias*split):]
        inst_entrenamiento = instancias[:int(num_instancias*split)]

        resultados = list()
        matriz_confusion = [[0 for _ in range(2)] for _ in range(2)]

        for prueba in inst_prueba:
            DM = dist_manhattan(inst_entrenamiento, prueba)
            DM.sort(key=lambda x: x[1])
            clase = definir_clase(DM[:int(len(DM)*0.20)], inst_entrenamiento)
            resultados.append(clase)

        for i in range(len(inst_prueba)):
            if inst_prueba[i][-1] == resultados[i]:
                if inst_prueba[i][-1] == 1:
                    matriz_confusion[0][0] += 1
                else:
                    matriz_confusion[1][1] += 1
            else:
                if inst_prueba[i][-1] == 1:
                    matriz_confusion[0][1] += 1
                else:
                    matriz_confusion[1][0] += 1

        precision = (matriz_confusion[0][0] + matriz_confusion[1][1]) / len(resultados)
        print(precision)