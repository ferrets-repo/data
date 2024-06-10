import pandas as pd

df = pd.DataFrame({'score': ['A', 'B', 'C']})

df['score'].replace({'A': 1, 'B': 2, 'C': 3}, inplace=True)

print(df)