from general import create_datasets_from_file_sheets
from other import pivot, rename_columns
from convert import convert_columns 

instructions = {
    "Logement" : [
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
    ],
    "Type_logement" : [
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
    ],
    "Categorie_logement" : [
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

