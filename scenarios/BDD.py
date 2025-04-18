from sqlalchemy import create_engine, inspect, text
import dataiku
from dataiku import Dataset
import pandas as pd

# Connexion à la base de données PostgreSQL
engine = create_engine('postgresql://postgres:test@host.docker.internal:5432/MSPR')

# Liste des datasets
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
]

# Liste des tables avec les colonnes et id
tables = [
    {
        "name": "dim_annee",
        "columns": {
            "annee": "annee"
        },
        "id": None,
        "add": []  # Liste vide pour dim_annee car il n'y a pas de colonnes supplémentaires
    },
    {
        "name": "fait_administration_penitentiaire",
        "columns": {
            "dim_annee_id": "dim_annee"
        },
        "id": None,
        "add": [
            {"name": "dim_annee_id", "value": "dim_annee"}  # Ajouter une colonne avec l'ID de dim_annee
        ]
    }
]

final_df = None

# Fusionner tous les datasets
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

# Inspecteur pour obtenir des informations sur les colonnes de la base
inspector = inspect(engine)

with engine.connect() as conn:
    # Pour chaque ligne dans final_df
    for index, row in final_df.iterrows():
        # Pour chaque table
        for table in tables:
            table_name = table["name"]
            columns = table["columns"]
            delete_sql = text(f"DELETE FROM {table_name};")

            # Sélectionner les colonnes à insérer en fonction de columns
            row_to_insert = row[[key for key in columns.keys() if key in final_df.columns]].dropna()

            # Ajouter les colonnes spécifiées dans add (si elles sont définies)
            for add_column in table.get("add", []):
                column_name = add_column["name"]
                column_value = add_column["value"]

                # Parcourir toutes les tables pour trouver la table qui correspond à column_value
                for ref_table in tables:
                    if column_value == ref_table["name"]:
                        # Si l'ID de la table référencée est défini, on remplace la valeur de la colonne par l'ID
                        if ref_table["id"] is not None:
                            row_to_insert[column_name] = ref_table["id"]
                            print(f"Assigning ID from table '{ref_table['name']}' ({ref_table['id']}) to column '{column_name}' for row {row['annee']}")

            # Si la ligne à insérer est vide après le filtrage, passer à la ligne suivante
            if row_to_insert.empty:
                print(f"Skipping year {row['annee']} as no valid data found for table {table_name}.")
                continue

            # Construire la chaîne des colonnes à insérer
            columns_str = ", ".join(row_to_insert.index)
            # Créer les placeholders pour les valeurs
            placeholders = ", ".join([f":{col}" for col in row_to_insert.index])
            print(row, "roww")
            # Créer la requête SQL pour l'insertion
            insert_sql = text(f"""
                INSERT INTO {table_name} ({columns_str})
                VALUES ({placeholders})
                RETURNING id;
            """)
            print("sql", insert_sql)
            # Connexion à la base de données et exécution de la requête

                try:
                    # Exécution de la requête avec les valeurs du DataFrame
                    if(row["annee"] == 2006):
                        conn.execute(delete_sql) 
                    result = conn.execute(insert_sql, row_to_insert.to_dict())
                    # Récupérer l'ID auto-incrémenté retourné par la requête
                    inserted_id = result.scalar()
                    print(f"Inserted row for year {row['annee']} into table {table_name} with ID: {inserted_id}")
                    table["id"] = inserted_id  # Mettre à jour l'ID de la table après insertion
                    conn.commit()  # Valider la transaction
                except Exception as e:
                    # En cas d'erreur, rollback de la transaction
                    conn.rollback()
                    print(f"Error inserting row for year {row['annee']} into table {table_name}: {e}")