print("tzs")
import dataiku
import pandas as pd, numpy as np
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
    
    'Blanc' : 'Blank'
}

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
        "first_party_col_name" : "Nuance candidat 1",
        "votes_col_nb" : 2,
        "cycle_length" : 4,
    },
    "2022" : {
        "df" : legislative_2022.get_dataframe(),
        "first_party_col_name" : "Code Nuance",
        "votes_col_nb" : 2,
        "cycle_length" : 5,
    },
    "2017" : {
        "df" : legislative_2017.get_dataframe(),
        "first_party_col_name" : "Code Nuance",
        "votes_col_nb" : 2,
        "cycle_length" : 5,
    },
    "2012" : {
        "df" : legislative_2012.get_dataframe(),
        "first_party_col_name" : "Code Nuance",
        "votes_col_nb" : 3,
        "cycle_length" : 5,
    },
    "2007" : {
        "df" : legislative_2007.get_dataframe(),
        "first_party_col_name" : "Code Nuance",
        "votes_col_nb" : 3,
        "cycle_length" : 5,
    },
    "2002" : {
        "df" : legislative_2002.get_dataframe(),
        "first_party_col_name" : "Code Nuance",
        "votes_col_nb" : 3,
        "cycle_length" : 5,
    },
    "1997" : {
        "df" : legislative_1997.get_dataframe(),
        "first_party_col_name" : "Code Nuance",
        "votes_col_nb" : 3,
        "cycle_length" : 5,
    },
    "1993" : {
        "df" : legislative_1993.get_dataframe(),
        "first_party_col_name" : "Code Nuance",
        "votes_col_nb" : 3,
        "cycle_length" : 3,
    },
}

# Create empty dataframe with columns needed
final_df = pd.DataFrame(columns=["année", "parti", "voix", "couleur"])

count = 0

# Iterate over dataframes
for key, df in dfs.items():
    headers = df["df"].columns 
    row = df["df"].iloc[0]
    col_count = 0
    
    # Iterate over first line values
    for index, (header, value) in enumerate(zip(headers, row)):
        
        # Create new row for blank votes
        if(header == "Blancs" or header == "Nuls" or header == "Blancs et nuls"):
            final_df.loc[count, "année"] = key
            final_df.loc[count, "parti"] = "Blanc"
            
            # Add blank and nulls if needed
            if pd.isna(final_df.at[count, "voix"]):
                final_df.loc[count, "voix"] = value
            else:
                final_df.loc[count, "voix"] += value
            
            if(header == "Nuls" or header == "Blancs et nuls"):
                count += 1
            
        
        # Increment since first party
        if(headers.get_loc(df["first_party_col_name"]) <= index):
            col_count += 1
            
        if(col_count == 1):
            final_df.loc[count, "année"] = key
            final_df.loc[count, "parti"] = value   
            
        if(col_count == df["votes_col_nb"]):
            final_df.loc[count, "voix"] = value
            
        if(col_count == df["cycle_length"]):
            col_count = 0
            count += 1

final_df['couleur'] = final_df['parti'].map(party_orientation)
final_df = columns_to_int(final_df, ["année", "voix"])

test = dataiku.Dataset("Legislatives")
test.write_with_schema(final_df)
