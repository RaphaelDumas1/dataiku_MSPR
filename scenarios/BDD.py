from sqlalchemy import create_engine, inspect, text
import dataiku
from dataiku import Dataset
import pandas as pd

engine = create_engine('postgresql://postgres:test@host.docker.internal:5432/MSPR')

datasets_names = [
  "Esperance_de_vie",
  "Taux_scolarisation",
  # "annuaire_des_ecoles_en_france",
  "Administration_penitentiaire", 
  # "Delinquance", 
  # "Presidentielles",
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
  #"Quotient_familiale",
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
  # "Legislatives"
]  # à adapter

tables = [
    {
        "name" : "dim_annee",
        "columns" : {
            "annee" : "annee"
        },
        "id" : None
    },
    {
        "name" : "dim_annee",
        "columns" : {
            "annee" : "annee"
        },
        "id" : None
    }
]

final_df = None


for ds_name in datasets_names:
    ds = dataiku.Dataset(ds_name)
    df = ds.get_dataframe()
    
    new_columns = {
        col: f"{col}_{ds_name}" for col in df.columns if col != "annee"
    }
    
    df = df.rename(columns=new_columns)
    
    if final_df is None:
        final_df = df  # première itération, on initialise
    else:
        final_df = pd.merge(final_df, df, on="annee", how="outer")  # merge avec le reste
    
inspector = inspect(engine)

# Foreach year
for index, row in final_df.iterrows():
    # Foreach table
    for table in tables:
        table_name = table["name"]
        columns = table["columns"]
        
        # Sélectionner les colonnes à insérer, en fonction des colonnes définies dans `columns`
        row_to_insert = row[[key for key in columns.keys() if key in final_df.columns]].dropna()

        # Si la ligne à insérer est vide après le filtrage, passer à la ligne suivante
        if row_to_insert.empty:
            print(f"Skipping year {row['annee']} as no valid data found for table {table_name}.")
            continue

        # Construire la chaîne des colonnes à insérer
        columns_str = ", ".join(row_to_insert.index)
        # Créer les placeholders pour les valeurs
        placeholders = ", ".join([f":{col}" for col in row_to_insert.index])

        # Créer la requête SQL pour l'insertion
        insert_sql = text(f"""
            INSERT INTO {table_name} ({columns_str})
            VALUES ({placeholders})
            RETURNING id;
        """)

        # Connexion à la base de données et exécution de la requête
        with engine.connect() as conn:
            try:
                # Exécution de la requête avec les valeurs du DataFrame
                result = conn.execute(insert_sql, row_to_insert.to_dict())
                # Récupérer l'ID auto-incrémenté retourné par la requête
                inserted_id = result.scalar()
                print(f"Inserted row for year {row['annee']} into table {table_name} with ID: {inserted_id}")
                table["id"] = inserted_id
                conn.commit()  # Valider la transaction
            except Exception as e:
                # En cas d'erreur, rollback de la transaction
                conn.rollback()
                print(f"Error inserting row for year {row['annee']} into table {table_name}: {e}")

        
    
