from utils import create_datasets_from_file_sheets, pivot, copy_years_range, columns_to_int, add_columns, extract_and_concat_to_original, columns_to_string

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
        "functions": [
            {
                 "name" : extract_and_concat_to_original,
                 "args" : [(802, 1604), (1606, 2804)]
            },
            {
                 "name" : columns_to_int,
                 "args" : [["Année", "Nombre foyers NDUR", "Nombre personnes NDUR", "Montant total NDUR", "Nombre foyers NDURPAJE",
                           "Nombre personnes NDURPAJE", "Montant total NDURPAJE", "Nombre foyers NDUREJ", "Nombre personnes NDUREJ",
                           "Montant total NDUREJ", "Nombre foyers NDURAL", "Nombre personnes NDURAL", "Montant total NDURAL", 
                           "Nombre foyers NDURINS", "Nombre personnes NDURINS", "Montant total NDURINS"]]
            },
            {
                 "name" : columns_to_string,
                 "args" : [["Numéro département", "Numéro région"]]
            },
        ]
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
        "functions": [
            {
                 "name" : columns_to_int,
                 "args" : [["Année"]]
            },
        ]
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
                 "args" : []
            },
        ]
    },
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Demographie.xlsx", datasets, [])
