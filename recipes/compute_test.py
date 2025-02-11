# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
# Dataset MSPR__1__Presidentielle_2022 renamed to Presidentielle_2022 by admin on 2025-02-11 15:20:49
presidentielle_2022 = dataiku.Dataset("Presidentielle_2022")
presidentielle_2017 = dataiku.Dataset("MSPR__1__Presidentielle_2017")
presidentielle_2012 = dataiku.Dataset("MSPR__1__Presidentielle_2012")
presidentielle_2007 = dataiku.Dataset("MSPR__1__Presidentielle_2007")
# Dataset MSPR__1__Presidentielle_2002 renamed to Presidentielle_2002 by admin on 2025-02-11 15:21:03
presidentielle_2002 = dataiku.Dataset("Presidentielle_2002")
# Dataset MSPR__1__Presidentielle_1995 renamed to Presidentielle_1995 by admin on 2025-02-11 15:20:56
presidentielle_1995 = dataiku.Dataset("Presidentielle_1995")

dfs = {
    "2022" : presidentielle_2022.get_dataframe(),
    "2017" : presidentielle_2017.get_dataframe(),
    "2012" : presidentielle_2012.get_dataframe(),
    "2007" : presidentielle_2007.get_dataframe(),
    "2002" : presidentielle_2002.get_dataframe(),
    "1995" : presidentielle_1995.get_dataframe()
}


final_df = pd.DataFrame(columns=["Année", "Genre", "Nom", "Prénom", "Voix"])
count = 0

for key, df in dfs.items():
    headers = df.columns 
    row = df.iloc[0]
    col_count = 0
    started = False

    for header, value in zip(headers, row):
        if(header == "Blancs" or header == "Blancs et nuls"):
            final_df.loc[count, "Année"] = key
            final_df.loc[count, "Nom"] = "Blanc"
            final_df.loc[count, "Prénom"] = "Blanc"
            final_df.loc[count, "Voix"] = value
            count += 1
        
        
        if(col_count > 0):
            col_count += 1
            
        if(header == "Sexe" or started and col_count == 0):
            final_df.loc[count, "Année"] = key
            final_df.loc[count, "Genre"] = value   
            col_count = 1
            started = True
            
        if(col_count == 2):
            final_df.loc[count, "Nom"] = value
            
        if(col_count == 3):
            final_df.loc[count, "Prénom"] = value

        if(col_count == 4):
            final_df.loc[count, "Voix"] = value
         
        if(col_count == 6):
            col_count = 0
            count += 1
            
        

# Write recipe outputs
test = dataiku.Dataset("test")
test.write_with_schema(final_df)
