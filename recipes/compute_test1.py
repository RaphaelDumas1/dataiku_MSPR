# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

legislative_2024 = dataiku.Dataset("Legislative_2024")
legislative_2022 = dataiku.Dataset("Legislative_2022")
legislative_2017 = dataiku.Dataset("Legislative_2017")
legislative_2012 = dataiku.Dataset("Legislative_2012")
legislative_2007 = dataiku.Dataset("Legislative_2007")
legislative_2002 = dataiku.Dataset("Legislative_2002")
legislative_1997 = dataiku.Dataset("Legislative_1997")
legislative_1993 = dataiku.Dataset("Legislative_1993")



dfs = {
    "2024" : legislative_2024.get_dataframe(),
    "2022" : legislative_2022.get_dataframe(),
    "2017" : legislative_2017.get_dataframe(),
    "2012" : legislative_2012.get_dataframe(),
    "2007" : legislative_2007.get_dataframe(),
    "2002" : legislative_2002.get_dataframe(),
    "1997" : legislative_1997.get_dataframe(),
    "1993" : legislative_1993.get_dataframe(),
}


final_df = pd.DataFrame(columns=["Année", "Partis", "Voix"])
count = 0

for key, df in dfs.items():
    headers = df.columns 
    row = df.iloc[0]
    col_count = 0
    started = False

    for header, value in zip(headers, row):
        if(header == "Blancs" or header == "Nuls"):
            final_df.loc[count, "Année"] = key
            final_df.loc[count, "Partis"] = "Blanc"
            final_df.loc[count, "Voix"] += value
            count += 1
            
        if(header == "Blancs et nuls"):
            final_df.loc[count, "Année"] = key
            final_df.loc[count, "Partis"] = "Blanc"
            final_df.loc[count, "Voix"] = value
            count += 1
            
        
        if(col_count > 0):
            col_count += 1
            
        if(header == "Nuance candidat 1" or header == "Code Nuance" or started and col_count == 0):
            final_df.loc[count, "Partis"] = key
            col_count = 1
            started = True
            
        if(col_count == 2):
            final_df.loc[count, "Voix"] = value
         
        if(col_count == 4):
            col_count = 0
            count += 1
            
        

# Write recipe outputs
# Dataset test renamed to Presidentielle by admin on 2025-02-11 15:22:10
test = dataiku.Dataset("Presidentielle")
test.write_with_schema(final_df)
