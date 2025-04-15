import dataiku
import pandas as pd
import io  # Importation du module pour gérer un buffer mémoire

# Connexion au projet
client = dataiku.api_client()
project = client.get_project(dataiku.default_project_key())

# Liste des datasets à exporter
datasets_names = [
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
  "Evolution_trimestrielle_emploi",
  "Logement", 
  "Type_logement",
  "Categorie_logement", 
  "Statut_occupation_logement",
  "Composition_menage",
  "Nombre_enfant",
  "Nombre_detranger",
  "Quotient_familiale",
  "Taux_de_natalite",
  "Taux_de_mortalite",
  "Population",
  "Repartition_age",
  "Repartition_sexe",
  "Nombre_dimmigre", 
    
  
  "Impot_moyen", 
  
  , "Evolution_population", 
   
   
   
   
   
   
  "Repartition_des_contrats", 
   
  "Salaire_moyen", 
   
  
  
   
  "Taux_de_pauvrete", 
    
   
  
  "Legislatives"
]
# Ajoutez vos datasets ici
folder = dataiku.Folder("test")  # ID du dossier de destination

for dataset_name in datasets_names:
    dataset = dataiku.Dataset(dataset_name)
    df = dataset.get_dataframe()
    
    # Création d'un buffer mémoire
    buffer = io.BytesIO()
    
    # Écriture dans le buffer
    df.to_csv(buffer, index=False, sep=";")  # Ajoutez encoding si nécessaire
    
    # Sauvegarde dans le dossier
    file_path = f"{dataset_name}.csv"
    with folder.get_writer(file_path) as writer:
        writer.write(buffer.getvalue())  # Écrit le contenu du buffer dans le fichier

print("Export terminé avec succès ✅")

