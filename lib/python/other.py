import pandas as pd
from check import check_columns_exist
from utils import make_list_values_unique



# Used to pivot a dataframe and rename it first column
def pivot(df, first_column_name):
    # Pivot
    df.set_index(df.columns[0], inplace=True)
    df = df.T.reset_index()

    # Rename column
    df = df.rename(columns={df.columns[0]: first_column_name})
    df.columns = make_list_values_unique(df.columns)

    return df



# Used to add up multiple columns values to a new column
def create_column_by_adding_columns_values(df, columns, result_column):
    check_columns_exist(df, columns)

    df[result_column] = df[columns].apply(pd.to_numeric, errors='coerce').sum(axis=1)
    return df



# Used to add new rows based on given column range
def add_rows_from_column_range(df, column, start, end):
    df_full = pd.DataFrame({column: range(min(df[column].min(), start), end + 1)})
    return pd.merge(df_full, df, on=column, how='left')



# Used to rename columns based on a dict with keys as old names and values a new names
def rename_columns(df, columns_dict):
    check_columns_exist(df, columns_dict.keys())
    return df.rename(columns=columns_dict)



# Used to set the header(s) of the dataframe from the value(s) of the row with the given index
# Function parameter is used to make eventual post treatment on header(s)
def set_row_as_headers(df, index, function=None):
    df.columns = df.iloc[index]
    
    if function is not None:
        df.columns = function(df.columns)
    
    return df