from check import check_columns_exist
import pandas as pd



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
def column_to_decimal(df, column, round_to=None):
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



# Used to convert the type of the column(s) of a dataframe based on a dict with key(s) as column name(s) and value(s) as type(s) (int, decimal_round, str)
# If type is given directly instead of dict then convert all colum(s) of dataframe to this type 
def convert_columns(df, columns_or_type):
    columns = columns_or_type
    
    if not isinstance(columns, dict):
        columns = {key: columns_or_type for key in df.columns}
    
    check_columns_exist(df, columns.keys())
    
    for key, value in columns.items():
        key = key.strip() if isinstance(key, str) else key
        
        try:
            if value == 'int':
                df = column_to_int(df, key)
            elif value == 'str':
                df = column_to_string(df, key)
            elif value.startswith('decimal'):
                round_to = (value.split("_", 1) + [None])[1]
                df = column_to_decimal(df, key, int(round_to))
            
        except Exception as e:
            raise ValueError(f"Erreur de conversion dans la colonne '{key}': {e}")

    return df