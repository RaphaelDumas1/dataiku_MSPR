from general import create_datasets_from_file_sheets
from special import process_category_metier, process_evolution_trimestrielle_emploi
from other import pivot, rename_columns, set_row_as_headers
from convert import convert_columns 
from delete import delete_rows_by_index

datasets = {
    "Taux_de_chomage" : [
        {
            "name" : columns_to_int,
            "args" : [["Année"]]
        }
    ],
    "Repartition_des_contrats" : [
        {
            "name" : columns_to_int,
            "args" : []
        }
    ],
    "Categorie_metiers" : [
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
        }
    ],
    "Nombre_de_salarie" : [
        {
            "name" : columns_to_int,
            "args" : []
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

