from utils import create_datasets_from_file_sheets

datasets = [
    {
        "name": "Taux_scolarisation",
        "functions": []
    },
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Sante.xlsx", datasets, [])
