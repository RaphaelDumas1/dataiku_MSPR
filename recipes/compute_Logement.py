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
        "name": "Type_logement",
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
        "name": "Categorie_logement",
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
        "name": "Statut_occupation_logement",
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
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Emploi.xlsx", datasets, ["Categorie metiers"])

