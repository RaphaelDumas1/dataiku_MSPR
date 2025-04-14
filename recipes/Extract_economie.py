from utils import create_datasets_from_file_sheets, process_pib

datasets = [
    {
        "name": "Pib",
        "functions": [
            {
                "name" : process_pib,
                "args" : []
            }
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