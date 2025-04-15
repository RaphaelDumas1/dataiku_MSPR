from utils import create_datasets_from_file_sheets, process_pib, pivot, columns_to_int, columns_to_float, process_inflation

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
                "args" : [[" Produit intérieur brut (PIB)", "Importations de biens et de services", "Dépense de consommation finale", "Dont ménages",
                          "Dont administrations publiques", "Formation brute de capital fixe", "Dont sociétés et entreprises individuelles non financières",
                          "Dont administrations publiques 2", "Dont ménages hors entrepreneurs individuels", "Exportations de biens et de services",
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
        "functions": []
    },
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Economie.xlsx", datasets, [])