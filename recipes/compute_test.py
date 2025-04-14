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
        "input": "MSPR_Taux_de_natalite",
        "output": "Taux_de_natalite",
        "functions": []
    },
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Demographie.xlsx", datasets, [])
