# -*- coding: utf-8 -*-
import dataiku
import pandas as pd
import numpy as np
from dataiku import pandasutils as pdu
from utils import columns_to_int

party_orientation = {
    'EXG': 'Left', 'COM': 'Left', 'FG': 'Left', 'SOC': 'Left', 'RDG': 'Left',
    'DVG': 'Left', 'VEC': 'Left', 'ECO': 'Left', 'FI': 'Left', 'NUP': 'Left',
    'UG': 'Left', 'DXG': 'Left', 'PRS': 'Left', 'GEC': 'Left', 'LO': 'Left',
    'LCR': 'Left', 'PRG': 'Left',

    'CEN': 'Right', 'MDM': 'Right', 'UDI': 'Right', 'DVC': 'Right', 'UDFD': 'Right',
    'REM': 'Right', 'ENS': 'Right', 'ALLI': 'Right', 'UDF': 'Right',

    'UMP': 'Right', 'RPR': 'Right', 'LR': 'Right', 'DVD': 'Right', 'DIV': 'Right',
    'MAJ': 'Right', 'PRV': 'Right', 'NCE': 'Right', 'DL': 'Right',

    'FN': 'Far_Right', 'RN': 'Far_Right', 'FRN': 'Far_Right', 'MNR': 'Far_Right',
    'EXD': 'Far_Right', 'DLF': 'Far_Right', 'DSV': 'Far_Right', 'REC': 'Far_Right',
    'MPF': 'Far_Right', 'RPF': 'Far_Right',

    'REG': 'Right', 'CPNT': 'Right', 'AUT': 'Right', 'PREP': 'Right',

    'Blanc': 'Blank'
}

# Charger les datasets
datasets = {
    "2024": dataiku.Dataset("Legislative_2024"),
    "2022": dataiku.Dataset("Legislative_2022"),
    "2017": dataiku.Dataset("Legislative_2017"),
    "2012": dataiku.Dataset("Legislative_2012"),
    "2007": dataiku.Dataset("Legislative_2007"),
    "2002": dataiku.Dataset("Legislative_2002"),
    "1997": dataiku.Dataset("Legislative_1997"),
    "1993": dataiku.Dataset("Legislative_1993"),
}

dfs = {
    "2024": {"first_party_col_name": "Nuance candidat 1", "votes_col_nb": 2, "cycle_length": 4},
    "2022": {"first_party_col_name": "Code Nuance", "votes_col_nb": 2, "cycle_length": 5},
    "2017": {"first_party_col_name": "Code Nuance", "votes_col_nb": 2, "cycle_length": 5},
    "2012": {"first_party_col_name": "Code Nuance", "votes_col_nb": 3, "cycle_length": 5},
    "2007": {"first_party_col_name": "Code Nuance", "votes_col_nb": 3, "cycle_length": 5},
    "2002": {"first_party_col_name": "Code Nuance", "votes_col_nb": 3, "cycle_length": 5},
    "1997": {"first_party_col_name": "Code Nuance", "votes_col_nb": 3, "cycle_length": 5},
    "1993": {"first_party_col_name": "Code Nuance", "votes_col_nb": 3, "cycle_length": 3},
}

# Ajouter les DataFrames
for year in dfs:
    dfs[year]["df"] = datasets[year].get_dataframe()

# Création du DataFrame final
final_df = pd.DataFrame(columns=["année", "parti", "voix", "couleur"])
count = 0

for year, data in dfs.items():
    df = data["df"]
    headers = df.columns
    row = df.iloc[0]
    col_count = 0

    for index, (header, value) in enumerate(zip(headers, row)):
        if header in ["Blancs", "Nuls", "Blancs et nuls"]:
            final_df.loc[count, "année"] = year
            final_df.loc[count, "parti"] = "Blanc"
            if pd.isna(final_df.at[count, "voix"]):
                final_df.loc[count, "voix"] = value
            else:
                final_df.loc[count, "voix"] += value
            if header in ["Nuls", "Blancs et nuls"]:
                count += 1

        if headers.get_loc(data["first_party_col_name"]) <= index:
            col_count += 1

        if col_count == 1:
            final_df.loc[count, "année"] = year
            final_df.loc[count, "parti"] = value

        if col_count == data["votes_col_nb"]:
            final_df.loc[count, "voix"] = value

        if col_count == data["cycle_length"]:
            col_count = 0
            count += 1

# Ajout de la colonne couleur
final_df['couleur'] = final_df['parti'].map(party_orientation)

# Conversion des colonnes numériques
final_df = columns_to_int(final_df, ["année", "voix"])

# Sauvegarde dans le dataset "Legislatives"
output_dataset = dataiku.Dataset("Legislatives")
output_dataset.write_with_schema(final_df)
