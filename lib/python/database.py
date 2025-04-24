from sqlalchemy import create_engine, inspect, text



# Used to build an SQL query from given table name
# Parameter source_row is used to pick values to insert in column(s) define in parameter df_to_db_mapping
# Parameter columns_to_add is used as a dict containing db column(s) as key(s) and value(s) to put in it
def build_insert_query(table_name, source_row=None, df_to_db_mapping={}, columns_to_add={}, returning=None):
    values = {}
    
    # Get values in row with mapping
    if source_row is not None:
        values = {db_column: source_row[df_column] for df_column, db_column in df_to_db_mapping.items()}
        
    values.update(columns_to_add)
    
    columns_str = ", ".join(values.keys())
    placeholders = ", ".join([f":{col}" for col in values.keys()])
    
    query = f"""
        INSERT INTO {table_name} ({columns_str})
        VALUES ({placeholders})
    """
    
    if returning:
        query += f"\nRETURNING {returning}"

    return {
        "query": text(query),
        "params": values,
        "returning": returning
    }



# Used to execute a list of queries as dict
def execute_queries(conn, queries):
    result = None

    try:
        for q in queries:
            query = q["query"]
            params = q["params"]
            returning = q["returning"]
            
            db_result = None
            if params is not None :
                db_result = conn.execute(query, params)
            else :
                conn.execute(query)
                
            conn.commit()

            if returning:
                result = db_result.scalar()            
    except Exception as e:
        conn.rollback()

    return result



# Used to build an insert query and execute it
def build_execute_insert_query(conn, table_name, row=None, mapping={}, columns_to_add={}, returning=None):
    query = build_insert_query(table_name, row, mapping, columns_to_add, returning)
    return execute_queries(conn, [query])



# Used to insert each element of a list in a column in table
def insert_in_table_column_from_list(conn, table_name, column, list, return_mapping):
    mapping = {}
    for element in list: 
        mapping.update({element : build_execute_insert_query(conn, table_name, None, {}, {column : element}, return_mapping)})
    return mapping



# Used to retrieve all column names of a table in database
def get_column_names_from_table(conn, table_name):
    try:
        result = conn.execute(text(f"SELECT * FROM {table_name} LIMIT 0"))
        return list(result.keys())
    except Exception as e:
        print(f"Erreur lors de la récupération des colonnes : {e}")
        return []