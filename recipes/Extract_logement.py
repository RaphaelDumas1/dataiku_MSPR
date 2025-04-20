from utils import create_datasets_from_file_sheets, pivot, columns_to_int, columns_to_float, complete_with_inteprolate, rename_columns

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
                 "args" : [["Part des résidences principales (%)", "Part des rés. secondaires (yc log. occasionnels) (%)", "Part des logements vacants (%)"]]
            },
            {
                 "name" : complete_with_inteprolate,
                 "args" : []
            },
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
                 "args" : []
            },
            {
                 "name" : complete_with_inteprolate,
                 "args" : []
            },
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
                 "args" : []
            },
            {
                 "name" : complete_with_inteprolate,
                 "args" : []
            },
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
                 "args" : []
            },
            {
                 "name" : complete_with_inteprolate,
                 "args" : []
            },
            {
                 "name" : rename_columns,
                 "args" : [{"ensemble" : "ensemble_logements"}]
            },
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
                 "args" : []
            },
           {
                 "name" : complete_with_inteprolate,
                 "args" : []
            },
           {
                 "name" : rename_columns,
                 "args" : [{"ensemble" : "ensemble_menages"}]
            },
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
                 "args" : []
            },
            {
                 "name" : complete_with_inteprolate,
                 "args" : []
            },
        ]
    }
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Logement.xlsx", datasets, [])

