from geenral import create_datasets_from_file_sheets
from other import pivot, add_columns, rename_columns,
from special import copy_years_range, extract_and_concat_to_original
from convert import convert_columns
from delete import delete_columns_in_list



instructions = [
    "Nombre_detranger" : [
        {
             "name" : convert_columns,
             "args" : [{
                 "Année" : "int",
                 "Nombre" : "int"
             }]
        },
        {
             "name" : rename_columns,
             "args" : [{"Nombre" : "etrangers"}]
        },
    ],
    "Taux_de_natalite" : [
        {
             "name" : convert_columns,
             "args" : [{
                 "Année" : "int",
             }]
        }
    ],
    "Taux_de_mortalite" : [
         {
             "name" : convert_columns,
             "args" : [{
                 "Année" : "int",
             }]
        }
    ],
    "Population" : [
        {
             "name" : convert_columns,
             "args" : [{
                 "Année" : "int",
                 "Nombre" : "int",
             }]
        }
        {
             "name" : rename_columns,
             "args" : [{"Nombre" : "population"}]
        },
    ],
    "Repartition_age" : [
        {
             "name" : convert_columns,
             "args" : [{
                 "Année" : "int",
             }]
        }
    ]
    {
        "name": ,
        "functions": 
    },
    # {
    #    "name": "Quotient_familiale",
    #    "functions": [
    #        {
    #             "name" : extract_and_concat_to_original,
    #             "args" : [(801, 1603), (1604, 2802)]
    #        },
    #        {
    #             "name" : delete_columns_in_list,
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
        "name": ,
        "functions": 
    },
    {
        "name": ,
        "functions": 
    },
    {
        "name": ,
        "functions": 
    },
    {
        "name": ,
        "functions": [
            
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
            {
                 "name" : complete_with_inteprolate,
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
            {
                 "name" : complete_with_inteprolate,
                 "args" : []
            },
            {
                 "name" : rename_columns,
                 "args" : [{"nombre" : "immigres"}]
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
            {
                 "name" : complete_with_inteprolate,
                 "args" : []
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
            {
                 "name" : complete_with_inteprolate,
                 "args" : []
            },
        ]
    },
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Demographie.xlsx", datasets, ["Quotient familiale"])
