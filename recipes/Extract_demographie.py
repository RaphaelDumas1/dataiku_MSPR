from utils import create_datasets_from_file_sheets, pivot, copy_years_range, columns_to_int, add_columns

datasets = [
    {
        "name": "Nombre_detranger",
        "functions": [
            {
                 "name" : columns_to_int,
                 "args" : []
            },
        ]
    },
    {
        "name": "Quotient_familiale",
        "functions": []
    },
    {
        "name": "Taux_de_natalite",
        "functions": [
            {
                 "name" : columns_to_int,
                 "args" : [["Année"]]
            },
        ]
    },
    {
        "name": "Taux_de_mortalite",
        "functions": [
            {
                 "name" : columns_to_int,
                 "args" : [["Année"]]
            },
        ]
    },
    {
        "name": "Population",
        "functions": [
            {
                 "name" : columns_to_int,
                 "args" : []
            },
        ]
    },
    {
        "name": "Repartition_age",
        "functions": [
            {
                 "name" : columns_to_int,
                 "args" : [["Année"]]
            },
        ]
    },
    {
        "name": "Repartition_sexe",
        "functions": [
            {
                 "name" : add_columns,
                 "args" : ["Population femme", "Population homme", "Population totale"]
            },
            {
                 "name" : columns_to_int,
                 "args" : []
            },
        ]
    },
    {
        "name": "Nombre_dimmigre",
        "functions": [
            {
                 "name" : columns_to_int,
                 "args" : []
            },
        ]
    },
    {
        "name": "Taux_de_pauvrete",
        "functions": []
    },
    {
        "name": "Evolution_population",
        "functions": [
            {
                 "name" : pivot,
                 "args" : [["Année"]]
            },
            {
                 "name" : copy_years_range,
                 "args" : None
            },
        ]
    },
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Demographie.xlsx", datasets, [])
