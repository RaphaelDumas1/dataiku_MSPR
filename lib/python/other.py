# Used to pivot a dataframe and rename it first column
def pivot(df, first_column_name):
    # Pivot
    df.set_index(df.columns[0], inplace=True)
    df = df.T.reset_index()

    # Rename column
    df = df.rename(columns={df.columns[0]: first_column_name})
    df.columns = make_list_values_unique(df.columns)
    
    return df


# Used to add 
def create_column_by_adding_columns_values(df, first_column, second_column, result_column):
    check_columns_exist(df, [first_column, second_column])

    df[result_column] = pd.to_numeric(df[first_column], errors='coerce') + pd.to_numeric(df[second_column], errors='coerce')
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