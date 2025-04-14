from utils import create_datasets_from_file_sheets, process_pib, pivot, columns_to_int, columns_to_float

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
                "args" : [["Produit intérieur brut (PIB)", "Importations de biens et de services", "Dépense de consommation finale"]]
            },
        ]
    },
    {
        "name": "Inflation",
        "functions": []
    },
    {
        "name": "Salaire_moyen",
        "functions": []
    },
    {
        "name": "Impot_moyen",
        "functions": []
    },
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Economie.xlsx", datasets, [])