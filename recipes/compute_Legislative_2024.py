from utils import create_datasets_from_file_sheets

datasets = [
    {
        "name": "Taux_de_chomage",
        "functions": [
            {
                "name" : columns_to_int,
                "args" : [["Année"]]
            }
        ]
    },
    {
        "name": "Repartition_des_contrats",
        "functions": [
            {
                "name" : columns_to_int,
                "args" : []
            }
        ]
    },
    {
        "name": "Categorie_metiers",
        "functions": [
            {
                 "name" : process_category_metier,
                 "args" : []   
            },
            {
                 "name" : pivot,
                 "args" : ["Année"]   
            },
            {
                "name" : columns_to_int,
                "args" : []
            }
            
        ]
    },
    {
        "name": "Nombre_de_salarie",
        "functions": [
            {
                "name" : columns_to_int,
                "args" : []
            }
        ]
    },
    {
        "name": "Evolution_trimestrielle_emploi",
        "functions": [
            {
                "name" : process_evolution_trimestrielle_emploi,
                "args" : []
            },
            {
                "name" : rename_column,
                "args" : ["None", "Année"]
            },
            {
                "name" : columns_to_int,
                "args" : [["Année"]]
            }
        ]
    },
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Legislative.xlsx", datasets, [])
