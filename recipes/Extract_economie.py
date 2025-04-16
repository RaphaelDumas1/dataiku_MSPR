from utils import create_datasets_from_file_sheets, process_pib, pivot, columns_to_int, columns_to_float, columns_to_float, set_row_as_headers, delete_rows_by_index, make_unique, set_row_as_headers

def pib_column(columns):
    return make_unique(columns.astype(str).str.strip().str.replace(" \(r\)", "", regex=True))

datasets = [
    {
        "name": "Pib",
        "functions": [
            {
                "name" : process_pib,
                "args" : []
            },
            {
                "name" : pivot,
                "args" : ["Année"]
            },
            {
                "name" : columns_to_int,
                "args" : [["Année"]]
            },
            {
                "name" : columns_to_float,
                "args" : [["Produit intérieur brut (PIB)", "Importations de biens et de services", "Dépense de consommation finale", "Dépense de consommation finale dont ménages",
                          "Dépense de consommation finale dont administrations publiques", "Formation brute de capital fixe", "Formation brute de capital fixe dont sociétés et entreprises individuelles non financières",
                          "Formation brute de capital fixe dont administrations publiques", " Formation brute de capital fixe dont ménages hors entrepreneurs individuels", "Exportations de biens et de services",
                          "Demande intérieure hors stocks"], 1]
            },
        ]
    },
    {
        "name": "Inflation",
        "functions": [
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
        ]
    },
    {
        "name": "Salaire_moyen",
        "functions": [
            {
                "name" : columns_to_int,
                "args" : []
            },
        ]
    },
    {
        "name": "Impot_moyen",
        "functions": [
            {
                "name" : columns_to_int,
                "args" : [["Année"]]
            },
            {
                "name" : columns_to_float,
                "args" : [["Impot"], 2]
            },
        ]
    },
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Economie.xlsx", datasets, [])