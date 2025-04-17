from utils import create_datasets_from_file_sheets, strip_headers, columns_to_int, pivot, complete_with_inteprolate

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
                 "name" : complete_with_inteprolate,
                 "args" : []
            },
            {
                 "name" : columns_to_int,
                 "args" : []
            }, 
        ]
    },
    {
        "name": "Delinquance",
        "functions": [
            {
                 "name" : columns_to_int,
                 "args" : [{"Année", "nombre", "insee_pop", "insee_pop_millesime", "insee_log", "insee_log_millesime"}]
            }
        ]
    },
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Securite.xlsx", datasets, [])
