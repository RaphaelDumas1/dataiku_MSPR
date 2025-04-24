# Special treatment for catgeoriemetier
def process_categorie_metier(df):
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

def copy_years_range(df):
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