import random as rand
import pandas as pd

values = list()

for i in range(1000):
    values.append([i+1] + [rand.randint(0, 10) for i in range(7)] + [rand.randint(1, 2)])


df_completo = pd.DataFrame(values)
df_completo.to_csv('./Archivos/dataset1.csv', index=False, header=False)
