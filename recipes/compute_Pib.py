from utils import create_datasets_from_file_sheets

datasets = [
    {
        "name": "Pib",
        "functions": []
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

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Education.xlsx", datasets, [])