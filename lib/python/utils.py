import dataiku
import pandas as pd
import openpyxl
import time
from io import BytesIO
import re
from sqlalchemy import create_engine

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

def clean_title(title):
    return '_'.join(title.split()).replace(')', '').replace('(', '').replace('/', '_').replace('.', '_')

def create_dataframe_from_sheet(sheet):
    data = list(sheet.values)
    transposed = list(zip(*data))
    valid_columns = [(i, col[0]) for i, col in enumerate(transposed) if any(cell is not None and str(cell).strip() for cell in col)]
    headers = make_unique([str(h).strip() for _, h in valid_columns])
    rows = [[row[i] for i, _ in valid_columns] for row in data[1:]]
    return pd.DataFrame(rows, columns=headers)

def strip_headers(df):
    df.columns = df.columns.str.strip()
    return df

def find_entry_in_instructions(title, datasets_instructions):
    entry = next((d for d in datasets_instructions if d["name"] == title), None)
    if entry is None:
        raise ValueError(f"Aucune entrée trouvée pour le nom : '{title}'")
    return entry


def create_datasets_from_file_sheets(project_id, folder_id, file_name, datasets_instructions, sheets_to_exclude):
    client = dataiku.api_client()
    project = client.get_project(project_id)
    folder = dataiku.Folder(folder_id, project_key=project.project_key)

    with folder.get_download_stream(file_name) as file_handle:
        try:
            ss = openpyxl.load_workbook(BytesIO(file_handle.read()))
        except InvalidFileException:
            raise InvalidFileException("Fichier Excel invalide ou corrompu")
        except Exception as e:
            raise RuntimeError(f"Erreur inattendue lors du chargement du fichier : {e}")

    for sheet_name in ss.sheetnames:
        if sheet_name in sheets_to_exclude:
            continue

        sheet = ss[sheet_name]
        title = clean_title(sheet_name)
        df = create_dataframe_from_sheet(sheet)
        instruction = find_entry_in_instructions(title, datasets_instructions)
        
        execute_instruction_on_dataframe(df, title, instruction)

# Check if column exists in dataframe
def is_column_in_dataframe(df, column):
    if column not in df.columns:
        raise ValueError(f"Colonne '{column}' non trouvée dans le DataFrame.")
        
# Delete row(s) in dataframe where column equal value
def delete_where_equal(df, column, value):
    is_column_in_dataframe(df, column)
    return df[df[column] != value].reset_index(drop=True)

# Delete row(s) in dataframe where column not equal value
def delete_where_not_equal(df, column, value):
    is_column_in_dataframe(df, column)
    return df[df[column] == value].reset_index(drop=True)

# 
# FUNCTIONS
#

def pivot(df, first_column_name):
    # Pivot
    df.set_index(df.columns[0], inplace=True)
    df = df.T.reset_index()

    # Rename column
    df = df.rename(columns={df.columns[0]: first_column_name})
    
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

def columns_to_int(df, columns=None):
    if columns is None:
        columns = df.columns
    
    for column in columns:
        column = column.strip() if isinstance(column, str) else column

        if column not in df.columns:
            raise ValueError(f"Colonne '{column}' non trouvée dans le DataFrame.")

        try:
            df[column] = df[column].apply(lambda x: int(float(
                str(x)
                .replace('\xa0', '') 
                .replace(' ', '')
                .replace(',', '.')
            )) if pd.notnull(x) else x)
        except Exception as e:
            raise ValueError(f"Erreur de conversion dans la colonne '{column}': {e}")
            
        df[column] = df[column].astype("Int64")

    return df

def columns_to_float(df, columns=None, round=None):
    if columns is None:
        columns = df.columns

    for column in columns:
        column = column.strip() if isinstance(column, str) else column

        if column not in df.columns:
            raise ValueError(f"Colonne '{column}' non trouvée dans le DataFrame.")

        try:
            df[column] = df[column].apply(lambda x: float(
                str(x)
                .replace('\xa0', '')  # espace insécable
                .replace(' ', '')     # espace classique
                .replace(',', '.')    # virgule -> point
            ) if pd.notnull(x) else x)
        except Exception as e:
            raise ValueError(f"Erreur de conversion dans la colonne '{column}': {e}")
    
        if round is not None:
            df[column] = df[column].round(1)
    
    return df

def columns_to_string(df, columns=None):
    if columns is None:
        columns = df.columns

    for column in columns:
        column = column.strip() if isinstance(column, str) else column

        if column not in df.columns:
            raise ValueError(f"Colonne '{column}' non trouvée dans le DataFrame.")

        try:
            df[column] = df[column].apply(
                lambda x: str(int(x)) if isinstance(x, float) and x.is_integer()
                else str(x) if pd.notnull(x)
                else x
            )
        except Exception as e:
            raise ValueError(f"Erreur de conversion dans la colonne '{column}': {e}")

        df[column] = df[column].astype("string")

    return df

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

def rename_column(df, old_name, new_name):
    if old_name not in df.columns:
        raise ValueError(f"La colonne '{old_name}' n'existe pas dans le DataFrame.")
    return df.rename(columns={old_name: new_name})

def process_pib(df):
    if len(df) > 3:
        df.columns = df.iloc[2].astype(str).str.strip().str.replace(" \(r\)", "", regex=True)
        df.columns = make_unique(df.columns)
    else:
        raise ValueError("Le DataFrame ne contient pas au moins 4 lignes pour définir les headers")
    
    df = df[df.index <= 17]
    
    rows_to_prefix = [9, 10, 13, 14, 15]
    first_col = df.columns[0]

    prefix_sources = {
        9: 7,
        10: 7,
        13: 11,
        14: 11,
        15: 11
    }

    for i in rows_to_prefix:
        if i < len(df):
            val = df.at[i, first_col]
            if pd.notnull(val):
                source_row = prefix_sources.get(i)
                reference_value = str(df.at[source_row, first_col]).strip() if source_row in df.index else ""

                current_val = str(val).strip()
                new_val = f"{reference_value} dont {current_val}"

                if new_val in df[first_col].values:
                    new_val += " 2"

                df.at[i, first_col] = new_val

    
    # 3. Supprimer lignes 1 à 4, 5, 8, 10, 14 et toutes les lignes après 19
    rows_to_drop = list(range(0, 4)) + [6, 8, 12]
    df = df.drop(index=[i for i in rows_to_drop if i < len(df)], errors='ignore')

    

    # Réinitialiser les index
    df = df.reset_index(drop=True)

    return df

def process_inflation(df):
    df = df[df.index <= 35]
    
    if len(df) > 3:
        df.columns = df.iloc[2]
    else:
        raise ValueError("Le DataFrame ne contient pas au moins 4 lignes pour définir les headers")
        
    rows_to_drop = list(range(0, 3))
    df = df.drop(index=[i for i in rows_to_drop if i < len(df)], errors='ignore')
    
    df = df.reset_index(drop=True)
    return df
        
def process_annuaire(df):  
    delete_columns = ['code_departement', 'code_region', 'libelle_departement', 'libelle_region']

    df = df.drop(columns=delete_columns)
    df = df.dropna(how="all")
    columns_defaults = {
        "type_etablissement": "Inconnu",
        "statut_public_prive": "Inconnu",
        "adresse_1": "Inconnue",
        "adresse_2": "Inconnue",
        "ecole_maternelle": 0.0,
        "ecole_elementaire": 0.0,
        "voie_generale" : 0.0,
        "voie_technologique" : 0.0,
        "voie_professionnelle" : 0.0,
        "telephone": "Inconnu",
        "fax": "Inconnu", 
        "web": "Inconnu", 
        "mail": "Inconnu", 
        "telephone": "Inconnu", 
        "restauration": 0.0,
        "hebergement": 0.0,
        "ulis": 0.0,
        "apprentissage": 0.0,
        "segpa": 0.0,
        "section_arts": 0.0,
        "section_cinema": 0.0,
        "section_theatre": 0.0,
        "section_sport": 0.0,
        "section_internationale": 0.0,
        "section_europeenne": 0.0,
        "lycee_agricole": 0.0,
        "lycee_militaire": 0.0,
        "lycee_des_metiers": 0.0,
        "post_bac": 0.0,
        "appartenance_education_prioritaire": "Aucune",
        "greta": 0.0,
        "siren_siret": "Inconnu",
        "fiche_onisep": "Inconnue",
        "position": "48.856614,2.3522219",
        "type_contrat_prive": "Inconnu",
        "coordx_origine": "2.3522",
        "coordy_origine": "48.8566",
        "epsg_origine": "EPSG:2154",
        "nom_circonscription": "Inconnu",
        "latitude": "48.856614",
        "longitude": "2.3522219",
        "precision_localisation": "Inconnue",
        "rpi_concentre" : 0.0,
        "rpi_disperse" : 0.0,
        "pial" : "Inconnu",
        "etablissement_mere" : "Inconnu",
        "type_rattachement_etablissement_mere" : "Inconnu",
        "code_circonscription" : "Inconnu",
        "code_zone_animation_pedagogique" : "Inconnu",
        "libelle_zone_animation_pedagogique" : "Inconnu",
        "code_bassin_formation" : "Inconnu",
        "libelle_bassin_formation" : "Inconnu"
    }
        
    for col, default in columns_defaults.items():
        df[col] = df[col].fillna("").apply(lambda x: x if str(x).strip() else default)
    
    df["nombre_d_eleves"] = df["nombre_d_eleves"].fillna(df["nombre_d_eleves"].mean())
    
    return df
    
        
def execute_instruction_on_dataframe(df, title, instruction):
    engine = create_engine('postgresql://postgres:test@host.docker.internal:5432/MSPR')
    functions = instruction["functions"]
    instruction_name = instruction["name"]
   
    for function in functions:
        # Set variables for iteration
        name = function["name"]
        args = function["args"] if function["args"] is not None else []
        print("yes", df.columns)
        # Use function
        df = name(df, *args)

    # Drop empty rows
    df = df.dropna(how="all")
    df.columns = df.columns.str.lower()
    
    table_name = title.lower()

    # Exportation vers PostgreSQL
    df.to_sql(table_name, engine, if_exists='replace', index=False)

    # Write datas
    dataset = dataiku.Dataset(instruction_name)
    dataset.write_with_schema(df)

def extract_and_concat_to_original(df, interval1, interval2):
    
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
    
    print("lll", df_cleaned.columns, df1.columns, df2.columns)
    
    # On ne réindexe pas ici, on s'assure juste que les colonnes sont bien dans df_cleaned
    columns_to_add_1 = [col for col in df1.columns if col in df_cleaned.columns]
    columns_to_add_2 = [col for col in df2.columns if col in df_cleaned.columns]
    
    df_cleaned = df_cleaned[columns_to_add_1]
    df1 = df1[columns_to_add_1]
    df2 = df2[columns_to_add_1]
    
    df_cleaned = pd.concat([df_cleaned, df1, df2], axis=0, ignore_index=True)
    
    df_cleaned["Date référence"] = df_cleaned["Date référence"].astype(str).str[:4]
    df_cleaned.rename(columns={'Date référence': 'Année'}, inplace=True)
    
    delete_columns = ['Numéro département', 'Nom département', 'Numéro région', 'Nom région', "Lieu résidence"]

    df_cleaned = df_cleaned.drop(columns=delete_columns)

    return df_cleaned