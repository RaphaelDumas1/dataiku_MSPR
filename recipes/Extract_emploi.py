from general import create_datasets_from_file_sheets
from special import process_categorie_metier, process_evolution_trimestrielle_emploi
from other import pivot, rename_columns, set_row_as_headers
from convert import convert_columns 
from delete import delete_rows_by_index

instructions = {
    "Taux_de_chomage" : [
        {
            "name" : convert_columns,
            "args" : [{
                "Année" : 'int'
            }]
        }
    ],
    "Repartition_des_contrats" : [
        {
            "name" : convert_columns,
            "args" : [{
                "Année" : 'int',
                "CDI" : 'int',
                "CDD" : 'int'
            }]
        }
    ],
    "Categorie_metiers" : [
        {
             "name" : process_categorie_metier,
             "args" : []   
        },
        {
             "name" : pivot,
             "args" : ["Année"]   
        },
        {
            "name" : convert_columns,
            "args" : [{
                "Année" : 'int',
                'agriculteurs exploitants' : 'int',
                "artisans, commercants, chefs entreprise" : 'int',
                "cadres et professions intellectuelles superieures" : 'int',
                "professions intermediaires": 'int',
                "employes" : 'int',
                "ouvriers" : 'int',
                "retraites" : 'int',
                "autres personnes sans activite professionnelle" : 'int',
                "total" : 'int'
            }]
        }
    ],
    "Nombre_de_salarie" : [
        {
            "name" : convert_columns,
            "args" : [{
                "Année" : 'int',
                "nombre" : 'int',
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
    #        "args" : [{"None" : "Année"}]
    #    },
    #    {
    #        "name" : columns_to_int,
    #        "args" : [["Année"]]
    #    }
}

create_datasets_from_file_sheets("MSPR - Emploi.xlsx", instructions)

