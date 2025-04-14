from utils import run, process, process_category_metier, pivot_years, to_int

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

run("MSPR", "aPmnwurD", "MSPR - Emploi.xlsx", ["Categorie metiers"], datasets)

