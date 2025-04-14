from utils import create_datasets_from_file_sheets

datasets = [
    {
        "name": "Nombre_detranger",
        "functions": []
    },
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Demographie.xlsx", datasets, [])
