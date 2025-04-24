import dataiku
import pandas as pd
import openpyxl
import time
from io import BytesIO
import re
from unidecode import unidecode
from utils import make_list_values_unique


#
# Environnement
#

PROJECT_ID = "MSPR"
SOURCE_FOLDER_ID = "Datas"



#
# Global
#


# Used in recipes to create datasets for each sheets in Excel file given in parameter
# Intructions parameter is a dict used to pass function(s) to apply before writing the datasets
def create_datasets_from_file_sheets(file_name, instructions):
    
    # Loading source
    
    client = dataiku.api_client()
    project = client.get_project(PROJECT_ID)
    folder = dataiku.Folder(SOURCE_FOLDER_ID, project_key=project.project_key)
    
    # Loading file sheets
    
    with folder.get_download_stream(file_name) as file_handle:
        try:
            ss = openpyxl.load_workbook(BytesIO(file_handle.read()))
        except InvalidFileException:
            raise InvalidFileException("Fichier Excel invalide ou corrompu")
        except Exception as e:
            raise RuntimeError(f"Erreur inattendue lors du chargement du fichier : {e}")
    
     # Iterate over sheets
    
    for sheet_name in ss.sheetnames:
        sheet = ss[sheet_name]
        title = '_'.join(sheet_name.split()).replace(')', '').replace('(', '').replace('/', '_').replace('.', '_')
        
        if title not in instructions:
            continue
        
        df = create_dataframe_from_sheet(sheet)
        df = execute_instructions_on_dataframe(df, instructions[title])
        
        
        # Post treatment and write dataset
        
        df.columns = [unidecode(col).lower() for col in df.columns]

        if instructions[title].get("post_treatment") != False:
            df = add_rows_from_column_range(df, "annee", 2006, 2024)
            df = fill_with_interpolation(df, "annee")                    
                                
        # TODO if title not in ["annuaire_des_ecoles_en_france", "Delinquance"]:         
        
        dataset = dataiku.Dataset(title)
        dataset.write_with_schema(df)
        


# Used to convert a sheet in a dataframe
def create_dataframe_from_sheet(sheet):
    # Get datas in a list
    data = list(sheet.values)
    transposed = list(zip(*data))
 
    # Remove empty columns
    valid_columns = [(i, col[0]) for i, col in enumerate(transposed) if any(cell is not None and str(cell).strip() for cell in col)]
    
    headers = make_list_values_unique([str(h).strip() for _, h in valid_columns])
    rows = [[row[i] for i, _ in valid_columns] for row in data[1:]]
    
    return pd.DataFrame(rows, columns=headers).dropna(how="all")



# Used to execute each function in instructions on a dataframe   
def execute_instructions_on_dataframe(df, instructions):
    for instruction in instructions:
        function = instruction["name"]
        args = instruction["args"] if instruction["args"] is not None else []

        df = function(df, *args)
    
    return df