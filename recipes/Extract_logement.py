from utils import create_datasets_from_file_sheets, pivot, column_from_float_to_string, columns_to_int

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
                 "args" : ["Année"]
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
                 "args" : ["Année"]
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
                 "args" : ["Année"]
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
                 "args" : ["Année"]
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
                 "args" : ["Année"]
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
                 "args" : ["Année"]
            }
        ]
    }
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Emploi.xlsx", datasets, [])

