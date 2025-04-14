from utils import create_datasets_from_file_sheets, pivot_years, column_from_float_to_string, strip_headers

datasets = [
    {
        "name": "Administration_penitentiaire",
        "functions": [
            {
                 "name" : pivot_years,
                 "args" : None
            },
            {
                 "name" : column_from_float_to_string,
                 "args" : ["Année"]
            },
            {
                 "name" : strip_headers,
                 "args" : []
            }
        ]
    },
    {
        "name": "Delinquance",
        "functions": []
    },
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Securite.xlsx", datasets, [])
