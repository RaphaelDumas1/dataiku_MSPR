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

# Create empty dataframe with columns needed
final_df = pd.DataFrame(columns=["Année", "Parti", "Voix"])

count = 0

# Iterate over dataframes
for key, df in dfs.items():
    headers = df.columns 
    first_party_position = next((headers.get_loc(col) for col in ["Nuance candidat 1", "Code Nuance"] if col in headers), None)
    row = df.iloc[0]
    col_count = 0
    
    # Iterate over first line values
    for index, (header, value) in enumerate(zip(headers, row)):
        
        # Create new row for blank votes
        if(header == "Blancs" or header == "Nuls" or header == "Blancs et nuls"):
            final_df.loc[count, "Année"] = key
            final_df.loc[count, "Parti"] = "Blanc"
            final_df.loc[count, "Voix"] += value
            
            if(header == "Nuls" or header == "Blancs et nuls"):
                count += 1
            
        
        # Increment since first party
        if(first_party_position <= index):
            col_count += 1
            
        if(col_count == 1):
            final_df.loc[count, "Année"] = key
            final_df.loc[count, "Parti"] = value   
            
        if(col_count == 2):
            final_df.loc[count, "Voix"] = value
            
        if(col_count == 3):
            final_df.loc[count, "Prénom"] = value
            
        

# Write recipe outputs
# Dataset test renamed to Presidentielle by admin on 2025-02-11 15:22:10
# Dataset test1 renamed to Legislatives by admin on 2025-02-11 18:01:36
test = dataiku.Dataset("Legislatives")
test.write_with_schema(final_df)
