from utils import create_datasets_from_file_sheets

datasets = [
    {
        "name": "Logement",
        "functions": [
            {
                 "name" : pivot_years,
                 "args" : None
            },
            {
                 "name" : column_from_float_to_string,
                 "args" : ["Année"]
            }
        ]
    },
    {
        "name": "Repartition_des_contrats",
        "functions": [
            
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
                 "name" : pivot_years,
                 "args" : []   
            },
            
        ]
    },
    {
        "name": "Nombre_de_salarie",
        "functions": []
    },
    {
        "name": "Evolution_trimestrielle_emploi",
        "functions": []
    },
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Emploi.xlsx", datasets, ["Categorie metiers"])

