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
            "name" : columns_to_int,
            "args" : [["Année"]]
        },
        {
            "name" : columns_to_float,
            "args" : [[" Produit intérieur brut (PIB)", "Importations de biens et de services", "Dépense de consommation finale", "Dépense de consommation finale dont ménages",
                      "Dépense de consommation finale dont administrations publiques", "Formation brute de capital fixe", "Formation brute de capital fixe dont sociétés et entreprises individuelles non financières",
                      "Formation brute de capital fixe dont administrations publiques", " Formation brute de capital fixe dont ménages hors entrepreneurs individuels", "Exportations de biens et de services",
                      "Demande intérieure hors stocks"], 1]
        },
        {
            "name" : complete_with_inteprolate,
            "args" : []
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
            "name" : columns_to_int,
            "args" : [["Année"]]
        },
        {
            "name" : columns_to_float,
            "args" : [["Taux d'inflation"]]
        },
        {
            "name" : complete_with_inteprolate,
            "args" : []
        },
    ],
    "Salaire_moyen" : [
        {
            "name" : columns_to_int,
            "args" : []
        },
        {
            "name" : complete_with_inteprolate,
            "args" : []
        },
    ],
   "Impot_moyen" : [
        {
            "name" : columns_to_int,
            "args" : [["Année"]]
        },
        {
            "name" : columns_to_float,
            "args" : [["Impot"], 2]
        },
        {
            "name" : complete_with_inteprolate,
            "args" : []
        },
    ] 
}



create_datasets_from_file_sheets("MSPR - Economie.xlsx", instructions)