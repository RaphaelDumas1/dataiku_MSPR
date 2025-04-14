from utils import create_datasets_from_file_sheets

datasets = [
    {
        "name": "Nombre_detranger",
        "functions": []
    },
    {
        "name": "Quotient_familiale",
        "functions": []
    },
    {
        "name": "Taux_de_natalite",
        "functions": []
    },
    {
        "name": "Taux_de_mortalite",
        "functions": []
    },
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Demographie.xlsx", datasets, [])
