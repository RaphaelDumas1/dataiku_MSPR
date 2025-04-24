from general import create_datasets_from_file_sheets
from convert import convert_columns 
from other import pivot, rename_columns



instructions = {
    "Administration_penitentiaire" : [
        {
            "name" : pivot,
            "args" : ["annee"]
        },
        {
            "name" : rename_columns,
            "args" : [{
                "Personnes prises en charge" : "nombre_pris_en_charge",
                "Mesures en cours" : "nombre_en_cours",
                "Sursis1" : "nombre_sursis",
                "Travail d'intérêt général (TIG)2" : "nombre_travaux_interet_general",
                "Libérations conditionnelles3" : "nombre_liberations_conditionnelles",
                "Autres mesures" : "autres"
            }]
        }, 
        {
            "name" : convert_columns,
            "args" : ["int"]
        },
    ],
    "Delinquance" : [
        {
            "name" : convert_columns,
            "args" : [{
                "Année" : "int", 
                "nombre" : "int",
                "insee_pop": "int",
                "insee_pop_millesime": "int",
                "insee_log" : "int",
                "insee_log_millesime" : "int"
            }]
        }
    ]
}



create_datasets_from_file_sheets("MSPR - Securite.xlsx", instructions)