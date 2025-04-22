from utils import create_datasets_from_file_sheets, delete_rows_where_equal, columns_to_int, columns_to_float, rename_columns, complete_with_inteprolate

datasets = [
    {
        "name": "Esperance_de_vie",
        "functions": [
            {
                "name" : rename_columns,
                "args" : [
                    {
                        "Espérance de vie sans incapacité femme" : "femmes_sans_incapacite",
                        "Espérance de vie femme" : "femme_total",
                        "Espérance de vie sans incapacité homme" : "homme_sans_incapacite",
                        "Espérance de vie homme" : "homme_total"
                    }
                ]
            
            },
            {
                "name" : delete_rows_where_equal,
                "args" : ["femmes_sans_incapacite", "nd"]
            
            },
            {
                "name" : columns_to_int,
                "args" : [["Année"]]
            
            },
            {
                "name" : columns_to_float,
                "args" : [["femmes_sans_incapacite", "femme_total", "homme_sans_incapacite", "homme_total"], 1]
            
            },
            {
                "name" : complete_with_inteprolate,
                "args" : []
            
            },
        ]
    },
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Sante.xlsx", datasets, [])