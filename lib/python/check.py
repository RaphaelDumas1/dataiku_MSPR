# Used to check if given column(s) exist in a dataframe
def check_columns_exist(df, columns):
    for col in columns:
        if col not in df.columns:
            raise ValueError(f"Colonne '{col}' non trouvée dans le DataFrame.")