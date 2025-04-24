

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



# Used to fill empty values of numericals columns with interpolation
def fill_with_interpolation(df, columns_to_exlude=[]):
    int_columns = df.select_dtypes(include='int').columns.drop(columns_to_exlude, errors='ignore')
    float_columns = df.select_dtypes(include='float').columns.drop(columns_to_exlude, errors='ignore')
    float_precision = get_float_precision(df, float_cols)
    num_columns = df.select_dtypes(include='number').columns.drop(columns_to_exlude, errors='ignore')
    df[num_cols] = df[num_cols]\
        .interpolate(method='linear', limit_direction='both')\
        .ffill()\
        .bfill()

    for col in int_cols:
        df_full[col] = df_full[col].round().astype(int)

    for col, precision in float_precision.items():
        df_full[col] = df_full[col].round(precision)
        
    return df