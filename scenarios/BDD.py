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
            "dim_annee_id": "dim_annee",
            "personnes prises en charge" : "nombre_pris_en_charge",
            "mesures en cours" : "nombre_en_cours",
            "sursis1" : "nombre_sursis",
            "travail d'interet general (tig)2" : "nombre_travaux_interet_general",
            "liberations conditionnelles3" : "nombre_liberations_conditionnelles",
            "autres mesures" : "autres"
        },
        "id": None,
        "add": [
            {"name": "dim_annee_id", "value": "dim_annee"}  # Ajouter une colonne avec l'ID de dim_annee
        ]
    },
    {
        "name": "fait_menage",
        "columns": {
            "ensemble": "total",
            " - hommes seuls" : "homme_seul",
            " - femmes seules" : "femme seule",
            "- un couple avec enfant(s)" : "couple_avec_enfant",
            "- un couple sans enfant" : "couple_sans_enfant",
            "- une famille monoparentale" : "famille_monoparentale",
            "aucun enfant" : "sans_enfant",
            "1 enfant" : "un",
            "2 enfants" : "deux",
            "3 enfants" : "trois",
            "4 enfants ou plus" : "quatre_et_plus"
        },
        "id": None,
        "add": [
            {"name": "dim_annee_id", "value": "dim_annee"}  # Ajouter une colonne avec l'ID de dim_annee
        ]  # Liste vide pour dim_annee car il n'y a pas de colonnes supplémentaires
    },
    {
        "name": "fait_demographique",
        "columns": {
            "nombre": "total",
            "population homme" : "nombre_hommes",
            "population femme" : "nombre_femmes",
            "taux de natalite" : "nombre_naissance",
            "taux de deces" : "nombre_mortalite",
            "nombre" : "nombre_immigrant",
            "nombre" : "nombre_etranger",
            "homme_total" : "esperance_homme",
            "femmes_sans_incapacite" : "esperance_femme_sans_incapacite",
            "femme_total" : "esperance_femme",
            "hommes_sans_incapacite" : "esperance_homme_sans_incapacite"
        },
        "id": None,
        "add": [
            {"name": "dim_annee_id", "value": "dim_annee"}  # Ajouter une colonne avec l'ID de dim_annee
        ]  # Liste vide pour dim_annee car il n'y a pas de colonnes supplémentaires
    },
    {
        "name": "fait_economie",
        "columns": {
            "produit interieur brut (pib)": "pib_total",
            "importations de biens et de services" : "taux_importation",
            "population femme" : "taux_consommation",
            "depense de consommation finale dont menages" : "taux_consommation_menages",
            "depense de consommation finale dont administrations_publiques" : "taux_consommation_gouvernement",
            "formation brute de capital fixe" : "taux_investissement",
            "formation brute de capital fixe dont societes et entreprises individuelles non financieres" : "taux_investissement_entreprises",
            "formation brute de capital fixe dont administrations_publiques" : "taux_investissement_gouvernement",
            "formation brute de capital fixe dont menages hors entrepreneurs individuels" : "taux_investissement_menages",
            "exportations de biens et de services" : "taux_exportations",
            "Impot" : "moyenne_impot",
            "taux d'inflation" : "taux_inflation"
        },
        "id": None,
        "add": [
            {"name": "dim_annee_id", "value": "dim_annee"}  # Ajouter une colonne avec l'ID de dim_annee
        ]  # Liste vide pour dim_annee car il n'y a pas de colonnes supplémentaires
    },
    {
        "name": "fait_travail",
        "columns": {
            "salaire net": "total",
            "agriculteurs exploitants" : "nombre_agriculteurs",
            "artisans, commercants, chefs entreprise" : "nombre_artisans",
            "cadres et professions intellectuelles superieures" : "nombre_cadres",
            "professions intermediaires" : "nombre_professions_intermediaires",
            "employes" : "nombre_employes",
            "ouvriers" : "nombre_ouvriers",
            "retraites" : "nombre_retraites",
            "autres personnes sans activite professionnelle" : "nombre_sans_emploi",
            "cdi" : "nombre_cdi",
            "cdd" : "nombre_cdd",
            "taux" : "taux_chomage"
        },
        "id": None,
        "add": [
            {"name": "dim_annee_id", "value": "dim_annee"}  # Ajouter une colonne avec l'ID de dim_annee
        ]  # Liste vide pour dim_annee car il n'y a pas de colonnes supplémentaires
    },
    {
        "name": "fait_logement",
        "columns": {
            "nombre de logements": "total",
            "maisons" : "nombre_maisons",
            "appartements" : "nombre_appartements",
            "autres logements" : "nombre_autres",
            "proprietaires" : "nombre_proprietaires",
            "locataires" : "nombre_locataires",
            "- dont locataires d'un logement hlm loue vide" : "nombre_hlm",
            "loges gratuitement" : "nombre_loges_gratuit",
            "residences principales" : "nombre_residences_principales",
            "resid. secondaires et log. occasionnels" : "nombre_residences_secondaires",
            "logements vacants" : "nombre_logements_vacants"
        },
        "id": None,
        "add": [
            {"name": "dim_annee_id", "value": "dim_annee"}  # Ajouter une colonne avec l'ID de dim_annee
        ]  # Liste vide pour dim_annee car il n'y a pas de colonnes supplémentaires
    },
    {
        "name": "dim_delinquance",
        "columns": {
            "nombre": "total",
            "unite_de_compte" : "type_delinquance",
            "indicateur" : "indicateur",
        },
        "id": None,
        "add": []  # Liste vide pour dim_annee car il n'y a pas de colonnes supplémentaires
    },
    {
        "name": "dim_delinquance_has_fait_demographique",
        "columns": {},
        "id": None,
        "add": [
            {"name": "dim_delinquance_id", "value": "dim_delinquance"},
            {"name": "fait_demographique_id", "value": "dim_delinquance"},
        ]
    },
]

ids = {
        
    }


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
                # Delete old datas
                if(row["annee"] == 2006):
                    conn.execute(delete_sql) 
                    
                result = conn.execute(insert_sql, row_to_insert.to_dict())
                table["id"] = result.scalar()
                conn.commit()
            except Exception as e:
                # En cas d'erreur, rollback de la transaction
                conn.rollback()
                print(f"Error inserting row for year {row['annee']} into table {table_name}: {e}")