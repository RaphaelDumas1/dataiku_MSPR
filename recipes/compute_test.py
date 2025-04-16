import dataiku
import pandas as pd
from sqlalchemy import create_engine

# Connexion à PostgreSQL
engine = create_engine('postgresql://postgres:test@localhost:5432/MSPR')

# Liste des datasets du projet
project = dataiku.api_client().get_project("MSPR")
recipe = project.get_recipe("compute_test")
input_datasets = recipe.get_settings().get_recipe_inputs()
print("yesss", input_datasets)

# Boucle sur les datasets d'entrée
for ds_info in input_datasets.values():
    dataset_name = ds_info["refs"]  # Récupère la référence (le nom du dataset)
    
    # Crée un objet dataset Dataiku
    dku_dataset = dataiku.Dataset(dataset_name)
    
    # Lecture des données du dataset
    df = dku_dataset.get_dataframe()
    
    # Nom de la table dans PostgreSQL (tu peux personnaliser le nom si besoin)
    table_name = dataset_name.lower()

    # Exportation vers PostgreSQL
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"✅ Dataset {dataset_name} écrit dans PostgreSQL")