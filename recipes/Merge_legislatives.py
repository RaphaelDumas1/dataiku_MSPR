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
    "2024" : {
        "df" : legislative_2024.get_dataframe(),
        "party_col_name" : "Nuance candidat 1",
        "voices_col_nb" : 2,
        "total_cycle" : 4,
    },
    "2022" : {
        "df" : legislative_2022.get_dataframe(),
        "party_col_name" : "Code Nuance",
        "voices_col_nb" : 2,
        "total_cycle" : 5,
    },
    "2017" : {
        "df" : legislative_2017.get_dataframe(),
        "party_col_name" : "Code Nuance",
        "voices_col_nb" : 2,
        "total_cycle" : 5,
    },
    "2012" : {
        "df" : legislative_2012.get_dataframe(),
        "party_col_name" : "Code Nuance",
        "voices_col_nb" : 3,
        "total_cycle" : 5,
    },
    "2007" : {
        "df" : legislative_2007.get_dataframe(),
        "party_col_name" : "Code Nuance",
        "voices_col_nb" : 3,
        "total_cycle" : 5,
    },
    "2002" : {
        "df" : legislative_2002.get_dataframe(),
        "party_col_name" : "Code Nuance",
        "voices_col_nb" : 3,
        "total_cycle" : 5,
    },
    "1997" : {
        "df" : legislative_1997.get_dataframe(),
        "party_col_name" : "Code Nuance",
        "voices_col_nb" : 3,
        "total_cycle" : 5,
    },
    "1993" : {
        "df" : legislative_1993.get_dataframe(),
        "party_col_name" : "Code Nuance",
        "voices_col_nb" : 3,
        "total_cycle" : 5,
    },
}

# Create empty dataframe with columns needed
final_df = pd.DataFrame(columns=["Année", "Parti", "Voix"])

count = 0

# Iterate over dataframes
for key, df in dfs.items():
    print(f"key")
    headers = df["df"].columns 
    row = df["df"].iloc[0]
    col_count = 0
    
    # Iterate over first line values
    for index, (header, value) in enumerate(zip(headers, row)):
        
        # Create new row for blank votes
        if(header == "Blancs" or header == "Nuls" or header == "Blancs et nuls"):
            final_df.loc[count, "Année"] = key
            final_df.loc[count, "Parti"] = "Blanc"
            final_df.loc[count, "Voix"] = final_df.loc[count, "Voix"].fillna(0) + value
            
            if(header == "Nuls" or header == "Blancs et nuls"):
                count += 1
            
        
        # Increment since first party
        if(headers.get_loc(df["party_col_name"]) <= index):
            col_count += 1
            
        if(col_count == 1):
            final_df.loc[count, "Année"] = key
            final_df.loc[count, "Parti"] = value   
            
        if(col_count == df["voices_col_nb"]):
            final_df.loc[count, "Voix"] = value
            
        if(col_count == df["total_cycle"]):
            col_count = 0
            count += 1
        

test = dataiku.Dataset("Legislatives")
test.write_with_schema(final_df)
