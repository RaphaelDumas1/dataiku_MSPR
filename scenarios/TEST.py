import dataiku
import pandas as pd
import io  # Importation du module pour gérer un buffer mémoire

# Connexion au projet
client = dataiku.api_client()
project = client.get_project(dataiku.default_project_key())

# Liste des datasets à exporter
datasets_names = ["Categorie_logement"]  # Ajoutez vos datasets ici
folder = dataiku.Folder("test")  # ID du dossier de destination

for dataset_name in datasets_names:
    dataset = dataiku.Dataset(dataset_name)
    df = dataset.get_dataframe()
    
    # Création d'un buffer mémoire
    buffer = io.BytesIO()
    
    # Écriture dans le buffer
    df.to_csv(buffer, index=False, encoding="utf-8", sep=";")  # Ajoutez encoding si nécessaire
    
    # Sauvegarde dans le dossier
    file_path = f"{dataset_name}.csv"
    with folder.get_writer(file_path) as writer:
        writer.write(buffer.getvalue())  # Écrit le contenu du buffer dans le fichier

print("Export terminé avec succès ✅")

