import dataiku
import pandas as pd
import openpyxl
import time
from io import BytesIO
import re
from unidecode import unidecode



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

        if instructions.get(title, {}).get("post_treatment") != False:
            # Interpolate
            
            
            df = delete_rows_not_in_range(df, "annee", 2006, 2024)
                                
        # TODO if title not in ["annuaire_des_ecoles_en_france", "Delinquance"]:         
        
        dataset = dataiku.Dataset(title)
        dataset.write_with_schema(df)
        
        
        
# Used to make each element of a list unique by adding a number at the end of it to prevent duplicates   
def make_list_values_unique(list):
    seen = {}
    result = []
    for values in list:
        values = str(values).strip()
        if values not in seen:
            seen[values] = 1
            result.append(values)
        else:
            count = seen[values]
            new_values = f"{values}_{count}"
            while new_values in seen:
                count += 1
                new_h = f"{values}_{count}"
            seen[values] = count + 1
            seen[new_values] = 1
            result.append(new_values)
    return result       



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



#
# CHECK
#



# Used to check if given column(s) exist in a dataframe
def check_columns_exist(df, columns):
    for col in columns:
        if col not in df.columns:
            raise ValueError(f"Colonne '{col}' non trouvée dans le DataFrame.")

        
        
#
# DELETE
#



# Used to delete row(s) in a dataframe where column equal value
def delete_rows_where_equal(df, column, value):
    check_columns_exist(df, [column])
    return df[df[column] != value].reset_index(drop=True)



# Used to delete row(s) in a dataframe where column not equal value
def delete_rows_where_not_equal(df, column, value):
    check_columns_exist(df, [column])
    return df[df[column] == value].reset_index(drop=True)



# Used to delete columns(s) in list by name in a dataframe
def delete_columns_in_list(df, columns_to_delete):
    check_columns_exist(df, columns_to_delete)
    return df.drop(columns=columns_to_delete)



# Used to delete columns(s) to keep only the one(s) in list
def delete_columns_not_in_list(df, columns_to_keep):
    check_columns_exist(df, columns_to_keep)
    return df[columns_to_keep]



# Used to delete row(s) from a list of indexes
# The optionnal parameter max_index is used to remove rows after the given value
def delete_rows_by_index(df, indexes, max_index=None):
    if max_index is not None:
        df = df[df.index <= max_index]
        
    return df.drop(index=[i for i in indexes if i < len(df)], errors='ignore').reset_index(drop=True)

# Used to delete row(s) in a dataframe where column values lower than min_range parameter and higher than max_range parameter
def delete_rows_not_in_range(df, column, min_range, max_range):
    check_columns_exist(df, [column])
    return df[(df[column] >= min_range) & (df[column] <= max_range)]

#
# CONVERT
#



# Used to convert the given column of a dataframe to integer type
def column_to_int(df, column):
    df[column] = (
        df[column]
        .astype(str)
        .str.replace('\xa0', '', regex=False)
        .str.replace(' ', '', regex=False)
        .str.replace(',', '.', regex=False)
        .apply(lambda x: int(float(x)) if x.lower() != 'nan' else pd.NA)
        .astype("Int64")
    )
    return df



# Used to convert the given column of a dataframe to decimal type
def column_to_decima(df, column, round_to=None):
    df[column] = (
        df[column]
        .astype(str)
        .str.replace(r'[\s\xa0]', '', regex=True)
        .str.replace(',', '.', regex=False)
        .apply(lambda x: float(x) if x.lower() != 'nan' else pd.NA)
    )

    if round_to is not None:
        df[column] = df[column].round(round_to)

    return df



# Used to convert the given column of a dataframe to string type
def column_to_string(df, column):
    df[column] = (
        df[column]
        .apply(lambda x: str(int(x)) if isinstance(x, float) and x.is_integer()
               else str(x) if pd.notnull(x) else pd.NA)
        .astype("string")
    )
    return df



# Used to convert the types of the columns of a dataframe based on a dict with keys as columns names and value as types (int, decimal_round, str)
def convert_columns(df, columns):
    check_columns_exist(df, columns.keys())
    
    for key, value in columns.items():
        key = key.strip() if isinstance(key, str) else key
        
        try:
            if value == 'int':
                df = column_to_int(df, key)
            else if value == 'str':
                df = column_to_string(df, key)
            else if value.startswith('decimal'):
                round_to = (s.split("_", 1) + [None])[1]
                df = column_to_decimal(df, key, round_to)
            
        except Exception as e:
            raise ValueError(f"Erreur de conversion dans la colonne '{column}': {e}")

    return df


#
# FILL
#



# Used to fill empty values in a dataframe from a dict with keys as columns names and values as replacement values
def fill_empty_values(df, values_dict):
    check_columns_exist(df, values_dict.keys())
    
    for col, value in values_dict.items():
        df[col] = df[col].fillna("").apply(lambda x: x if str(x).strip() else value)
        
    return df



# Used to fill empty values of numericals columns from a list with the mean of the others values of the columns
def fill_empty_values_with_mean(df, columns):
    check_columns_exist(df, columns)
    
    for col in columns:
        df[col] = df[col].fillna(df[col].mean())
        
    return df



def interpolate(df):
    int_cols = df.select_dtypes(include='int').columns.drop('année', errors='ignore')
    float_cols = df.select_dtypes(include='float').columns.drop('année', errors='ignore')
    
    # Register float precision
    float_precision = {}
    for col in float_cols:
        non_null = df[col].dropna()
        if not non_null.empty:
            float_precision[col] = non_null.map(lambda x: len(str(x).split(".")[1]) if "." in str(x) else 0).max()
        else:
            float_precision[col] = 1

    full_years = pd.DataFrame({'année': range(min(df['année'].min(), 2006), 2025)})

    df_full = pd.merge(full_years, df, on='année', how='left')

    # Interpolation + extrapolation
    num_cols = df_full.select_dtypes(include='number').columns.drop('année')

    df_full[num_cols] = df_full[num_cols]\
        .interpolate(method='linear', limit_direction='both')\
        .ffill()
        .bfill()

    # Reconvertir les colonnes int d'origine
    for col in int_cols:
        df_full[col] = df_full[col].round().astype(int)

    # Arrondir les colonnes float au bon nombre de décimales
    for col, precision in float_precision.items():
        df_full[col] = df_full[col].round(precision)

    return df_full



def pivot(df, first_column_name):
    # Pivot
    df.set_index(df.columns[0], inplace=True)
    df = df.T.reset_index()

    # Rename column
    df = df.rename(columns={df.columns[0]: first_column_name})
    df.columns = make_list_values_unique(df.columns)
    
    return df

def copy_years_range(df):
    print("llll", df.columns)
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
    df.loc[0, "None_2"] = df.loc[0, "None"]  
    df.loc[0, "None_5"] = df.loc[0, "None_3"]  
    df.loc[0, "None_8"] = df.loc[0, "None_6"]  
    df = df.drop(columns=["None", "None_1", "None_3", "None_4", "None_6", "None_7"])
    df.columns = df.iloc[0] 
    df = df[1:].reset_index(drop=True) 
    
    return df

def process_evolution_trimestrielle_emploi(df):
    df = df.reset_index(drop=True)
    new_rows = []

    for i in range(0, len(df), 4):
        group = df.iloc[i:i+4]
        
        if group.empty:
            continue
        
        first_label = str(group.iloc[0, 0])
        match = re.search(r'\b(20\d{2}|19\d{2})\b', first_label)
        year = match.group(0) if match else f"Année_{i//4 + 1}"

        new_row = {df.columns[0]: year}

        # Moyenne des autres colonnes
        for col in df.columns[1:]:
            try:
                new_row[col] = pd.to_numeric(group[col], errors='coerce').mean().round(2)
            except:
                new_row[col] = None

        new_rows.append(new_row)

    return pd.DataFrame(new_rows)



def add_columns(df, col1, col2, result_column):
    if col1 not in df.columns or col2 not in df.columns:
        raise ValueError(f"Colonnes '{col1}' ou '{col2}' non trouvées dans le DataFrame.")

    try:
        df[result_column] = (
            pd.to_numeric(df[col1], errors='coerce')
            + pd.to_numeric(df[col2], errors='coerce')
        )
    except Exception as e:
        raise ValueError(f"Erreur lors de l'addition des colonnes : {e}")

    return df


def add_rows_from_column_range(df, column, start, end)
    df_full = pd.DataFrame({column: range(min(df[column].min(), start), end + 1)})
    return pd.merge(years, df, on='année', how='left')

def rename_columns(df, columns_dict):
    return df.rename(columns=columns_dict)

def set_row_as_headers(df, index, function=None):
    df.columns = df.iloc[index]
    
    if function is not None:
        df.columns = function(df.columns)

    return df


        


def extract_and_concat_to_original(df, interval1, interval2):
    df = df.reset_index(drop=True)
    # Fonction d'extraction
    def extract(df, start, end):
        block = df.iloc[start:end+1].copy()
        headers = block.iloc[0]
        sub_df = pd.DataFrame(block.values[1:], columns=headers)
        return sub_df.reset_index(drop=True), list(range(start, end+1))

    df1, idx1 = extract(df, *interval1)
    df2, idx2 = extract(df, *interval2)
    
    

    # Supprimer les lignes d'origine
    all_rows_to_drop = set(idx1 + idx2)
    df_cleaned = df.drop(index=all_rows_to_drop).reset_index(drop=True)
    df_cleaned = df_cleaned.dropna(how="all")
    
    df_cleaned.rename(columns={'Quotient familial': 'Caracteristiques'}, inplace=True)
    df1.rename(columns={'Situation familiale': 'Caracteristiques'}, inplace=True)
    df2.rename(columns={'Age responsable dossier': 'Caracteristiques'}, inplace=True)

    # On ne réindexe pas ici, on s'assure juste que les colonnes sont bien dans df_cleaned
    columns_to_add_1 = [col for col in df1.columns if col in df_cleaned.columns]
    columns_to_add_2 = [col for col in df2.columns if col in df_cleaned.columns]
    
    df_cleaned = df_cleaned[columns_to_add_1]
    df1 = df1[columns_to_add_1]
    df2 = df2[columns_to_add_1]
    
    df_cleaned = pd.concat([df_cleaned, df1, df2], axis=0, ignore_index=True)
    
    df_cleaned["Date référence"] = df_cleaned["Date référence"].astype(str).str[:4]
    df_cleaned.rename(columns={'Date référence': 'Année'}, inplace=True)

    return df_cleaned