import pandas as pd

EXCEL_FILE = "bd.xlsx"

# Charger les données Excel
def load_data():
    return pd.read_excel(EXCEL_FILE, engine="openpyxl")

# Sauvegarder les modifications dans le fichier Excel
def save_data(df):
    df.to_excel(EXCEL_FILE, index=False, engine="openpyxl")

# Filtrer les données selon une colonne et une valeur donnée
def filter_data(df, column, value):
    return df[df[column] == value]

# Mettre à jour les valeurs manquantes ou modifiées
def update_values(df, updates, filter_column, filter_value):
    for col, val in updates.items():
        df.loc[df[filter_column] == filter_value, col] = val
    return df
