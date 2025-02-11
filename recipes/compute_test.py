# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

presidentielle_2022 = dataiku.Dataset("Presidentielle_2022")
presidentielle_2017 = dataiku.Dataset("Presidentielle_2017")
presidentielle_2012 = dataiku.Dataset("Presidentielle_2012")
presidentielle_2007 = dataiku.Dataset("Presidentielle_2007")
presidentielle_2002 = dataiku.Dataset("Presidentielle_2002")
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

    for index, (header, value) in enumerate(zip(headers, row)):
        if(header == "Blancs" or header == "Blancs et nuls"):
            final_df.loc[count, "Année"] = key
            final_df.loc[count, "Nom"] = "Blanc"
            final_df.loc[count, "Prénom"] = "Blanc"
            final_df.loc[count, "Voix"] = value
            count += 1
        
        
        if(headers.get_loc("Sexe") <= index):
            col_count += 1
            
        if(col_count == 1):
            final_df.loc[count, "Année"] = key
            final_df.loc[count, "Genre"] = value   
            
        if(col_count == 2):
            final_df.loc[count, "Nom"] = value
            
        if(col_count == 3):
            final_df.loc[count, "Prénom"] = value

        if(col_count == 4):
            final_df.loc[count, "Voix"] = value
         
        if(col_count == 6):
            col_count = 0
            count += 1
            
        

results = dataiku.Dataset("Presidentielle")
results.write_with_schema(final_df)
