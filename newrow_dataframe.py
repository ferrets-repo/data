import pandas as pd

# Create a DataFrame
df = pd.DataFrame({
    'Name': [''],
    'Age': ['']
})

print(df)

# Create a dictionary with the data for the new row
new_row = {'Name': 'David', 'Age': 40}

# Inserting the new row
df.loc[len(df)] = new_row

# Reset the index
df = df.reset_index(drop=True)

print(df)