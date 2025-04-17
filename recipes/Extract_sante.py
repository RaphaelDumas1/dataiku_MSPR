from utils import create_datasets_from_file_sheets, delete_where_equal, columns_to_int, columns_to_float, rename_columns

datasets = [
    {
        "name": "Esperance_de_vie",
        "functions": [
            {
                "name" : delete_where_equal,
                "args" : ["Espérance de vie sans incapacité femme", "nd"]
            
            },
            {
                "name" : rename_columns,
                "args" : [{
                    "Espérance de vie sans incapacité femme" : "femmes_sans_incapacite",
                    "Espérance de vie femme" : "femme_total",
                    "Espérance de vie sans incapacité homme" : "homme_sans_incapacite",
                    "Espérance de vie homme" : "homme_total"
                }]
            
            },
            {
                "name" : columns_to_int,
                "args" : [["Année"]]
            
            },
            {
                "name" : columns_to_float,
                "args" : [["femmes_sans_incapacite", "femme_total", "homme_sans_incapacite", "homme_total"], 1]
            
            },
            
        ]
    },
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Sante.xlsx", datasets, [])