from general import create_datasets_from_file_sheets
from special import process_categorie_metier, process_evolution_trimestrielle_emploi
from other import pivot, rename_columns, set_row_as_headers
from convert import convert_columns 
from delete import delete_rows_by_index

datasets = {
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
            "name" : columns_to_int,
            "args" : []
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

