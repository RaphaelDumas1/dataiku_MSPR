def get_float_precision(df, float_cols):
    float_precision = {}
    for col in float_cols:
        non_null = df[col].dropna()
        if not non_null.empty:
            float_precision[col] = non_null.map(lambda x: len(str(x).split(".")[1]) if "." in str(x) else 0).max()
        else:
            float_precision[col] = 1
    return float_precision




# Used to make each element of a list unique by adding a number at the end of it to prevent duplicates   
def make_list_values_unique(list):
    seen = {}
    result = []
    for values in list:
        values = str(values).strip()
        if values not in seen:
            seen[values] = 1
            result.append(values)
        else:
            count = seen[values]
            new_values = f"{values}_{count}"
            while new_values in seen:
                count += 1
                new_h = f"{values}_{count}"
            seen[values] = count + 1
            seen[new_values] = 1
            result.append(new_values)
    return result 
