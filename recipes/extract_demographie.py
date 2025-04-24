from general import create_datasets_from_file_sheets
from other import pivot, rename_columns, create_column_by_adding_columns_values
from special import process_evolution_population, process_quotient_familiale
from convert import convert_columns
from delete import delete_columns_in_list



instructions = {
    "Nombre_detranger" : [
        {
            "name" : rename_columns,
            "args" : [{"Nombre" : "nombre_etranger"}]
        },
        {
            "name" : convert_columns,
            "args" : ["int"]
        }
    ],
    "Taux_de_natalite" : [
        {
            "name" : rename_columns,
            "args" : [{
                "Année" : "annee",
                "Taux de natalite" : "taux_natalite"
            }]
        },
        {
            "name" : convert_columns,
            "args" : [{
                "annee" : "int",
            }]
        }
    ],
    "Taux_de_mortalite" : [
        {
            "name" : rename_columns,
            "args" : [{
                "Année" : "annee",
                "Taux de deces" : "taux_mortalite"
            }]
        },
        {
            "name" : convert_columns,
            "args" : [{
                "annee" : "int",
            }]
        }
    ],
    "Population" : [
        {
            "name" : rename_columns,
            "args" : [{
                "Nombre" : "population"
            }]
        },
        {
            "name" : convert_columns,
            "args" : ["int"]
        }
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
            "name" : rename_columns,
            "args" : [{
                "Année" : "annee",
                "Population homme" : "nombre_hommes",
                "Population femme" : "nombre_femmes"
            }]
        },
        {
            "name" : create_column_by_adding_columns_values,
            "args" : [["nombre_hommes", "nombre_femmes"], "Population totale"]
        },
        {
            "name" : convert_columns,
            "args" : ["int"]
        }
    ],
    "Nombre_dimmigre" : [
        {
            "name" : rename_columns,
            "args" : [{"Nombre" : "nombre_immigrant"}]
        },
        {
            "name" : convert_columns,
            "args" : ["int"]
        }
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
            "args" : ["annee"]
        },
        {
            "name" : process_evolution_population,
            "args" : []
        },
        {
            "name" : convert_columns,
            "args" : [{
                "annee" : "int",
            }]
        }
    ],
    #"Quotient_familiale" : [
    #    {
    #         "name" : process_quotient_familiale,
    #         "args" : [(801, 1603), (1604, 2802)]
    #    },
    #    {
    #         "name" : delete_columns_in_list,
    #         "args" : [['Numéro département', 'Nom département', 'Numéro région', 'Nom région', "Lieu résidence"]]
    #    },
    #    {
    #         "name" : convert_columns,
    #         "args" : ["int"]
    #    }
    #]
}



create_datasets_from_file_sheets("MSPR - Demographie.xlsx", instructions)