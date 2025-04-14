from utils import run, process, process_category_metier, pivot_years

run("MSPR", "aPmnwurD", "MSPR - Emploi.xlsx", [])

datasets = [
    {
        "input": "Taux_de_chomage",
        "output": "Taux_de_chomage",
        "functions": []
    },
    {
        "input": "Repartition_des_contrats",
        "output": "Repartition_des_contrats",
        "functions": []
    },
    {
        "input": "Categorie_metiers",
        "output": "Categorie_metiers",
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
        "input": "Nombre_de_salarie",
        "output": "Nombre_de_salarie",
        "functions": []
    },
]
process(datasets)

