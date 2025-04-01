import dataiku
import pandas as pd

# Connexion au projet
client = dataiku.api_client()
project = client.get_project(dataiku.default_project_key())

# Liste des datasets à exporter
datasets_names = ["Categorie_logement"]  # Modifiez avec vos datasets
folder = dataiku.Folder("test")  # ID du dossier de destination

for dataset_name in datasets_names:
    dataset = dataiku.Dataset(dataset_name)
    df = dataset.get_dataframe()
    
    # Nom du fichier CSV
    file_path = f"{dataset_name}.csv"
    
    # Sauvegarde dans le dossier
    with folder.get_writer(file_path) as writer:
        df.to_csv(writer, index=False)

print("Export terminé avec succès ✅")
