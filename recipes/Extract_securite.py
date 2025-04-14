from utils import create_datasets_from_file_sheets, strip_headers, columns_to_int, pivot

datasets = [
    {
        "name": "Administration_penitentiaire",
        "functions": [
            {
                 "name" : pivot,
                 "args" : ["Année"]
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
        "functions": [
            {
                 "name" : columns_to_int,
                 "args" : [{"Année", "nombre", }]
            }
        ]
    },
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Securite.xlsx", datasets, [])
