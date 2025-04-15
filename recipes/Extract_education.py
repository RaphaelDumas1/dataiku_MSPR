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
                           "siren_siret", "coordx_origine", "coordy_origine", "rpi_disperse", "code_type_contrat_prive", "code_bassin_formation",
                           "code_nature", "code_zone_animation_pedagogique"]]
            },
            {
                 "name" : columns_to_int,
                 "args" : [["ecole_maternelle", "ecole_elementaire", "voie_generale", "voie_technologique", "voie_professionnelle",
                           "restauration", "hebergement", "ulis", "apprentissage", "segpa", "section_arts", "section_cinema", "section_theatre",
                           "section_sport", "section_internationale", "section_europeenne", "lycee_agricole", "lycee_militaire", "lycee_des_metiers",
                           "post_bac", "greta", "nombre_d_eleves", "multi_uai", "rpi_concentre"]]
            }
        ]
    },
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Education.xlsx", datasets, [])