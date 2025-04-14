from utils import create_datasets_from_file_sheets, process, process_category_metier, pivot_years, to_int

datasets = [
    {
        "name": "MSPR_Taux_scolarisation",
        "functions": []
    },
]

create_datasets_from_file_sheets("MSPR", "aPmnwurD", "MSPR - Education.xlsx", [])
