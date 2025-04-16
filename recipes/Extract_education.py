from utils import create_datasets_from_file_sheets, columns_to_int, columns_to_string, delete_where_not_equal, delete_columns_by_name, fill_empty_values, fill_empty_values_with_mean

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
                "name" : delete_columns_by_name,
                "args" : [['code_departement', 'code_region', 'libelle_departement', 'libelle_region']]
            },
            {
                "name" : fill_empty_values,
                "args" : [{
                    "type_etablissement": "Inconnu",
                    "statut_public_prive": "Inconnu",
                    "adresse_1": "Inconnue",
                    "adresse_2": "Inconnue",
                    "ecole_maternelle": 0.0,
                    "ecole_elementaire": 0.0,
                    "voie_generale" : 0.0,
                    "voie_technologique" : 0.0,
                    "voie_professionnelle" : 0.0,
                    "telephone": "Inconnu",
                    "fax": "Inconnu", 
                    "web": "Inconnu", 
                    "mail": "Inconnu", 
                    "telephone": "Inconnu", 
                    "restauration": 0.0,
                    "hebergement": 0.0,
                    "ulis": 0.0,
                    "apprentissage": 0.0,
                    "segpa": 0.0,
                    "section_arts": 0.0,
                    "section_cinema": 0.0,
                    "section_theatre": 0.0,
                    "section_sport": 0.0,
                    "section_internationale": 0.0,
                    "section_europeenne": 0.0,
                    "lycee_agricole": 0.0,
                    "lycee_militaire": 0.0,
                    "lycee_des_metiers": 0.0,
                    "post_bac": 0.0,
                    "appartenance_education_prioritaire": "Aucune",
                    "greta": 0.0,
                    "siren_siret": "Inconnu",
                    "fiche_onisep": "Inconnue",
                    "position": "48.856614,2.3522219",
                    "type_contrat_prive": "Inconnu",
                    "coordx_origine": "2.3522",
                    "coordy_origine": "48.8566",
                    "epsg_origine": "EPSG:2154",
                    "nom_circonscription": "Inconnu",
                    "latitude": "48.856614",
                    "longitude": "2.3522219",
                    "precision_localisation": "Inconnue",
                    "rpi_concentre" : 0.0,
                    "rpi_disperse" : 0.0,
                    "pial" : "Inconnu",
                    "etablissement_mere" : "Inconnu",
                    "type_rattachement_etablissement_mere" : "Inconnu",
                    "code_circonscription" : "Inconnu",
                    "code_zone_animation_pedagogique" : "Inconnu",
                    "libelle_zone_animation_pedagogique" : "Inconnu",
                    "code_bassin_formation" : "Inconnu",
                    "libelle_bassin_formation" : "Inconnu"
                }]
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