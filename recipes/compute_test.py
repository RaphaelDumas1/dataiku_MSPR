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


final_df = pd.DataFrame(columns=["Année", "Genre", "Nom", "Prénom", "Voix"])
count = 0

for key, df in dfs.items():
    headers = df.columns 
    row = df.iloc[0]
    col_count = 0
    started = false

    for header, value in zip(headers, row):
        if(col_count > 0):
            col_count += 1
            
        if(header == "Sexe" or started and col_count == 0):
            final_df.loc[count, "Année"] = key
            final_df.loc[count, "Genre"] = value   
            col_count = 1
            started = true
            
        if(col_count == 2):
            final_df.loc[count, "Nom"] = value
            
        if(col_count == 3)
            final_df.loc[count, "Prénom"] = value

        if(col_count == 4)
            final_df.loc[count, "Voix"] = value
         
        if(col_count == 6):
            col_count = 0
            count += 1
            
        

# Write recipe outputs
test = dataiku.Dataset("test")
test.write_with_schema(final_df)
