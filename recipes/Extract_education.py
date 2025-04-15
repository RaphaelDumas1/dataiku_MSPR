from utils import create_datasets_from_file_sheets, columns_to_int, process_annuaire, columns_to_string

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
            },
            {
                 "name" : columns_to_string,
                 "args" : [["code_postal", "code_commune", "code_departement", "code_academie", "code_region", ""]]
            },
            {
                 "name" : columns_to_int,
                 "args" : [["ecole_maternelle", "ecole_elementaire", "voie_generale", "voie_technologique", "voie_professionnelle",
                           ]]
            }
        ]
    },
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Education.xlsx", datasets, [])