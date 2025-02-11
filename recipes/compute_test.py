# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
MSPR__1__Presidentielle_2022 = dataiku.Dataset("MSPR__1__Presidentielle_2022")
MSPR__1__Presidentielle_2022_df = MSPR__1__Presidentielle_2022.get_dataframe()


# Compute recipe outputs from inputs
# TODO: Replace this part by your actual code that computes the output, as a Pandas dataframe
# NB: DSS also supports other kinds of APIs for reading and writing data. Please see doc.

# Extraire la première ligne comme en-têtes et la deuxième ligne comme valeurs
headers = df.columns  # Noms des colonnes
second_row = df.iloc[1]  # Deuxième ligne

# Itération sur chaque colonne de la deuxième ligne
for header, value in zip(headers, second_row):
    print(f"Colonne: {header}, Valeur: {value}")
    
    # Exemple de test conditionnel
    if "Nom" in header:
        print(f"Nom détecté: {value}")
    elif "Score" in header:
        print(f"Score détecté: {value}")
    else:
        print(f"Autre valeur: {value}")

test_df = MSPR__1__Presidentielle_2022_df # For this sample code, simply copy input to output


# Write recipe outputs
test = dataiku.Dataset("test")
test.write_with_schema(test_df)
