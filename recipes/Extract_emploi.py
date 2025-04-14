from utils import create_datasets_from_file_sheets, process_category_metier, pivot, columns_to_int

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
        "functions": []
    },
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Emploi.xlsx", datasets, [])

