from utils import (
    create_datasets_from_file_sheets, 
    columns_to_int, 
    process_annuaire, 
    columns_to_string, 
    delete_where_not_equal, 
    delete_columns_by_name
)

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
            
        ]
    },
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Education.xlsx", datasets, [])