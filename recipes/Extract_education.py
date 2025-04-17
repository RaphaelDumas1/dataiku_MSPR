from utils import create_datasets_from_file_sheets, columns_to_int, columns_to_string, delete_where_not_equal, fill_empty_values, fill_empty_values_with_mean, delete_columns__not_in_list

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
                "name" : delete_where_not_equal,
                "args" : ["code_departement", 35.0]
            },
            {
                "name" : delete_columns__not_in_list,
                "args" : [['identifiant_de_l_etablissement', 'nom_etablissement', 'nombre_d_eleves', 'type_etablissement']]
            },
            {
                "name" : fill_empty_values,
                "args" : [{"type_etablissement": "Inconnu"}]
            },
            {
                 "name" : fill_empty_values_with_mean,
                 "args" : [["nombre_d_eleves"]]
            },
            {
                 "name" : columns_to_string,
                 "args" : [["code_postal", "code_commune", "code_academie", "telephone",
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