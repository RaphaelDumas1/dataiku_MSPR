from utils import create_datasets_from_file_sheets, pivot_years, strip_headers, columns_to_int

datasets = [
    {
        "name": "Administration_penitentiaire",
        "functions": [
            {
                 "name" : pivot_years,
                 "args" : None
            },
            {
                 "name" : strip_headers,
                 "args" : []
            },
            {
                 "name" : columns_to_int,
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
