import dataiku
import pandas as pd
import openpyxl
import time
from io import BytesIO

def make_unique(headers):
    seen = {}
    result = []
    for h in headers:
        h = str(h).strip()
        if h not in seen:
            seen[h] = 1
            result.append(h)
        else:
            count = seen[h]
            new_h = f"{h}_{count}"
            while new_h in seen:
                count += 1
                new_h = f"{h}_{count}"
            seen[h] = count + 1
            seen[new_h] = 1
            result.append(new_h)
    return result

def create_datasets_from_file_sheets(project_id, folder_id, file_name, datasets, exclude_sheets):
    client = dataiku.api_client()
    project = client.get_project(project_id)
    folder = dataiku.Folder(folder_id, project_key=project.project_key)

    datasets_in_project = []
    for dataset in project.list_datasets():
        datasets_in_project.append(dataset.get('name'))

    with folder.get_download_stream(file_name) as file_handle:
        try:
            ss = openpyxl.load_workbook(BytesIO(file_handle.read()))
        except Exception:
            print("tz")

    for sheet in ss.sheetnames:
        if sheet in exclude_sheets:
            continue

        ss_sheet = ss[sheet]
        title = ss_sheet.title
        title = '_'.join(title.split()).replace(')', '').replace('(', '').replace('/', '_').replace('.', '_')
        
        data = list(ss_sheet.values)
        
        headers = data[0]
        rows = data[1:]
        # Garder uniquement les colonnes dont l'en-tête n'est pas None ou vide
        valid_columns = [(i, h) for i, h in enumerate(headers) if h is not None and str(h).strip() != '']

        # Extraire les colonnes valides pour le DataFrame
        filtered_headers = make_unique([h for _, h in valid_columns])
        filtered_rows = [[row[i] for i, _ in valid_columns] for row in rows]
        

        # Construire le DataFrame propre
        df = pd.DataFrame(filtered_rows, columns=filtered_headers)
        entry = next((d for d in datasets if d["name"] == title), None)
        
        if entry is None:
            raise ValueError(f"Aucune entrée trouvée pour le nom : '{title}'")
        
        df = process(df, entry)
        
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
    df = df.rename(columns={df.columns[0]: "Année"})
    
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
    df.columns = df.iloc[0] 
    df = df[1:].reset_index(drop=True) 
    
    return df

def to_intt(df, columns):
    for column in columns:
        column = column.strip() if isinstance(column, str) else column

        if column not in df.columns:
            raise ValueError(f"Colonne '{column}' non trouvée dans le DataFrame.")

        try:
            df[column] = df[column].apply(lambda x: int(float(x)) if pd.notnull(x) else x)
        except Exception as e:
            raise ValueError(f"Erreur de conversion dans la colonne '{column}': {e}")

    return df

def process(df, dataset):
    # Set variables for iteration
    namee = dataset["name"]
    functions = dataset["functions"]

    for function in functions:
        # Set variables for iteration
        name = function["name"]
        args = function["args"] if function["args"] is not None else []

        # Transform
        df = name(df, *args)

    # Drop empty rows
    df = df.dropna(how="all")

    # Write datas
    result_dataset = dataiku.Dataset(namee)
    result_dataset.write_with_schema(df)