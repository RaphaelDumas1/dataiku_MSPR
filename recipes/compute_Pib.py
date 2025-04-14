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
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Education.xlsx", datasets, [])