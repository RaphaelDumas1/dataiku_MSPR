from utils import create_datasets_from_file_sheets

datasets = [
    {
        "name": "Esperance_de_vie",
        "functions": []
    },
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Sante.xlsx", datasets, [])