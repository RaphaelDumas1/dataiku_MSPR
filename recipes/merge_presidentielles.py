import dataiku
import pandas as pd
from convert import convert_columns
from utils import get_dataframe_from_dataset

#
# Datas
#

candidates_labels = {
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
    
    'BLANC': 'Blank'
}


dataframes = {
    "2022" : get_dataframe_from_dataset("Presidentielle_2022"),
    "2017" : get_dataframe_from_dataset("Presidentielle_2017"),
    "2012" : get_dataframe_from_dataset("Presidentielle_2012"),
    "2007" : get_dataframe_from_dataset("Presidentielle_2007"),
    "2002" : get_dataframe_from_dataset("Presidentielle_2002"),
    "1995" : get_dataframe_from_dataset("Presidentielle_1995")
}

#
# Logic
#

# Create empty dataframe with columns needed
final_df = pd.DataFrame(columns=["annee", "genre", "nom", "prenom", "voix", "couleur"])

new_rows_count = 0

# Iterate over dataframes
for year, dataframe in dataframes.items():
    headers = dataframe.columns 
    row = dataframe.iloc[0]
    column_count = 0
    
    # Iterate over first line values
    for index, (header, value) in enumerate(zip(headers, row)):
        
        # Create new row for blank votes
        if(header == "blancs" or header == "blancs et nuls"):
            final_df.loc[new_rows_count, "annee"] = year
            final_df.loc[new_rows_count, "nom"] = "BLANC"
            final_df.loc[new_rows_count, "prenom"] = "Blanc"
            final_df.loc[new_rows_count, "voix"] = value
            final_df.loc[new_rows_count, "genre"] = "NA"
            new_rows_count += 1
        
        # Increment since first candidate
        if(headers.get_loc("sexe") <= index):
            column_count += 1
            
        if(column_count == 1):
            final_df.loc[new_rows_count, "annee"] = year
            final_df.loc[new_rows_count, "genre"] = value   
            
        if(column_count == 2):
            final_df.loc[new_rows_count, "nom"] = value
            
        if(column_count == 3):
            final_df.loc[new_rows_count, "prenom"] = value

        if(column_count == 4):
            final_df.loc[new_rows_count, "voix"] = value

        if(column_count == 6):
            column_count = 0
            new_rows_count += 1

# Post treatment
final_df['couleur'] = final_df['nom'].map(candidates_labels)
final_df = convert_columns(final_df, {"annee" : 'int', "voix" : 'int'})
final_df = final_df[final_df['annee'] >= 2006]

# Write to dataset
results = dataiku.Dataset("Presidentielles")
results.write_with_schema(final_df)