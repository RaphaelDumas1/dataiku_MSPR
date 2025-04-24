from general import create_datasets_from_file_sheets
from other import pivot, set_row_as_headers, rename_columns
from convert import convert_columns 
from delete import delete_rows_by_index

def pib_column(columns):
    return columns.astype(str).str.strip().str.replace(" \(r\)", "", regex=True)

instructions = {
    "Pib" : [
        {
            "name" : set_row_as_headers,
            "args" : [1, pib_column]
        },
        {
            "name" : delete_rows_by_index,
            "args" : [[0, 1, 2, 3, 6, 8, 12], 17]
        },
        {
            "name" : pivot,
            "args" : ["Année"]
        },
        {
            "name" : rename_columns,
            "args" : [{
                "ménages": "Dépense de consommation finale dont ménages",
                "administrations publiques": "Dépense de consommation finale dont administrations publiques",
                "sociétés et entreprises individuelles non financières": "Formation brute de capital fixe dont sociétés et entreprises individuelles non financières",
                "administrations publiques_1": "Formation brute de capital fixe dont administrations publiques",
                "ménages hors entrepreneurs individuels": "Formation brute de capital fixe dont ménages hors entrepreneurs individuels"
            }]
        },
        {
            "name" : convert_columns,
            "args" : [{
                "Année" :'int',
                " Produit intérieur brut (PIB)" : "decimal_1",
                "Importations de biens et de services" : "decimal_1",
                "Dépense de consommation finale" : "decimal_1",
                "Dépense de consommation finale dont ménages" : "decimal_1",
                "Dépense de consommation finale dont administrations publiques" : "decimal_1",
                "Formation brute de capital fixe" : "decimal_1",
                "Formation brute de capital fixe dont sociétés et entreprises individuelles non financières" : "decimal_1",
                "Formation brute de capital fixe dont administrations publiques" : "decimal_1",
                " Formation brute de capital fixe dont ménages hors entrepreneurs individuels" : "decimal_1",
                "Exportations de biens et de services" : "decimal_1",
                "Demande intérieure hors stocks" : "decimal_1"
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
            "name" : convert_columns,
            "args" : [{
                "Année" : 'int',
                "Taux d'inflation" : 'decimal_1'
            }]
        }
    ],
    "Salaire_moyen" : [
        {
            "name" : convert_columns,
            "args" : [{
                "Année" : 'int',
                "Salaire net" : 'int'
            }]
        }
    ],
   "Impot_moyen" : [
        {
            "name" : convert_columns,
            "args" : [{
                "Année" : 'int',
                "Impot" : 'decimal_2'
            }]
        }
    ] 
}



create_datasets_from_file_sheets("MSPR - Economie.xlsx", instructions)