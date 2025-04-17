from sqlalchemy import create_engine
import dataiku
from dataiku import Dataset

engine = create_engine('postgresql://postgres:test@host.docker.internal:5432/MSPR')

datasets_names = [
  "Esperance_de_vie",
  "Taux_scolarisation",
  # "annuaire_des_ecoles_en_france",
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
  "Taux_de_pauvrete",
  "Evolution_population",
  "Pib",
  "Inflation",
  "Salaire_moyen",
  "Impot_moyen", 
  "Legislatives"
]  # à adapter

min_years = []

for name in datasets_names:
    print("lll", name)
    ds = Dataset(name)
    df = ds.get_dataframe(columns=['année'])  # suppose que la colonne s'appelle exactement "année"
    min_year = df['année'].min()
    min_years.append((name, min_year))

# Trouver le dataset avec l'année la plus ancienne
oldest = min(min_years, key=lambda x: x[1])
print(oldest)
