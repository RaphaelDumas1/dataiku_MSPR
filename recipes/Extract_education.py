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
                 "args" : [["code_postal", "code_commune", "code_departement", "code_academie", "code_region", "telephone",
                           "siren_siret", "coordx_origine", "coordy_origine"]]
            },
            {
                 "name" : columns_to_int,
                 "args" : [["ecole_maternelle", "ecole_elementaire", "voie_generale", "voie_technologique", "voie_professionnelle",
                           "restauration", "hebergement", "apprentissage", "segpa", "section_arts", "section_cinema", "section_theatre",
                           "section_sport", "section_internationale", "section_europeenne", "lycee_agricole", "lycee_militaire", "lycee_des_metiers",
                           "post_bac", "greta", "nombre_d_eleves"]]
            }
        ]
    },
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Education.xlsx", datasets, [])