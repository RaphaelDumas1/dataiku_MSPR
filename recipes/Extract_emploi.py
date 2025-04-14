from utils import create_datasets_from_file_sheets, process_category_metier, pivot, columns_to_int, process_evolution_trimestrielle_emploi, rename_column

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
       
        ]
    },
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Emploi.xlsx", datasets, [])

