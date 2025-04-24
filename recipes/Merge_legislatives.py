import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
from convert import convert_columns

party_orientation = {
    # Far-left parties
    'EXG': 'Far_Left', 'LO': 'Far_Left', 'LCR': 'Far_Left',

    # Left-wing parties
    'COM': 'Left', 'FG': 'Left', 'SOC': 'Left', 'RDG': 'Left',
    'DVG': 'Left', 'VEC': 'Left', 'ECO': 'Left', 'FI': 'Left',
    'NUP': 'Left', 'UG': 'Left', 'DXG': 'Left', 'PRS': 'Left',
    'GEC': 'Left', 'PRG': 'Left',

    # Center parties
    'CEN': 'Center', 'MDM': 'Center', 'UDI': 'Center', 'DVC': 'Center',
    'REM': 'Center', 'ENS': 'Center', 'ALLI': 'Center', 'UDF': 'Center', 'UDFD': 'Center',

    # Right-wing parties
    'UMP': 'Right', 'RPR': 'Right', 'LR': 'Right', 'DVD': 'Right', 
    'MAJ': 'Right', 'PRV': 'Right', 'NCE': 'Right', 'DL': 'Right',
    'DIV': 'Right', 'CPNT': 'Right', 'REG': 'Right', 'PREP': 'Right',
    'AUT': 'Right',

    # Far-right parties
    'FN': 'Far_Right', 'RN': 'Far_Right', 'FRN': 'Far_Right', 'MNR': 'Far_Right',
    'EXD': 'Far_Right', 'DLF': 'Far_Right', 'DSV': 'Far_Right', 'REC': 'Far_Right',
    'MPF': 'Far_Right', 'RPF': 'Far_Right',
    
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
        "first_party_col_name" : "nuance candidat 1",
        "votes_col_nb" : 2,
        "cycle_length" : 4,
    },
    "2022" : {
        "df" : legislative_2022.get_dataframe(),
        "first_party_col_name" : "code nuance",
        "votes_col_nb" : 2,
        "cycle_length" : 5,
    },
    "2017" : {
        "df" : legislative_2017.get_dataframe(),
        "first_party_col_name" : "code nuance",
        "votes_col_nb" : 2,
        "cycle_length" : 5,
    },
    "2012" : {
        "df" : legislative_2012.get_dataframe(),
        "first_party_col_name" : "code nuance",
        "votes_col_nb" : 3,
        "cycle_length" : 5,
    },
    "2007" : {
        "df" : legislative_2007.get_dataframe(),
        "first_party_col_name" : "code nuance",
        "votes_col_nb" : 3,
        "cycle_length" : 5,
    },
    "2002" : {
        "df" : legislative_2002.get_dataframe(),
        "first_party_col_name" : "code nuance",
        "votes_col_nb" : 3,
        "cycle_length" : 5,
    },
    "1997" : {
        "df" : legislative_1997.get_dataframe(),
        "first_party_col_name" : "code nuance",
        "votes_col_nb" : 3,
        "cycle_length" : 5,
    },
    "1993" : {
        "df" : legislative_1993.get_dataframe(),
        "first_party_col_name" : "code nuance",
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
        if(header == "blancs" or header == "nuls" or header == "blancs et nuls"):
            final_df.loc[count, "année"] = key
            final_df.loc[count, "parti"] = "blanc"
            
            # Add blank and nulls if needed
            if pd.isna(final_df.at[count, "voix"]):
                final_df.loc[count, "voix"] = value
            else:
                final_df.loc[count, "voix"] += value
            
            if(header == "nuls" or header == "blancs et nuls"):
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
final_df = convert_columns(final_df, {"année" : 'int', "voix" : 'int'})
final_df = final_df[final_df['année'] >= 2006]

test = dataiku.Dataset("Legislatives")
test.write_with_schema(final_df)
