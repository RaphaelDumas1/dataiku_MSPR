from utils import run, process, process_category_metier, pivot_years

datasets = [
    {
        "name": "Taux_de_chomage",
        "functions": []
    },
    {
        "name": "Repartition_des_contrats",
        "functions": []
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
]

run("MSPR", "aPmnwurD", "MSPR - Emploi.xlsx", [], datasets)

