from utils import create_datasets_from_file_sheets, pivot, columns_to_int, columns_to_float

datasets = [
    {
        "name": "Logement",
        "functions": [
            {
                 "name" : pivot,
                 "args" : ["Année"]
            },
            {
                 "name" : columns_to_int,
                 "args" : [["Année", "Nombre de logements"]]
            },
            {
                 "name" : columns_to_float,
                 "args" : [["Année", "Nombre de logements"]]
            }
        ]
    },
    {
        "name": "Type_logement",
        "functions": [
            {
                 "name" : pivot,
                 "args" : ["Année"]
            },
            {
                 "name" : columns_to_int,
                 "args" : [["Année"]]
            }
        ]
    },
    {
        "name": "Categorie_logement",
        "functions": [
            {
                 "name" : pivot,
                 "args" : ["Année"]
            },
            {
                 "name" : columns_to_int,
                 "args" : [["Année"]]
            }
        ]
    },
    {
        "name": "Statut_occupation_logement",
        "functions": [
            {
                 "name" : pivot,
                 "args" : ["Année"]
            },
            {
                 "name" : columns_to_int,
                 "args" : [["Année"]]
            }
        ]
    },
    {
        "name": "Composition_menage",
       "functions": [
            {
                 "name" : pivot,
                 "args" : ["Année"]
            },
           {
                 "name" : columns_to_int,
                 "args" : [["Année"]]
            }
        ]
    },
    {
        "name": "Nombre_enfant",
        "functions": [
            {
                 "name" : pivot,
                 "args" : ["Année"]
            },
            {
                 "name" : columns_to_int,
                 "args" : [["Année"]]
            }
        ]
    }
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Logement.xlsx", datasets, [])

