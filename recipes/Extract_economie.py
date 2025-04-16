from utils import create_datasets_from_file_sheets, process_pib, pivot, columns_to_int, columns_to_float, columns_to_float, set_row_as_headers, delete_rows_by_index

datasets = [
    {
        "name": "Pib",
        "functions": [
            {
                "name" : process_pib,
                "args" : []
            },
            
        ]
    },
    {
        "name": "Inflation",
        "functions": [
            {
                "name" : set_row_as_headers,
                "args" : [2]
            },
            {
                "name" : delete_rows_by_index,
                "args" : [[0, 1, 2], 35]
            },
            {
                "name" : columns_to_int,
                "args" : [["Année"]]
            },
            {
                "name" : columns_to_float,
                "args" : [["Taux d'inflation"]]
            },
        ]
    },
    {
        "name": "Salaire_moyen",
        "functions": [
            {
                "name" : columns_to_int,
                "args" : []
            },
        ]
    },
    {
        "name": "Impot_moyen",
        "functions": [
            {
                "name" : columns_to_int,
                "args" : [["Année"]]
            },
            {
                "name" : columns_to_float,
                "args" : [["Impot"], 2]
            },
        ]
    },
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Economie.xlsx", datasets, [])