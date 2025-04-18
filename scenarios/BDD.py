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
    
table_name = "dim_annee"  # Remplace par le nom de ta table PostgreSQL
inspector = inspect(engine)
table_columns = [col['name'] for col in inspector.get_columns(table_name)]

print("Table columns:", table_columns)
print("final", len(final_df))


for index, row in final_df.iterrows():
    row_to_insert = row[[col for col in final_df.columns if col in table_columns]].dropna()

    print("ttt", row_to_insert)
    if row_to_insert.empty:
        print("skip")
        continue  # Skip si la ligne est vide après filtrage

    columns_str = ", ".join(row_to_insert.index)
    placeholders = ", ".join([f":{col}" for col in row_to_insert.index])
    print("aaa")
    insert_sql = text(f"""
        INSERT INTO {table_name} ({columns_str})
        VALUES ({placeholders})
        RETURNING id;
    """)  # Assure-toi que la colonne auto-incrémentée s'appelle bien "id"
    print("sql", insert_sql)
    with engine.connect() as conn:
        result = conn.execute(insert_sql, row_to_insert.to_dict())
        inserted_id = result.scalar()  # Récupère la valeur retournée par RETURNING id
        print(f"ooo : {inserted_id}")
    
    
print("mmm", final_df.columns)
        
    
