import dataiku
import pandas as pd
from sqlalchemy import create_engine

# Connexion à PostgreSQL
engine = create_engine('postgresql://postgres:test@localhost:5432/MSPR')

# Liste des datasets du projet
project = dataiku.api_client().get_project("MSPR")
recipe = project.get_recipe("compute_test")

# Récupérer les datasets d'entrée de la recette
print("yess", doc(recipe))

for ds in input_datasets:
    dataset_name = ds["name"]
    dku_dataset = dataiku.Dataset(dataset_name)
    
    # Lecture des données
    df = dku_dataset.get_dataframe()
    
    # Écriture dans PostgreSQL
    df.to_sql(dataset_name.lower(), engine, if_exists='replace', index=False)
    print(f"✅ Dataset {dataset_name} écrit dans PostgreSQL")
