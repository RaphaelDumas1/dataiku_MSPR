from general import create_datasets_from_file_sheets
from special import process_category_metier, process_evolution_trimestrielle_emploi
from other import pivot, rename_columns
from convert import convert_columns  , delete_rows_by_index, make_unique, set_row_as_headers, complete_with_inteprolate  

datasets = [
    {
        "name": "Taux_de_chomage",
        "functions": [
            {
                "name" : columns_to_int,
                "args" : [["Année"]]
            }
        ]
    },
    {
        "name": "Repartition_des_contrats",
        "functions": [
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
        "name": "Categorie_metiers",
        "functions": [
            {
                 "name" : process_category_metier,
                 "args" : []   
            },
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
        "name": "Nombre_de_salarie",
        "functions": [
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
    #{
    #    "name": "Evolution_trimestrielle_emploi",
    #    "functions": [
    #        {
    #            "name" : process_evolution_trimestrielle_emploi,
    #            "args" : []
    #        },
    #        {
    #            "name" : rename_columns,
    #            "args" : [{"None" : "Année"}]
    #        },
    #        {
    #            "name" : columns_to_int,
    #            "args" : [["Année"]]
    #        }
    #    ]
    #},
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Emploi.xlsx", datasets, ["Evolution trimestrielle emploi "])

