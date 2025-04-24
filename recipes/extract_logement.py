from general import create_datasets_from_file_sheets
from other import pivot, rename_columns
from convert import convert_columns 



instructions = {
    "Logement" : [
        {
            "name" : pivot,
            "args" : ["annee"]
        },
        {
            "name" : convert_columns,
            "args" : [{
                "annee" : "int",
                "Nombre de logements" : "int",
                "Part des résidences principales (%)" : "decimal_1",
                "Part des rés. secondaires (yc log. occasionnels) (%)" : "decimal_1",
                "Part des logements vacants (%)" : "decimal_1"
            }]
        }
    ],
    "Type_logement" : [
        {
            "name" : pivot,
            "args" : ["annee"]
        },
        {
            "name" : rename_columns,
            "args" : [{
                "Maisons" : "nombre_maisons",
                "Appartements" : "nombre_appartements",
                "Autres logements" : "nombre_autres",
            }]
        },
        {
            "name" : convert_columns,
            "args" : ["int"]
        }
    ],
    "Categorie_logement" : [
        {
            "name" : pivot,
            "args" : ["annee"]
        },
        {
            "name" : rename_columns,
            "args" : [{
                "Résidences principales" : "nombre_residences_principales",
                "Résid. secondaires et log. occasionnels" : "nombre_residences_secondaires",
                "Logements vacants" : "nombre_logements_vacants"
            }]
        },
        {
            "name" : convert_columns,
            "args" : ["int"]
        }
    ],
    "Statut_occupation_logement" : [
        {
            "name" : pivot,
            "args" : ["annee"]
        },
        {
            "name" : rename_columns,
            "args" : [{
                "Propriétaires" : "nombre_proprietaires",
                "Locataires" : "nombre_locataires",
                "- dont locataires d'un logement HLM loué vide" : "nombre_hlm",
                "Logés gratuitement" : "nombre_logements_gratuit",
                "Ensemble" : "ensemble_logements"
            }]
        },
        {
            "name" : convert_columns,
            "args" : ["int"]
        },
    ],
    "Composition_menage" : [
        {
            "name" : pivot,
            "args" : ["annee"]
        },
        {
            "name" : rename_columns,
            "args" : [{
                "Ensemble" : "ensemble_menages",
                "- hommes seuls" : "homme_seul",
                "- femmes seules" : "femme_seule",
                "- un couple avec enfant(s)" : "couple_avec_enfant",
                "- un couple sans enfant" : "couple_sans_enfant",
                "- une famille monoparentale" : "famille_monoparentale",
            }]
        },
        {
            "name" : convert_columns,
            "args" : ["int"]
        },
    ],
    "Nombre_enfant" : [
        {
            "name" : pivot,
            "args" : ["annee"]
        },
        {
            "name" : rename_columns,
            "args" : [{
                "Aucun enfant" : "sans_enfant",
                "1 enfant" : "un",
                "2 enfants" : "deux",
                "3 enfants" : "trois",
                "4 enfants ou plus" : "quatre_et_plus"
            }]
        },
        {
            "name" : convert_columns,
            "args" : ["int"]
        },
    ]
}



create_datasets_from_file_sheets("MSPR - Logement.xlsx", instructions)