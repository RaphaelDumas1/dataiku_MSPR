from check import check_columns_exist



# Used to delete row(s) in a dataframe where column equal value
def delete_rows_where_equal(df, column, value):
    check_columns_exist(df, [column])
    return df[df[column] != value].reset_index(drop=True)



# Used to delete row(s) in a dataframe where column not equal value
def delete_rows_where_not_equal(df, column, value):
    check_columns_exist(df, [column])
    return df[df[column] == value].reset_index(drop=True)



# Used to delete columns(s) in a dataframe from a list of column name(s) 
def delete_columns_in_list(df, columns_to_delete):
    check_columns_exist(df, columns_to_delete)
    return df.drop(columns=columns_to_delete)



# Used to delete columns(s) in a dataframe to keep only the one(s) in list
def delete_columns_not_in_list(df, columns_to_keep):
    check_columns_exist(df, columns_to_keep)
    return df[columns_to_keep]



# Used to delete row(s) from a list of indexe(s)
# The optionnal parameter max_index is used to remove rows after the given value
def delete_rows_by_index(df, indexes, max_index=None):
    if max_index is not None:
        df = df[df.index <= max_index]
        
    return df.drop(index=[i for i in indexes if i < len(df)], errors='ignore').reset_index(drop=True)