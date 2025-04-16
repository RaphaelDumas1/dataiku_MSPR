from utils import create_datasets_from_file_sheets, pivot, columns_to_int, columns_to_float, process_inflation, columns_to_float, delete_rows_by_index, set_row_as_headers

datasets = [
    {
        "name": "Pib",
        "functions": [
            {
                "name" : set_row_as_headers,
                "args" : [2]
            },
            {
                "name" : delete_rows_by_index,
                "args" : [[0, 1, 2], 35]
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
                "args" : [[" Produit intérieur brut (PIB)", "Importations de biens et de services", "Dépense de consommation finale", "Dépense de consommation finale dont ménages",
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
                "name" : process_inflation,
                "args" : []
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