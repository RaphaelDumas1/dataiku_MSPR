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
             "name" : convert_columns,
             "args" : [{
                 "Année" : 'int',
                 "Maisons" : 'int',
                 "Appartements" : 'int',
                 "Autres logements" : 'int',
                 "Total" : "int"
             }]
        }
    ],
    "Categorie_logement" : [
        {
             "name" : pivot,
             "args" : ["Année"]
        },
        {
             "name" : convert_columns,
             "args" : [{
                 "Année" : 'int',
                 "Résidences principales" : 'int',
                 "Résid. secondaires et log. occasionnels" : 'int',
                 "Logements vacants" : 'int',
                 "Total" : "int"
             }]
        }
    ],
    "Statut_occupation_logement" : [
        {
             "name" : pivot,
             "args" : ["Année"]
        },
        {
             "name" : convert_columns,
             "args" : [{
                 "Année" : 'int',
                 "Propriétaires" : 'int',
                 "Locataires" : 'int',
                 "- dont locataires d'un logement HLM loué vide" : 'int',
                 "Logés gratuitement" : "int",
                 "Ensemble" : "int"
             }]
        }
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
             "name" : convert_columns,
             "args" : [{
                 "Année" : 'int',
                 "Ménages d'une personne" : 'int',
                 "- hommes seuls" : 'int',
                 "- femmes seules" : 'int',
                 "Autres ménages sans famille" : "int",
                 "Ménages avec famille(s) dont la famille principale est" : "int",
                 "- un couple sans enfant" : 'int',
                 "- un couple avec enfant(s)" : 'int',
                 "- une famille monoparentale" : 'int',
                 "Ensemble" : 'int',
             }]
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
             "name" : convert_columns,
             "args" : [{
                 "Année" : 'int',
                 "Aucun enfant : 'int',
                 "1 enfant" : 'int',
                 "2 enfants" : 'int',
                 "3 enfants" : "int",
                 "4 enfants ou plus" : "int"
             }]
        },
    ]
}
 


create_datasets_from_file_sheets("MSPR - Logement.xlsx", instructions)

