import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
import logging

# 
# FUNCTIONS
#

def pivot_years(df):
    # Pivot
    df.set_index(df.columns[0], inplace=True)
    df = df.T.reset_index()

    # Rename column
    df = df.rename(columns={df.columns[0]: "Année"})
    
    return df

def column_from_float_to_string(df, column):
    df["Année"] = df["Année"].astype(float).astype(int).astype(str)
    return df

def columns_to_int(df, columns=None):
    
    
    if columns is None:
        columns = df.columns
    
    for col in columns:
        df[col] = df[col].astype(str).str.replace(" ", "").astype(float).astype('Int64')
        
    return df

def copy_years_range(df):
    # Add row for each year in range
    rows = []

    for index, row in df.iterrows():
        year_range = str(row['Année'])
        start_year, end_year = map(int, year_range.split('-'))

        if(index == (len(df) - 1)):
            end_year = end_year + 1

        for year in range(start_year, end_year):
            new_row = row.copy()
            new_row['Année'] = str(year)
            rows.append(new_row)
    
    return pd.DataFrame(rows)

def process_category_metier(df):
    # Remove headers rows
    df = df.drop(index=1)
    df = df.loc[:10]
    df.loc[0, "Unnamed: 3"] = df.loc[0, "Unnamed: 1"]  
    df.loc[0, "Unnamed: 6"] = df.loc[0, "Unnamed: 4"]  
    df.loc[0, "Unnamed: 9"] = df.loc[0, "Unnamed: 7"]  
    df = df.drop(columns=["Unnamed: 1", "Unnamed: 2", "Unnamed: 4", "Unnamed: 5", "Unnamed: 7", "Unnamed: 8"])
    df.columns = df.iloc[0] 
    df = df[1:].reset_index(drop=True) 
    
    return df


#
# DATASETS
#

datasets = [
    {
        "input": "MSPR_Categorie_logement",
        "output": "Categorie_logement",
        "functions": [
            {
                 "name" : pivot_years,
                 "args" : None
            },
            {
                 "name" : columns_to_int,
                 "args" : []
            }
        ]
    },
    {
        "input": "MSPR_Composition_menage",
        "output": "Composition_menage",
       "functions": [
            {
                 "name" : pivot_years,
                 "args" : None
            },
            {
                 "name" : columns_to_int,
                 "args" : []
            }
        ]
    },
    {
        "input": "MSPR_Delinquance",
        "output": "Delinquance",
        "functions": []
    },
    {
        "input": "MSPR_Evolution_population",
        "output": "Evolution_population",
        "functions": [
            {
                 "name" : pivot_years,
                 "args" : None
            },
            {
                 "name" : copy_years_range,
                 "args" : None
            },
        ]
    },
    {
        "input": "MSPR_Impot_moyen",
        "output": "Impot_moyen",
        "functions": []
    },
    {
        "input": "MSPR_Logement",
        "output": "Logement",
        "functions": [
            {
                 "name" : pivot_years,
                 "args" : None
            },
            {
                 "name" : column_from_float_to_string,
                 "args" : ["Année"]
            },
             {
                 "name" : columns_to_int,
                 "args" : [["Nombre de logements"]]
            }
        ]
    },
    {
        "input": "MSPR_Administration_penitentiaire",
        "output": "Administration_penitentiaire",
        "functions": [
            {
                 "name" : pivot_years,
                 "args" : None
            },
            {
                 "name" : column_from_float_to_string,
                 "args" : ["Année"]
            }
        ]
    },
    {
        "input": "MSPR_Nombre_de_salarie",
        "output": "Nombre_de_salarie",
        "functions": [
            {
                 "name" : columns_to_int,
                 "args" : [["Nombre de salarie"]]
            }
        ]
    },
    {
        "input": "MSPR_Nombre_detranger",
        "output": "Nombre_detranger",
        "functions": []
    },
    {
        "input": "MSPR_Nombre_dimmigre",
        "output": "Nombre_dimmigre",
        "functions": []
    },
    {
        "input": "MSPR_Nombre_enfant",
        "output": "Nombre_enfant",
        "functions": [
            {
                 "name" : pivot_years,
                 "args" : None
            },
            {
                 "name" : column_from_float_to_string,
                 "args" : ["Année"]
            }
        ]
    },
    {
        "input": "MSPR_Population",
        "output": "Population",
        "functions": []
    },
    {
        "input": "MSPR_Repartition_age",
        "output": "Repartition_age",
        "functions": [
            {
                 "name" : column_from_float_to_string,
                 "args" : ["Année"]
            }
        ]
    },
    {
        "input": "MSPR_Repartition_des_contrats",
        "output": "Repartition_des_contrats",
        "functions": [
            {
                 "name" : columns_to_int,
                 "args" : [["CDD", "CDI"]]
            }
        ]
    },
    {
        "input": "MSPR_Repartition_sexe",
        "output": "Repartition_sexe",
        "functions": [
            {
                 "name" : columns_to_int,
                 "args" : []
            }
        ]
    },
    {
        "input": "MSPR_Salaire_moyen",
        "output": "Salaire_moyen",
        "functions": []
    },
    {
        "input": "MSPR_Statut_occupation_logement",
        "output": "Statut_occupation_logement",
        "functions": [
            {
                 "name" : pivot_years,
                 "args" : None
            },
            {
                 "name" : columns_to_int,
                 "args" : []
            }
        ]
    },
    {
        "input": "MSPR_Taux_de_chomage",
        "output": "Taux_de_chomage",
        "functions": []
    },
    {
        "input": "MSPR_Taux_de_mortalite",
        "output": "Taux_de_mortalite",
        "functions": []
    },
    {
        "input": "MSPR_Taux_de_natalite",
        "output": "Taux_de_natalite",
        "functions": []
    },
    {
        "input": "MSPR_Taux_de_pauvrete",
        "output": "Taux_de_pauvrete",
        "functions": []
    },
    {
        "input": "MSPR_Type_logement",
        "output": "Type_logement",
        "functions": [
            {
                 "name" : pivot_years,
                 "args" : None
            },
            {
                 "name" : columns_to_int,
                 "args" : []
            }
        ]
    },
    {
        "input": "MSPR_Taux_scolarisation",
        "output": "Taux_scolarisation",
        "functions": [
            {
                 "name" : column_from_float_to_string,
                 "args" : ["Année"]
            }
        ]
    },
    {
        "input": "MSPR_Categorie_metiers",
        "output": "Categorie_metiers",
        "functions": [
            {
                 "name" : process_category_metier,
                 "args" : []   
            },
            {
                 "name" : pivot_years,
                 "args" : []   
            },
            {
                 "name" : columns_to_int,
                 "args" : []
            }
            
        ]
    },
    
]

#
# PROCESS
#

logger = logging.getLogger()

for dataset in datasets:
    # Set variables for iteration
    input_name = dataset["input"]
    output_name = dataset["output"]
    functions = dataset["functions"]
    logger.info(output_name)
    
    # Get datas
    dataset = dataiku.Dataset(input_name)
    df = dataset.get_dataframe()
    
    for function in functions:
        # Set variables for iteration
        name = function["name"]
        args = function["args"] if function["args"] is not None else []

        # Transform
        df = name(df, *args)
        
    # Drop empty rows
    df = df.dropna(how="all")

    # Write datas
    result_dataset = dataiku.Dataset(output_name)
    result_dataset.write_with_schema(df)