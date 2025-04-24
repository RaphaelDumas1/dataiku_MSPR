# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
from convert import convert_columns

candidate_orientation = {
    'MÉLENCHON': 'Far_Left',
    'ARTHAUD': 'Far_Left',
    'ROUSSEL': 'Far_Left',
    'POUTOU': 'Far_Left',
    'BESANCENOT': 'Far_Left',
    'GLUCKSTEIN': 'Far_Left',
    'LAGUILLER': 'Far_Left',
    'BUFFET': 'Far_Left',
    'HUE': 'Far_Left',
    'SCHIVARDI': 'Far_Left',

    'HOLLANDE': 'Left',
    'ROYAL': 'Left',
    'JOSPIN': 'Left',
    'HAMON': 'Left',
    'HIDALGO': 'Left',
    'TAUBIRA': 'Left',
    'CHEVENEMENT': 'Left',

    'JADOT': 'Green',
    'JOLY': 'Green',
    'VOYNET': 'Green',
    'MAMERE': 'Green',
    'BOVÉ': 'Green',
    'LEPAGE': 'Green',

    'MACRON': 'Center',
    'BAYROU': 'Center',
    'CHEMINADE': 'Center',
    'LASSALLE': 'Center',
    'BOUTIN': 'Center',

    'SARKOZY': 'Right',
    'FILLON': 'Right',
    'BALLADUR': 'Right',
    'CHIRAC': 'Right',
    'PÉCRESSE': 'Right',
    'MADELIN': 'Right',
    'SAINT-JOSSE': 'Right',

    'LE PEN': 'Far_Right',
    'ZEMMOUR': 'Far_Right',
    'DUPONT-AIGNAN': 'Far_Right',
    'ASSELINEAU': 'Far_Right',
    'NIHOUS': 'Far_Right',
    'MEGRET': 'Far_Right',
    'de VILLIERS': 'Far_Right',
    'VILLIERS DE': 'Far_Right',
    
    'blanc': 'Blank'
}

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

# Create empty dataframe with columns needed
final_df = pd.DataFrame(columns=["année", "genre", "nom", "prénom", "voix", "couleur"])

count = 0

# Iterate over dataframes
for key, df in dfs.items():
    headers = df.columns 
    row = df.iloc[0]
    col_count = 0
    
    # Iterate over first line values
    for index, (header, value) in enumerate(zip(headers, row)):
        
        # Create new row for blank votes
        if(header == "blancs" or header == "blancs et nuls"):
            final_df.loc[count, "année"] = key
            final_df.loc[count, "nom"] = "Blanc"
            final_df.loc[count, "prénom"] = "Blanc"
            final_df.loc[count, "voix"] = value
            final_df.loc[count, "genre"] = "NA"
            count += 1
        
        # Increment since first candidate
        if(headers.get_loc("sexe") <= index):
            col_count += 1
            
        if(col_count == 1):
            final_df.loc[count, "année"] = key
            final_df.loc[count, "genre"] = value   
            
        if(col_count == 2):
            final_df.loc[count, "nom"] = value
            
        if(col_count == 3):
            final_df.loc[count, "prénom"] = value

        if(col_count == 4):
            final_df.loc[count, "voix"] = value
         
        if(col_count == 6):
            col_count = 0
            count += 1

final_df['couleur'] = final_df['nom'].map(candidate_orientation)
final_df = convert_columns(final_df, {"année" : 'int', "voix" : 'int'})
final_df = final_df[final_df['année'] >= 2006]

# Dataset Presidentielle renamed to Presidentielles by admin on 2025-02-11 18:01:24
results = dataiku.Dataset("Presidentielles")
results.write_with_schema(final_df)
