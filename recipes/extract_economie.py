from general import create_datasets_from_file_sheets
from other import pivot, set_row_as_headers, rename_columns
from convert import convert_columns 
from delete import delete_rows_by_index



def clean_pib_headers(columns):
    return columns.astype(str).str.strip().str.replace(" \(r\)", "", regex=True)



instructions = {
    "Pib" : [
        {
            "name" : set_row_as_headers,
            "args" : [1, clean_pib_headers]
        },
        {
            "name" : delete_rows_by_index,
            "args" : [[0, 1, 2, 3, 6, 8, 12], 17]
        },
        {
            "name" : pivot,
            "args" : ["annee"]
        },
        {
            "name" : rename_columns,
            "args" : [{
                "Produit intérieur brut (PIB)": "pib_total",
                "Importations de biens et de services" : "taux_importation",
                "Dépense de consommation finale" : "taux_consommation",
                "ménages" : "taux_consommation_menages",
                "administrations publiques" : "taux_consommation_gouvernement",
                "Formation brute de capital fixe" : "taux_investissement",
                "sociétés et entreprises individuelles non financières" : "taux_investissement_entreprises",
                "administrations publiques_1" : "taux_investissement_gouvernement",
                "ménages hors entrepreneurs individuels" : "taux_investissement_menages",
                "Exportations de biens et de services" : "taux_exportations",
                "Demande intérieure hors stocks" : "taux_demande_interieure"
            }]
        },
        {
            "name" : convert_columns,
            "args" : [{
                "annee" :'int',
                "pib_total" : "decimal_1",
                "taux_importation" : "decimal_1",
                "taux_consommation" : "decimal_1",
                "taux_consommation_menages" : "decimal_1",
                "taux_consommation_gouvernement" : "decimal_1",
                "taux_investissement" : "decimal_1",
                "taux_investissement_entreprises" : "decimal_1",
                "taux_investissement_gouvernement" : "decimal_1",
                "taux_investissement_menages" : "decimal_1",
                "taux_exportations" : "decimal_1",
                "taux_demande_interieure" : "decimal_1"
            }]
        },
    ],
    "Inflation" : [
        {
            "name" : set_row_as_headers,
            "args" : [1]
        },
        {
            "name" : delete_rows_by_index,
            "args" : [[0, 1, 2], 35]
        },
        {
            "name" : rename_columns,
            "args" : [{
                "Année" : "annee",
                "Taux d'inflation" : "taux_inflation"
            }]
        },
        {
            "name" : convert_columns,
            "args" : [{
                "annee" : "int",
                "taux_inflation" : "decimal_1"
            }]
        }
    ],
    "Salaire_moyen" : [
        {
            "name" : rename_columns,
            "args" : [{
                "Année" : "annee",
                "Salaire Net" : "salaire"
            }]
        },
        {
            "name" : convert_columns,
            "args" : ["int"]
        }
    ],
    "Impot_moyen" : [
        {
            "name" : rename_columns,
            "args" : [{
                "Année" : "annee",
                "Impot" : "moyenne_impot"
            }]
        },
        {
            "name" : convert_columns,
            "args" : [{
                "annee" : "int",
                "moyenne_impot" : 'decimal_2'
            }]
        }
    ] 
}



create_datasets_from_file_sheets("MSPR - Economie.xlsx", instructions)