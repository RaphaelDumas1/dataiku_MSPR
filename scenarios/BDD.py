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

delinquance_ids = {}
age_ids = {}

# Liste des tables avec les colonnes et id
tables = [
    {
        "name": "dim_annee",
        "columns": {
            "annee": "annee"
        },
        "id": None,
        "add": {}  # Liste vide pour dim_annee car il n'y a pas de colonnes supplémentaires
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
        "add": {"dim_annee_id" : "dim_annee"}
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
        "add": {"dim_annee_id" :"dim_annee"}
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
        "add": {"dim_annee_id": "dim_annee"}
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
        "add": {"dim_annee_id" : "dim_annee"}
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
        "add": {"dim_annee_id" : "dim_annee"}
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
        "add": {"dim_annee_id" : "dim_annee"} 
    },
    {
        "name": "fait_scolarisation",
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
        "add": {"dim_annee_id" : "dim_annee"} 
    },
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
    
    # TABLE dim_age
    
    queries = [text(f"DELETE FROM dim_age;")]

    ds_repartition_age = dataiku.Dataset("Repartition age")
    ds_taux_scolarisation = dataiku.Dataset("Taux_scolarisation")
    df_repartition_age = ds_repartition_age.get_dataframe()
    df_taux_scolarisation = ds_taux_scolarisation.get_dataframe()
    labels_repartition_age = [col for col in df_repartition_age.columns if col != "annee"]
    labels_taux_scolarisation = [col for col in df_taux_scolarisation.columns if col != "annee"]
    labels = labels_repartition_age + labels_taux_scolarisation

    for label in labels: 
        queries.append(buildInsertQuery(row, "dim_age", {}, {"repartition_age" : label}, True))
        age_ids.update({label : executeQueries(conn, queries, "dim_age")})
        queries = []
    
    
    for index, row in final_df.iterrows():
        for table in tables:
            table_name = table["name"]
            columns = table["columns"]
            add = table["add"]
            
            # Delete old datas
            if(row["annee"] == 2006):
                queries.append(text(f"DELETE FROM {table_name};"))
            
            # Add new columns
            to_add = {}
            for key, value in add:
                for ref_table in tables:
                    if value == ref_table["name"] and ref_table["id"] is not None:
                        value = ref_table["id"] 
                
                to_add.update({key : value})
                    
            queries.append(buildInsertQuery(row, table_name, columns, to_add, True))        
            table["id"] = executeQueries(conn, queries, table_name)
            queries = []
            
            
            if(table_name == "fait_demographique"):
                ds_delinquance = dataiku.Dataset("Delinquance")
                df_delinquance = ds_delinquance.get_dataframe()               
                df_delinquance_filtered = df_delinquance[df_test['annee'] == row["annee"]]
                
                for i, r in df_delinquance_filtered.iterrows():
                    
                    # TABLE dim_delinquance
                    
                    # If delinquance doesnt exist
                    if r["unite_de_compte"] not in delinquance_ids:
                        
                        delinquance_columns = {
                            "unite_de_compte" : "type_delinquance",
                            "indicateur" : "indicateur",
                        }

                        queries.append(buildInsertQuery(row, "dim_delinquance", delinquance_columns, {}, True))
                        delinquance_ids.update({r["unite_de_compte"] : executeQueries(conn, queries, "dim_delinquance")})
                        queries = []
                    
                    # TABLE dim_delinquance_has_fait_demograhique
                    
                    delinquance_demographique_mapping = {
                        "dim_delinquance_id" : delinquance_ids[r["unite_de_compte"]]
                        "fait_demographique_id" : table["id"],   
                    }
                    
                    queries.append(buildInsertQuery(row, "dim_delinquance_has_fait_demograhique", {"nombre" : "total"}, col_mapping, False))
                    executeQueries(conn, queries, "dim_delinquance_has_fait_demograhique")    
                    queries = []
                
                # TABLE fait_demographique_has_dim_age
                
                df_repartition_age_filtered = df_repartition_age[df_repartition_age['annee'] == row["annee"]]
                row_unique = df_repartition_age_filtered.iloc[0]
                
                for col in row_unique.index:
                    if col != "annee":
                        col_mapping = {
                            "dim_age_id" : age_ids[col]
                            "fait_demographique_id" : table["id"],
                        }
                        queries.append(buildInsertQuery(row, "fait_demographique_has_dim_age", {row_unique[col] : "total"}, col_mapping, False))
                executeQueries(conn, queries, "fait_demographique_has_dim_age")
                
            queries = []
            df_filtre = df_test[df_test['annee'] == row["annee"]]
            row_unique = df_filtre.iloc[0]
            for col in row_unique.index:
                if col != "annee":
                    col_mapping = {
                        "dim_age_id" : age_ids[col]
                        "fait_demographqiue_id" : table["id"],
                    }
                    queries.append(buildInsertQuery(row, "fait_demographique_has_dim_age", {row_unique[col] : "total"}, col_mapping, False))
                executeQueries(conn, queries, "fait_demographique_has_dim_age")
            
            
                
                
def buildInsertQuery(row, table_name, mapping, columns_to_add={}, returning=None):
    values_dict = {sql_col: row[df_col] for df_col, sql_col in col_mapping.items()}
    values_dict.update(columns_to_add)
    
    columns_str = ", ".join(values_dict.keys())
    placeholders = ", ".join([f":{col}" for col in values_dict.keys()])
    
    query = f"""
        INSERT INTO {table_name} ({columns_str})
        VALUES ({placeholders})
    """
    
    if returning:
        query += f"\nRETURNING {returning}"

    return {
        "query": text(query),
        "params": values_dict,
        "returning": returning is not None
    }

def executeQueries(conn, queries, table_name):
    try:
        for q in queries:
            query = q["query"]
            params = q.get("params", {}) 
            has_returning = q.get("returning", False)

            result = conn.execute(query, **params) if params else conn.execute(query)
            conn.commit()
            
            if has_returning:
                return result.scalar()
    except Exception as e:
        conn.rollback()
                
