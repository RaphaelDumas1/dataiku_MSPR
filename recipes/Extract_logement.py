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
             "name" : convert_columns,
             "args" : [{
                 "Année" : 'int',
                 "Nombre de logements" : 'int',
                 "Part des résidences principales (%)" : 'decimal_1',
                 "Part des rés. secondaires (yc log. occasionnels) (%)" : "decimal_1",
                 "Part des logements vacants (%)" : "decimal_1"
             }]
        }
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
    ],
    "Statut_occupation_logement" : [
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
    ],
    "Composition_menage" : [
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
    ],
    "Nombre_enfant" : [
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
 


create_datasets_from_file_sheets("MSPR - Logement.xlsx", instructions)

