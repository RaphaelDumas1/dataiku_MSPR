from utils import create_datasets_from_file_sheets, columns_to_int, process_annuaire

datasets = [
    {
        "name": "Taux_scolarisation",
        "functions": [
            {
                 "name" : columns_to_int,
                 "args" : [["Année"]]
            }
        ]
    },
    {
        "name": "annuaire_des_ecoles_en_france",
        "functions": [
            {
                "name" : process_annuaire,
                "args" : []
            }
        ]
    },
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Education.xlsx", datasets, [])