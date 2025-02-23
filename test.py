import pandas as pd
import numpy as np

df = pd.DataFrame(columns=['url', 'date', 'main_card', 'prelims'])
print(pd.DataFrame(data={'url': [1], 'date': [2], 'main_card': [3], 'prelims': [4]}))

# df.set_index(keys='name', inplace=True)
df = pd.concat([df, pd.DataFrame(data={'url': [1], 'date': [2], 'main_card': [3], 'prelims': [4]}, index=['first'])], axis=0)
print(df)
for i in df.values:
    print(i)