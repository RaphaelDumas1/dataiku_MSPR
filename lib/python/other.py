def pivot(df, first_column_name):
    # Pivot
    df.set_index(df.columns[0], inplace=True)
    df = df.T.reset_index()

    # Rename column
    df = df.rename(columns={df.columns[0]: first_column_name})
    df.columns = make_list_values_unique(df.columns)
    
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

#
def add_rows_from_column_range(df, column, start, end)
    df_full = pd.DataFrame({column: range(min(df[column].min(), start), end + 1)})
    return pd.merge(df_full, df, on=column, how='left')

def rename_columns(df, columns_dict):
    return df.rename(columns=columns_dict)

def set_row_as_headers(df, index, function=None):
    df.columns = df.iloc[index]
    
    if function is not None:
        df.columns = function(df.columns)

    return df