import pandas as pd

# Créer un DataFrame a
a = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

# Créer une copie de a
b = a.copy()

# Modifier b
b['A'] = [7, 8, 9]

# Afficher a et b
print("DataFrame a:")
print(a)
print("\nDataFrame b:")
print(b)
