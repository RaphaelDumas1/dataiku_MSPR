from utils import create_datasets_from_file_sheets, process, process_category_metier, pivot_years, to_int

datasets = [
    {
        "name": "Taux_de_chomage",
        "functions": [
            {
                "name" : to_int,
                "args" : [["Année"]]
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

