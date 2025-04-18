from sqlalchemy import create_engine, inspect
import dataiku
from dataiku import Dataset
import pandas as pd

engine = create_engine('postgresql://postgres:test@host.docker.internal:5432/MSPR')

datasets_names = [
  "Esperance_de_vie",
  "Taux_scolarisation",
  # "annuaire_des_ecoles_en_france",
  "Administration_penitentiaire", 
  "Delinquance", 
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

final_df = None

for ds_name in datasets_names:
    ds = dataiku.Dataset(ds_name)
    df = ds.get_dataframe()
    
    new_columns = {
        col: f"{col}_{ds_name}" for col in df.columns if col != "année"
    }
    
    df = df.rename(columns=new_columns)
    
    if final_df is None:
        final_df = df  # première itération, on initialise
    else:
        final_df = pd.merge(final_df, df, on="année", how="outer")  # merge avec le reste
    
    table_name = "dim_année"  # Remplace par le nom de ta table PostgreSQL
    inspector = inspect(engine)

    # Liste des colonnes de la table dans PostgreSQL
    table_columns = [column['name'] for column in inspector.get_columns(table_name)]

    # Filtrer les colonnes du DataFrame pour qu'elles correspondent à la table
    df_columns_to_insert = [col for col in final_df.columns if col in table_columns]

    # Filtrer le DataFrame
    df_to_insert = final_df[df_columns_to_insert]

    # Insérer dans la table PostgreSQL
    df_to_insert.to_sql(table_name, engine, if_exists='append', index=False)
    
    
print("mmm", final_df.columns)
        
    
