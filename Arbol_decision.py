import csv
import math

def cargar_instancia(archivo):
    with open(archivo) as file:
        datos = csv.reader(file, delimiter=',')
        header = next(datos)
        instancias = [dato for dato in datos]

    return header, instancias

def entropia_shannon(nX, nY, n):
    entropia = -(nX/n) * math.log2(nX/n) - (nY/n) * math.log2(nY/n)
    return entropia

if __name__ == '__main__':
    splits = [0.70, 0.80, 0.90]
    header, dataset = cargar_instancia('./Archivos/dataset3.csv')
    num_instancias = len(dataset)
    inst_entrenamiento = dataset[:int(num_instancias * splits[0])]
    inst_prueba = dataset[int(num_instancias * splits[0]):]

    v1 = set()
    v2 = set()
    v3 = set()
    v4 = set()
    nX = 0 # cantidad de Si
    tabla = []

    for instancia in inst_entrenamiento:
        nX += 1 if instancia[-1] == 'Si' else 0
        v1.add(instancia[0])
        v2.add(instancia[1])
        v3.add(instancia[2])
        v4.add(instancia[3])
    entropiaArbol = entropia_shannon(nX, len(inst_entrenamiento) - nX, len(inst_entrenamiento))
    variables = [v1, v2, v3, v4]

    for i in range(len(variables)):
        ganancia = 0
        lista = list()
        for atributo in variables[i]:
            nSi = 0
            nNo= 0
            for instancia in inst_entrenamiento:
                if instancia[i] == atributo:
                    nSi += 1 if instancia[-1] == 'Si' else 0
                    nNo += 1 if instancia[-1] == 'No' else 0
            entropia = entropia_shannon(nSi, nNo, nSi+nNo)
            ganancia += (nSi + nNo) / len(inst_entrenamiento) * entropia
            print(atributo, nSi, nNo, nSi+nNo,entropia)
        print(ganancia)