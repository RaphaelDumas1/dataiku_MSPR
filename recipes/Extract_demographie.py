from utils import create_datasets_from_file_sheets, pivot, copy_years_range, columns_to_int, add_columns, extract_and_concat_to_original, columns_to_string, delete_columns_by_name, rename_columns, complete_with_inteprolate

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
    # {
    #    "name": "Quotient_familiale",
    #    "functions": [
    #        {
    #             "name" : extract_and_concat_to_original,
    #             "args" : [(801, 1603), (1604, 2802)]
    #        },
    #        {
    #             "name" : delete_columns_by_name,
    #             "args" : [['Numéro département', 'Nom département', 'Numéro région', 'Nom région', "Lieu résidence"]]
    #        },
    #        {
    #             "name" : columns_to_int,
    #             "args" : [["Année", "Nombre foyers NDUR", "Nombre personnes NDUR", "Montant total NDUR", "Nombre foyers NDURPAJE",
    #                       "Nombre personnes NDURPAJE", "Montant total NDURPAJE", "Nombre foyers NDUREJ", "Nombre personnes NDUREJ",
    #                       "Montant total NDUREJ", "Nombre foyers NDURAL", "Nombre personnes NDURAL", "Montant total NDURAL", 
    #                       "Nombre foyers NDURINS", "Nombre personnes NDURINS", "Montant total NDURINS"]]
    #        },
    #    ]
    #},
    {
        "name": "Taux_de_natalite",
        "functions": [
            {
                 "name" : columns_to_int,
                 "args" : [["Année"]]
            },
            {
                 "name" : complete_with_inteprolate,
                 "args" : []
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
                 "args" : ["Année"]
            },
            {
                 "name" : copy_years_range,
                 "args" : []
            },
            {
                 "name" : columns_to_int,
                 "args" : [["Année"]]
            },
        ]
    },
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Demographie.xlsx", datasets, ["Quotient familiale"])
