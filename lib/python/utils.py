def get_float_precision(df, float_cols):
    float_precision = {}
    for col in float_cols:
        non_null = df[col].dropna()
        if not non_null.empty:
            float_precision[col] = non_null.map(lambda x: len(str(x).split(".")[1]) if "." in str(x) else 0).max()
        else:
            float_precision[col] = 1
    return float_precision


