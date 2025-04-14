from utils import create_datasets_from_file_sheets

datasets = [
    {
        "name": "Taux_scolarisation",
        "functions": []
    },
    {
        "name": "annuaire_des_ecoles_en_france",
        "functions": []
    },
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Education.xlsx", datasets, [])