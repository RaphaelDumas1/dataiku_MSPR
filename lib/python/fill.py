from check import check_columns_exist
from utils import get_decimal_precision


# Used to fill empty values in a dataframe from a dict with key(s) as column name(s) and value(s) as replacement value(s)
def fill_empty_values(df, values_dict):
    check_columns_exist(df, values_dict.keys())
    
    for col, value in values_dict.items():
        df[col] = df[col].fillna("").apply(lambda x: x if str(x).strip() else value)
        
    return df



# Used to fill empty values of numerical column(s) from a list with the mean of the others values of the column(s)
def fill_empty_values_with_mean(df, columns):
    check_columns_exist(df, columns)
    
    for col in columns:
        df[col] = df[col].fillna(df[col].mean())
        
    return df



# Used to fill empty values of numerical column(s) with interpolation
def fill_with_interpolation(df, columns_to_exlude=[]):
    int_columns = df.select_dtypes(include='int').columns.drop(columns_to_exlude, errors='ignore')
    decimal_columns = df.select_dtypes(include='float').columns.drop(columns_to_exlude, errors='ignore')
    decimal_precision = get_decimal_precision(df, decimal_columns)
    num_columns = df.select_dtypes(include='number').columns.drop(columns_to_exlude, errors='ignore')
    
    # Interpolation + forward fill + backward fill
    df[num_columns] = df[num_columns]\
        .interpolate(method='linear', limit_direction='both')\
        .ffill()\
        .bfill()
    
    # Convert result to initial types
    for col in int_columns:
        df[col] = df[col].round().astype(int)

    for col, precision in decimal_precision.items():
        df[col] = df[col].round(precision)
        
    return df