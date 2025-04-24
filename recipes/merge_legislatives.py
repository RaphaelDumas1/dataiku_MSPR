import dataiku
import pandas as pd
from convert import convert_columns
from utils import get_dataframe_from_dataset

#
# Datas
#

party_labels = {
    'EXG': 'Far_Left', 'LO': 'Far_Left', 'LCR': 'Far_Left',

    'COM': 'Left', 'FG': 'Left', 'SOC': 'Left', 'RDG': 'Left',
    'DVG': 'Left', 'VEC': 'Left', 'ECO': 'Left', 'FI': 'Left',
    'NUP': 'Left', 'UG': 'Left', 'DXG': 'Left', 'PRS': 'Left',
    'GEC': 'Left', 'PRG': 'Left',

    'CEN': 'Center', 'MDM': 'Center', 'UDI': 'Center', 'DVC': 'Center',
    'REM': 'Center', 'ENS': 'Center', 'ALLI': 'Center', 'UDF': 'Center', 'UDFD': 'Center',

    'UMP': 'Right', 'RPR': 'Right', 'LR': 'Right', 'DVD': 'Right', 
    'MAJ': 'Right', 'PRV': 'Right', 'NCE': 'Right', 'DL': 'Right',
    'DIV': 'Right', 'CPNT': 'Right', 'REG': 'Right', 'PREP': 'Right',
    'AUT': 'Right',

    'FN': 'Far_Right', 'RN': 'Far_Right', 'FRN': 'Far_Right', 'MNR': 'Far_Right',
    'EXD': 'Far_Right', 'DLF': 'Far_Right', 'DSV': 'Far_Right', 'REC': 'Far_Right',
    'MPF': 'Far_Right', 'RPF': 'Far_Right',
    
    'blanc' : 'Blank'
}


dataframes = {
    "2024" : {
        "df" : get_dataframe_from_dataset("Legislative_2024"),
        "first_party_col_name" : "nuance candidat 1",
        "votes_col_nb" : 2,
        "cycle_length" : 4,
    },
    "2022" : {
        "df" : get_dataframe_from_dataset("Legislative_2022"),
        "first_party_col_name" : "code nuance",
        "votes_col_nb" : 2,
        "cycle_length" : 5,
    },
    "2017" : {
        "df" : get_dataframe_from_dataset("Legislative_2017"),
        "first_party_col_name" : "code nuance",
        "votes_col_nb" : 2,
        "cycle_length" : 5,
    },
    "2012" : {
        "df" : get_dataframe_from_dataset("Legislative_2012"),
        "first_party_col_name" : "code nuance",
        "votes_col_nb" : 3,
        "cycle_length" : 5,
    },
    "2007" : {
        "df" : get_dataframe_from_dataset("Legislative_2007"),
        "first_party_col_name" : "code nuance",
        "votes_col_nb" : 3,
        "cycle_length" : 5,
    },
    "2002" : {
        "df" : get_dataframe_from_dataset("Legislative_2002"),
        "first_party_col_name" : "code nuance",
        "votes_col_nb" : 3,
        "cycle_length" : 5,
    },
    "1997" : {
        "df" : get_dataframe_from_dataset("Legislative_1997"),
        "first_party_col_name" : "code nuance",
        "votes_col_nb" : 3,
        "cycle_length" : 5,
    },
    "1993" : {
        "df" : get_dataframe_from_dataset("Legislative_1993"),
        "first_party_col_name" : "code nuance",
        "votes_col_nb" : 3,
        "cycle_length" : 3,
    },
}

#
# Logic
#

# Create empty dataframe with columns needed
final_df = pd.DataFrame(columns=["annee", "parti", "voix", "couleur"])

new_rows_count = 0

# Iterate over dataframes
for year, dataframe in dataframes.items():
    headers = dataframe["df"].columns 
    row = dataframe["df"].iloc[0]
    column_count = 0
    
    # Iterate over first line values
    for index, (header, value) in enumerate(zip(headers, row)):
        
        # Create new row for blank votes
        if(header == "blancs" or header == "nuls" or header == "blancs et nuls"):
            final_df.loc[new_rows_count, "annee"] = year
            final_df.loc[new_rows_count, "parti"] = "blanc"
            
            # Add blank and nulls if needed
            if pd.isna(final_df.at[new_rows_count, "voix"]):
                final_df.loc[new_rows_count, "voix"] = value
            else:
                final_df.loc[new_rows_count, "voix"] += value
            
            if(header == "nuls" or header == "blancs et nuls"):
                new_rows_count += 1
            
        
        # Increment since first party
        if(headers.get_loc(dataframe["first_party_col_name"]) <= index):
            column_count += 1
            
        if(column_count == 1):
            final_df.loc[new_rows_count, "annee"] = year
            final_df.loc[new_rows_count, "parti"] = value   
            
        if(column_count == dataframe["votes_col_nb"]):
            final_df.loc[new_rows_count, "voix"] = value
            
        if(column_count == dataframe["cycle_length"]):
            column_count = 0
            new_rows_count += 1

# Post treatment
final_df['couleur'] = final_df['parti'].map(party_labels)
final_df = convert_columns(final_df, {"annee" : 'int', "voix" : 'int'})
final_df = final_df[final_df['annee'] >= 2006]

# Write to dataset
results = dataiku.Dataset("Legislatives")
results.write_with_schema(final_df)