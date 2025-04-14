from utils import create_datasets_from_file_sheets, delete_where_equal, columns_to_int, columns_to_float

datasets = [
    {
        "name": "Esperance_de_vie",
        "functions": [
            {
                "name" : delete_where_equal,
                "args" : ["Espérance de vie sans incapacité femme", "nd"]
            
            },
            {
                "name" : columns_to_int,
                "args" : [["Année"]]
            
            },
            {
                "name" : columns_to_float,
                "args" : [["Espérance de vie femme", "Espérance de vie homme"], 1]
            
            }
        ]
    },
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Sante.xlsx", datasets, [])