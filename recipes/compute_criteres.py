import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# 
# FUNCTIONS
#

def pivot_years(df):
    # Pivot
    df.set_index(df.columns[0], inplace=True)
    df = df.T.reset_index()

    # Rename column
    df.rename(columns={'index': 'Année'}, inplace=True)
    
    return df

def column_from_float_to_string(df, column):
    df["Année"] = df["Année"].astype(float).astype(int).astype(str)
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
    
    return df


#
# DATASETS
#

datasets = [
    {
        "input": "MSPR_Categorie_metiers",
        "output": "Categorie_metiers",
        "functions": [
            {
                 "name" : process_category_metier,
                 "args" : []   
            }
        ]
    },
]

#
# PROCESS
#

for dataset in datasets:
    # Set variables for iteration
    input_name = dataset["input"]
    output_name = dataset["output"]
    functions = dataset["functions"]
    
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