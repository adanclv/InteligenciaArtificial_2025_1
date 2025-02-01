import random as rand

def mayor_a_menor(a):
    v = list()
    for i in range(len(a) -1, -1, -1):
        v.append(a[i])

    return v


if __name__ == '__main__':
    # Vector de 10 digitos enteros
    vector = [rand.randint(1, 100) for _ in range(10)]
    print(vector)

    vector.sort()
    v1 = mayor_a_menor(vector[5:])
    v2 = list()
    temp = 0

    for e in vector[:5]:
        v2.append(e + temp)
        temp = e

    print("v1 = ", v1)
    print("v2 = ", v2)


