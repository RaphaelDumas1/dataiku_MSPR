from geenral import create_datasets_from_file_sheets
from other import pivot, create_column_by_adding_columns_values, rename_columns,
from special import copy_years_range, extract_and_concat_to_original
from convert import convert_columns
from delete import delete_columns_in_list



instructions = {
    "Nombre_detranger" : [
        {
             "name" : convert_columns,
             "args" : [{
                 "Année" : "int",
                 "Nombre" : "int"
             }]
        },
        {
             "name" : rename_columns,
             "args" : [{"Nombre" : "etrangers"}]
        },
    ],
    "Taux_de_natalite" : [
        {
             "name" : convert_columns,
             "args" : [{
                 "Année" : "int",
             }]
        }
    ],
    "Taux_de_mortalite" : [
         {
             "name" : convert_columns,
             "args" : [{
                 "Année" : "int",
             }]
        }
    ],
    "Population" : [
        {
             "name" : convert_columns,
             "args" : [{
                 "Année" : "int",
                 "Nombre" : "int",
             }]
        }
        {
             "name" : rename_columns,
             "args" : [{"Nombre" : "population"}]
        },
    ],
    "Repartition_age" : [
        {
             "name" : convert_columns,
             "args" : [{
                 "Année" : "int",
             }]
        }
    ],
    "Repartition_sexe" : [
        {
             "name" : create_column_by_adding_columns_values,
             "args" : [["Population femme", "Population homme"], "Population totale"]
        },
        {
             "name" : convert_columns,
             "args" : [{
                 "Année" : "int",
                 "Population femme" : 'int',
                 "Population femme" : 'int'
                 "Population totale": 'int'
             }]
        }
    ],
    "Nombre_dimmigre" : [
        {
             "name" : convert_columns,
             "args" : [{
                 "Année" : "int",
                 "Nombre" : "int",
             }]
        },
        {
             "name" : rename_columns,
             "args" : [{"Nombre" : "immigres"}]
        },
    ],
    "Taux_de_pauvrete" : [
        {
             "name" : convert_columns,
             "args" : [{
                 "Année" : "int",
             }]
        }
    ],
    "Evolution_population" : [
        {
             "name" : pivot,
             "args" : ["Année"]
        },
        {
             "name" : copy_years_range,
             "args" : []
        },
        {
             "name" : convert_columns,
             "args" : [{
                 "Année" : "int",
             }]
        }
    ],
    #"Quotient_familiale" : [
    #    {
    #         "name" : extract_and_concat_to_original,
    #         "args" : [(801, 1603), (1604, 2802)]
    #    },
    #    {
    #         "name" : delete_columns_in_list,
    #         "args" : [['Numéro département', 'Nom département', 'Numéro région', 'Nom région', "Lieu résidence"]]
    #    },
    #    {
    #         "name" : columns_to_int,
    #         "args" : [["Année", "Nombre foyers NDUR", "Nombre personnes NDUR", "Montant total NDUR", "Nombre foyers NDURPAJE",
    #                   "Nombre personnes NDURPAJE", "Montant total NDURPAJE", "Nombre foyers NDUREJ", "Nombre personnes NDUREJ",
    #                   "Montant total NDUREJ", "Nombre foyers NDURAL", "Nombre personnes NDURAL", "Montant total NDURAL", 
    #                   "Nombre foyers NDURINS", "Nombre personnes NDURINS", "Montant total NDURINS"]]
    #    },
    #]
}



create_datasets_from_file_sheets("MSPR - Demographie.xlsx", datasets, ["Quotient familiale"])
