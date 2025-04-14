from utils import create_datasets_from_file_sheets, delete_where_equal

datasets = [
    {
        "name": "Esperance_de_vie",
        "functions": [
            {
                "name" : delete_where_equal,
                "args" : ["Espérance de vie sans incapacité femme", "nd"]
            
            }
        ]
    },
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Sante.xlsx", datasets, [])