from general import create_datasets_from_file_sheets
from special import process_evolution_trimestrielle_emploi
from other import pivot, rename_columns, set_row_as_headers
from convert import convert_columns 
from delete import delete_rows_by_index, delete_columns_not_in_list
from utils import make_list_values_unique

instructions = {
    "Taux_de_chomage" : [
        {
            "name" : rename_columns,
            "args" : [{
                "Taux" : "taux_chomage"
            }]
        },
        {
            "name" : convert_columns,
            "args" : [{
                "Année" : "int"
            }]
        },
    ],
    "Repartition_des_contrats" : [
        {
            "name" : rename_columns,
            "args" : [{
                "CDI" : "nombre_cdi",
                "CDD" :  "nombre_cdd"
            }]
        },
        {
            "name" : convert_columns,
            "args" : ["int"]
        }
    ],
    "Categorie_metiers" : [
        {
            "name" : set_row_as_headers,
            "args" : [0, make_list_values_unique]   
        },
        {
            "name" : delete_rows_by_index,
            "args" : [[0, 1], 10]   
        },
        {
            "name" : rename_columns,
            "args" : [{
                "None_2" : "2010",
                "None_4" : "2015",
                "None_6" : "2021"
            }]
        },
        {
            "name" : delete_columns_not_in_list,
            "args" : [["None", "2010", "2015", "2021"]]   
        },
        {
            "name" : pivot,
            "args" : ["annee"]   
        },
        {
            "name" : rename_columns,
            "args" : [{
                "Agriculteurs exploitants" : "nombre_agriculteurs",
                "Artisans, commerçants, chefs entreprise" :  "nombre_artisans",
                "Cadres et professions intellectuelles supérieures" :  "nombre_cadres",
                "Professions intermédiaires" :  "nombre_professions_intermediaires",
                "Employés" :  "nombre_employes",
                "Ouvriers" :  "nombre_ouvriers",
                "Retraités" :  "nombre_retraites",
                "Autres personnes sans activité professionnelle" :  "nombre_sans_emplois",
            }]
        },
        {
            "name" : convert_columns,
            "args" : [{
                "annee" : "int",
                'nombre_agriculteurs' : "int",
                "nombre_artisans" : "int",
                "nombre_cadres" : "int",
                "nombre_professions_intermediaires" : "int",
                "nombre_employes" : "int",
                "nombre_ouvriers" : "int",
                "nombre_retraites" : "int",
                "nombre_sans_emplois" : "int",
                "Total" : "int"
            }]
        }
    ],
    "Nombre_de_salarie" : [
        {
            "name" : convert_columns,
            "args" : [{
                "Année" : "int",
                "Nombre de salarie" : "int",
            }]
        }
    ],
    #"Evolution_trimestrielle_emploi" : [
    #    {
    #        "name" : process_evolution_trimestrielle_emploi,
    #         "args" : []
    #    },
    #    {
    #        "name" : rename_columns,
    #        "args" : [{"None" : "annee"}]
    #    },
    #    {
    #        "name" : convert_columns,
    #        "args" : [{
    #            "annee" : "int",
    #        }]
    #    }
}



create_datasets_from_file_sheets("MSPR - Emploi.xlsx", instructions)