import dataiku
import pandas as pd
import io
from utils import get_dataframe_from_dataset

#
# Environnement
#

OUTPUT_FOLDER = "CSV_output"

#
# Datas
#

datasets_to_export = [
    "Esperance_de_vie",
    "Taux_scolarisation",
    "annuaire_des_ecoles_en_france",
    "Administration_penitentiaire", 
    "Delinquance", 
    "Presidentielles",
    "Taux_de_chomage",
    "Repartition_des_contrats",
    "Categorie_metiers",
    "Nombre_de_salarie",
    # "Evolution_trimestrielle_emploi",
    "Logement", 
    "Type_logement",
    "Categorie_logement", 
    "Statut_occupation_logement",
    "Composition_menage",
    "Nombre_enfant",
    "Nombre_detranger",
    # "Quotient_familiale",
    "Taux_de_natalite",
    "Taux_de_mortalite",
    "Population",
    "Repartition_age",
    "Repartition_sexe",
    "Nombre_dimmigre",
    "Taux_de_pauvrete",
    "Evolution_population",
    "Pib",
    "Inflation",
    "Salaire_moyen",
    "Impot_moyen", 
    "Legislatives"
]


client = dataiku.api_client()
project = client.get_project(dataiku.default_project_key())
output_folder = dataiku.Folder(OUTPUT_FOLDER) 

for dataset in datasets_to_export:
    df = get_dataframe_from_dataset(dataset)
    
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False, sep=";")

    with output_folder.get_writer(f"{dataset}.csv") as writer:
        writer.write(buffer.getvalue())