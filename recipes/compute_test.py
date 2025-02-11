# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
presidentielle_2022 = dataiku.Dataset("MSPR__1__Presidentielle_2022")
presidentielle_2017 = dataiku.Dataset("MSPR__1__Presidentielle_2017")
presidentielle_2012 = dataiku.Dataset("MSPR__1__Presidentielle_2012")
presidentielle_2007 = dataiku.Dataset("MSPR__1__Presidentielle_2007")
presidentielle_2002 = dataiku.Dataset("MSPR__1__Presidentielle_2002")
presidentielle_1995 = dataiku.Dataset("MSPR__1__Presidentielle_1995")

dfs = {
    "2022" : presidentielle_2022.get_dataframe(),
    "2017" : presidentielle_2017.get_dataframe(),
    "2012" : presidentielle_2012.get_dataframe(),
    "2007" : presidentielle_2007.get_dataframe(),
    "2002" : presidentielle_2002.get_dataframe(),
    "1995" : presidentielle_1995.get_dataframe()
}

final_df = pd.DataFrame(columns=["year"])

for key, df in dfs.items():
    headers = df.columns 
    row = df.iloc[0]

    for header, value in zip(headers, row):
        print(f"{key}")
        print(f"Colonne: {header}, Valeur: {value}")

        # Exemple de test conditionnel
        if "Nom" in header:
            print(f"Nom détecté: {value}")
        elif "Score" in header:
            print(f"Score détecté: {value}")
        else:
            print(f"Autre valeur: {value}")


# Compute recipe outputs from inputs
# TODO: Replace this part by your actual code that computes the output, as a Pandas dataframe
# NB: DSS also supports other kinds of APIs for reading and writing data. Please see doc.

# Extraire la première ligne comme en-têtes et la deuxième ligne comme valeurs



# Write recipe outputs
test = dataiku.Dataset("test")
test.write_with_schema(final_df)
